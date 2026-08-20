/* =========================================================
   ONE MORE TAKE FILMS — interactions
   ========================================================= */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Preloader ----------------------------------------
     Fixed-length countdown, never gated on image loading — the page
     stays interactive even if a photo is slow or missing. */
  var loader = document.getElementById('loader');
  var counts = loader ? loader.querySelectorAll('.loader__count span') : [];

  function finishLoader() {
    if (!loader) return;
    loader.classList.add('done');
    document.body.style.overflow = '';
    setTimeout(function () {
      if (loader.parentNode) loader.parentNode.removeChild(loader);
    }, 700);
  }

  if (loader) {
    if (reduced) {
      finishLoader();
    } else {
      document.body.style.overflow = 'hidden';
      var i = 0;
      var tick = setInterval(function () {
        if (counts[i]) counts[i].classList.add('on');
        i++;
        if (i >= counts.length) {
          clearInterval(tick);
          setTimeout(finishLoader, 380);
        }
      }, 340);
      setTimeout(finishLoader, 4000);   // safety net
    }
  }

  /* ---------- 2. Sticky nav + mobile menu -------------------------- */
  var nav = document.getElementById('nav');
  var burger = document.getElementById('burger');
  var navLinks = document.getElementById('navLinks');

  window.addEventListener('scroll', function () {
    if (nav) nav.classList.toggle('stuck', window.scrollY > 40);
  }, { passive: true });

  if (burger && navLinks) {
    burger.addEventListener('click', function () {
      var open = navLinks.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    Array.prototype.forEach.call(navLinks.querySelectorAll('a'), function (a) {
      a.addEventListener('click', function () {
        navLinks.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* ---------- 3. Scroll reveal ------------------------------------- */
  var revealables = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var siblings = Array.prototype.slice.call(
          e.target.parentNode.querySelectorAll(':scope > .reveal')
        );
        var idx = Math.max(0, siblings.indexOf(e.target));
        e.target.style.transitionDelay = Math.min(idx * 70, 420) + 'ms';
        e.target.classList.add('in');
        io.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    Array.prototype.forEach.call(revealables, function (el) { io.observe(el); });
  } else {
    Array.prototype.forEach.call(revealables, function (el) { el.classList.add('in'); });
  }

  /* ---------- 4. Parallax ------------------------------------------ */
  var parallaxEls = document.querySelectorAll('[data-parallax]');
  var ticking = false;

  function parallax() {
    var vh = window.innerHeight;
    Array.prototype.forEach.call(parallaxEls, function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.bottom < -200 || rect.top > vh + 200) return;
      var speed = parseFloat(el.getAttribute('data-parallax')) || 0.1;
      var offset = (rect.top + rect.height / 2 - vh / 2) * speed;
      el.style.transform = 'translate3d(0,' + offset.toFixed(1) + 'px,0)';
    });
    ticking = false;
  }

  if (!reduced && parallaxEls.length) {
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(parallax); ticking = true; }
    }, { passive: true });
    parallax();
  }

  /* ---------- 5. Work filter --------------------------------------- */
  var chips = document.querySelectorAll('.chip');
  var cards = document.querySelectorAll('#grid .card');

  Array.prototype.forEach.call(chips, function (chip) {
    chip.addEventListener('click', function () {
      Array.prototype.forEach.call(chips, function (c) { c.classList.remove('is-on'); });
      chip.classList.add('is-on');
      var f = chip.getAttribute('data-filter');
      Array.prototype.forEach.call(cards, function (card) {
        var match = f === 'all' || card.getAttribute('data-cat') === f;
        card.classList.toggle('hide', !match);
      });
    });
  });

  /* ---------- 6. Custom cursor (fine pointers only) ---------------- */
  var cursor = document.getElementById('cursor');
  var fine = window.matchMedia('(pointer: fine)').matches;

  if (cursor && fine && !reduced) {
    var cx = 0, cy = 0, tx = 0, ty = 0;

    document.addEventListener('mousemove', function (e) {
      tx = e.clientX; ty = e.clientY;
      cursor.classList.add('on');
    });

    (function loop() {
      cx += (tx - cx) * 0.18;
      cy += (ty - cy) * 0.18;
      cursor.style.transform = 'translate3d(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px,0)';
      requestAnimationFrame(loop);
    })();

    var hot = document.querySelectorAll('a,button,.card,.art__item,.svc__row');
    Array.prototype.forEach.call(hot, function (el) {
      el.addEventListener('mouseenter', function () { cursor.classList.add('grow'); });
      el.addEventListener('mouseleave', function () { cursor.classList.remove('grow'); });
    });
  }

  /* ---------- 7. Footer year --------------------------------------- */
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

})();
