(function () {
  var toggler = document.getElementById('navToggler');
  var sidebar = document.getElementById('mobileSidebar');
  var backdrop = document.getElementById('mobileSidebarBackdrop');
  var closeBtn = document.getElementById('mobileSidebarClose');
  if (!toggler || !sidebar || !backdrop) return;

  function openSidebar() {
    sidebar.classList.add('is-open');
    backdrop.classList.add('is-open');
    document.body.classList.add('no-scroll');
    toggler.setAttribute('aria-expanded', 'true');
    sidebar.setAttribute('aria-hidden', 'false');
  }
  function closeSidebar() {
    sidebar.classList.remove('is-open');
    backdrop.classList.remove('is-open');
    document.body.classList.remove('no-scroll');
    toggler.setAttribute('aria-expanded', 'false');
    sidebar.setAttribute('aria-hidden', 'true');
  }

  toggler.addEventListener('click', function () {
    sidebar.classList.contains('is-open') ? closeSidebar() : openSidebar();
  });
  closeBtn.addEventListener('click', closeSidebar);
  backdrop.addEventListener('click', closeSidebar);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeSidebar();
  });
  sidebar.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', closeSidebar);
  });
  window.addEventListener('resize', function () {
    if (window.innerWidth >= 992) closeSidebar();
  });
})();