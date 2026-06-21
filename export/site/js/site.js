/* ─── Agentic Developer Craftsmanship — Site JavaScript ──────────── */

(function () {

  // ── Sidebar toggle ──────────────────────────────────────────────
  const sidebar = document.getElementById('sidebar');
  const menuBtn = document.getElementById('menu-btn');
  const sidebarToggle = document.getElementById('sidebar-toggle');

  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
  }

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.remove('open');
    });
  }

  // Close sidebar when clicking outside (mobile)
  document.addEventListener('click', function (e) {
    if (window.innerWidth <= 768) {
      if (!sidebar.contains(e.target) && e.target !== menuBtn) {
        sidebar.classList.remove('open');
      }
    }
  });

  // ── Active link highlighting on scroll ──────────────────────────
  const tocLinks = document.querySelectorAll('.sidebar-nav .toc-chapter a, .sidebar-nav .toc-sub a');
  const sections = [];

  tocLinks.forEach(function (link) {
    var href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      var section = document.getElementById(href.slice(1));
      if (section) {
        sections.push({ el: section, link: link });
      }
    }
  });

  function updateActiveLink() {
    var scrollPos = window.scrollY + 120;
    var activeId = null;

    for (var i = sections.length - 1; i >= 0; i--) {
      if (sections[i].el.offsetTop <= scrollPos) {
        activeId = i;
        break;
      }
    }

    tocLinks.forEach(function (link) {
      link.classList.remove('active');
    });

    if (activeId !== null) {
      sections[activeId].link.classList.add('active');
    }
  }

  window.addEventListener('scroll', updateActiveLink);
  window.addEventListener('load', updateActiveLink);

  // ── Smooth scroll for TOC links ─────────────────────────────────
  tocLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      var href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        e.preventDefault();
        var target = document.getElementById(href.slice(1));
        if (target) {
          var offset = 20;
          var top = target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top: top, behavior: 'smooth' });

          // Close sidebar on mobile
          if (window.innerWidth <= 768) {
            sidebar.classList.remove('open');
          }
        }
      }
    });
  });

  // ── Copy button for code blocks ────────────────────────────────
  document.querySelectorAll('pre > code').forEach(function (codeBlock) {
    var pre = codeBlock.parentElement;
    var wrapper = document.createElement('div');
    wrapper.className = 'code-block-wrapper';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.setAttribute('aria-label', 'Copier le code');
    wrapper.appendChild(btn);

    btn.addEventListener('click', function () {
      var text = codeBlock.textContent;
      navigator.clipboard.writeText(text).then(function () {
        btn.classList.add('copied');
        btn.setAttribute('aria-label', 'Copié !');
        setTimeout(function () {
          btn.classList.remove('copied');
          btn.setAttribute('aria-label', 'Copier le code');
        }, 2000);
      });
    });
  });

})();
