-- PROPOSED — NOT APPLIED. Review and test on a Supabase branch/staging project first.
-- Target: Supabase project `startup-roof` (nxtzbidikgkasfhswhen), which backs the current live site.
-- Fixes findings documented in docs/evidence/backend-findings.md.

begin;

-- 1. Signup must not grant privileged roles from user-editable metadata.
--    Everyone starts as 'founder' (baseline member); the requested role is recorded separately for review.
alter table public.profiles add column if not exists requested_role text;

create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  requested text := lower(coalesce(new.raw_user_meta_data->>'requested_role', new.raw_user_meta_data->>'role', 'founder'));
  final_role public.user_role := 'founder';
begin
  if exists (select 1 from public.admin_allowlist a where lower(a.email) = lower(new.email)) then
    final_role := 'admin';
  end if;
  insert into public.profiles (id, full_name, role, requested_role, company, country)
  values (new.id,
          coalesce(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1)),
          final_role,
          case when requested in ('founder','investor','mentor','partner','corporate') then requested else 'founder' end,
          new.raw_user_meta_data->>'company',
          new.raw_user_meta_data->>'country')
  on conflict (id) do nothing;
  return new;
end $$;

-- 2. Investor role is granted only by an admin after verification (role column is already
--    protected by protect_admin_columns). Mirror it into app_metadata so the Netlify Functions,
--    which read only app_metadata, see the same decision:
create or replace function public.sync_investor_verified()
returns trigger language plpgsql security definer set search_path = public, auth as $$
begin
  if new.role is distinct from old.role then
    update auth.users set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb)
      || jsonb_build_object('investor_verified', new.role = 'investor')
    where id = new.id;
  end if;
  return new;
end $$;
drop trigger if exists trg_sync_investor_verified on public.profiles;
create trigger trg_sync_investor_verified after update of role on public.profiles
  for each row execute function public.sync_investor_verified();

-- 3. Stop exposing auth.users through PostgREST (advisor 0002 / 0010).
revoke all on public.profiles_admin from anon, authenticated;
alter view public.profiles_admin set (security_invoker = true);
alter view public.deal_desk_matches_investor set (security_invoker = true);

-- 4. Helper functions should not be callable anonymously (advisor 0028).
revoke execute on function public.is_admin() from anon;
revoke execute on function public.my_role() from anon;
revoke execute on function public.protect_admin_columns() from anon, authenticated;
revoke execute on function public.admin_metrics() from authenticated;

commit;

-- 5. Manual (dashboard): Auth → Password security → enable leaked-password protection.
-- 6. Existing accounts that self-selected 'investor' should be reviewed:
--    select id, full_name, role from public.profiles where role = 'investor';
