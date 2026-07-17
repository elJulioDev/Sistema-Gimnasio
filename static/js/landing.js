function formatCurrencyCLP(value) {
    let strValue = String(value).trim();
    strValue = strValue.replace(/[.,]\d{1,2}$/, '');
    const cleanValue = strValue.replace(/[.,]/g, '');
    const finalNumber = parseInt(cleanValue, 10);
    return isNaN(finalNumber) ? '0' : finalNumber.toLocaleString('es-CL');
}

document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('siteHeader');
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const revealEls = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach((el) => observer.observe(el));

  // Cierra el menú mobile al elegir un link
  const navMenu = document.getElementById('navMenu');
  if (navMenu) {
    const collapseInstance = bootstrap.Collapse.getOrCreateInstance(navMenu, { toggle: false });
    navMenu.querySelectorAll('a.nav-link, .account-mobile a').forEach((link) => {
      link.addEventListener('click', () => collapseInstance.hide());
    });
  }

  document.querySelectorAll('.raw-price').forEach(el => {
      el.textContent = formatCurrencyCLP(el.textContent);
  });
});