export {};
// Header menus and mobile drawer. Visibility is driven only by the `hidden` attribute,
// and aria-expanded is always written in the same step, so they cannot drift apart.

const menus = Array.from(document.querySelectorAll<HTMLElement>('[data-menu]'));

function setMenu(li: HTMLElement, open: boolean) {
  const btn = li.querySelector<HTMLButtonElement>('.nav-trigger');
  const panel = li.querySelector<HTMLElement>('.nav-panel');
  if (!btn || !panel) return;
  btn.setAttribute('aria-expanded', String(open));
  panel.hidden = !open;
}
function closeAll(except?: HTMLElement) {
  menus.forEach((m) => { if (m !== except) setMenu(m, false); });
}

menus.forEach((li) => {
  const btn = li.querySelector<HTMLButtonElement>('.nav-trigger');
  const panel = li.querySelector<HTMLElement>('.nav-panel');
  if (!btn || !panel) return;
  setMenu(li, false);
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') !== 'true';
    closeAll(li);
    setMenu(li, open);
  });
  btn.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      closeAll(li);
      setMenu(li, true);
      panel.querySelector<HTMLAnchorElement>('a')?.focus();
    }
  });
  panel.addEventListener('keydown', (e) => {
    const links = Array.from(panel.querySelectorAll<HTMLAnchorElement>('a'));
    const i = links.indexOf(document.activeElement as HTMLAnchorElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); links[(i + 1) % links.length]?.focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); links[(i - 1 + links.length) % links.length]?.focus(); }
  });
  li.addEventListener('focusout', (e) => {
    const next = e.relatedTarget as Node | null;
    if (next && !li.contains(next)) setMenu(li, false);
  });
});

document.addEventListener('click', (e) => {
  const t = e.target as Node;
  if (!menus.some((m) => m.contains(t))) closeAll();
});

// Drawer
const drawer = document.getElementById('site-drawer');
const opener = document.querySelector<HTMLButtonElement>('[data-drawer-open]');
let lastFocus: HTMLElement | null = null;

function focusables(root: HTMLElement) {
  return Array.from(root.querySelectorAll<HTMLElement>('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])'))
    .filter((el) => !el.hasAttribute('hidden') && el.offsetParent !== null);
}
function openDrawer() {
  if (!drawer) return;
  lastFocus = document.activeElement as HTMLElement;
  drawer.hidden = false;
  opener?.setAttribute('aria-expanded', 'true');
  document.body.classList.add('drawer-open');
  focusables(drawer)[0]?.focus();
}
function closeDrawer() {
  if (!drawer || drawer.hidden) return;
  drawer.hidden = true;
  opener?.setAttribute('aria-expanded', 'false');
  document.body.classList.remove('drawer-open');
  (lastFocus ?? opener)?.focus();
}
opener?.addEventListener('click', openDrawer);
drawer?.querySelectorAll('[data-drawer-close]').forEach((el) => el.addEventListener('click', closeDrawer));
drawer?.addEventListener('keydown', (e) => {
  if (e.key !== 'Tab') return;
  const f = focusables(drawer);
  if (!f.length) return;
  const first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
});
// Close the drawer if the viewport grows into desktop layout.
window.matchMedia('(min-width: 1180px)').addEventListener('change', (mq) => { if (mq.matches) closeDrawer(); });

document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  const openMenu = menus.find((m) => m.querySelector('.nav-trigger')?.getAttribute('aria-expanded') === 'true');
  if (openMenu) { setMenu(openMenu, false); openMenu.querySelector<HTMLButtonElement>('.nav-trigger')?.focus(); }
  closeDrawer();
});
