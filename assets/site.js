'use strict';
const current = decodeURIComponent(location.pathname.split('/').pop() || 'index.html');
for (const link of document.querySelectorAll('nav a')) {
  if (decodeURIComponent(link.getAttribute('href')) === current) link.setAttribute('aria-current', 'page');
}
