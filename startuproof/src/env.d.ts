interface ImportMetaEnv {
  readonly PUBLIC_SUPABASE_URL?: string;
  readonly PUBLIC_SUPABASE_ANON_KEY?: string;
  readonly SITE_INDEXABLE?: string;
}
interface ImportMeta { readonly env: ImportMetaEnv }
