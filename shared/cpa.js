// CPA · toggle de tema (claro/escuro)
// O bootstrap síncrono (que evita FOUC lendo localStorage antes do paint)
// fica inline no <head> de cada página. Este script só interpreta o clique
// no botão #theme-toggle quando o DOM já carregou.

(function () {
  var btn = document.getElementById('theme-toggle');
  if (!btn) return;
  var html = document.documentElement;

  function apply(theme) {
    html.dataset.theme = theme;
    localStorage.setItem('cpa-theme', theme);
    if (theme === 'dark') {
      btn.textContent = '◐ tema claro';
      btn.setAttribute('aria-label', 'Mudar para tema claro');
    } else {
      btn.textContent = '◑ tema escuro';
      btn.setAttribute('aria-label', 'Mudar para tema escuro');
    }
  }

  apply(html.dataset.theme || 'light');

  btn.addEventListener('click', function () {
    apply(html.dataset.theme === 'dark' ? 'light' : 'dark');
  });
}());
