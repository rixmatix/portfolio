/* ==========================================================================
   SITE.JS — the only JavaScript on this site. No frameworks, no build step.

   1. Mode toggle: switches between "ds" (dark, design systems — default)
      and "gen" (light, generalist). Saves the choice to sessionStorage, so
      it lasts for the tab session only — every new visit opens in "ds".
      Note: a tiny inline script in each page <head> applies the saved mode
      BEFORE first paint so there's no color flash.
   2. Token readout: prints the site's LIVE CSS custom properties into the
      footer. Not hardcoded — change tokens.css and the footer updates.
   3. Case study scrollspy: highlights the sticky sub-nav link for the
      section currently in view.
   4. Scrollytelling: maps scroll progress to the current step.
   5. Carousels: prev/next buttons scroll the track.
   6. Parallax gallery fallback: only for browsers without CSS scroll-driven
      animations (animation-timeline: view()); otherwise CSS does it all.
   7. Grid overlay: press "G" to toggle an 8px grid.
   ========================================================================== */

(function () {
  var root = document.documentElement;

  // ---- 1. Mode toggle -----------------------------------------------------
  function setMode(mode) {
    if (mode === "gen") { root.setAttribute("data-mode", "gen"); }
    else { root.removeAttribute("data-mode"); mode = "ds"; }
    try { sessionStorage.setItem("mode", mode); } catch (e) {}
    document.querySelectorAll(".mode-toggle button").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.dataset.mode === mode ? "true" : "false");
    });
    renderTokens(); // footer readout reflects the active mode's values
  }
  document.querySelectorAll(".mode-toggle button").forEach(function (btn) {
    btn.addEventListener("click", function () { setMode(btn.dataset.mode); });
  });
  // sync buttons with whatever the inline head script applied
  setModeButtons();
  function setModeButtons() {
    var current = root.getAttribute("data-mode") === "gen" ? "gen" : "ds";
    document.querySelectorAll(".mode-toggle button").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.dataset.mode === current ? "true" : "false");
    });
  }

  // ---- 2. Token readout ----------------------------------------------------
  function renderTokens() {
    var readout = document.querySelector("[data-token-readout]");
    if (!readout) return;
    var tokens = [
      "--bg-canvas", "--bg-raised", "--fg-primary", "--fg-secondary",
      "--fg-accent", "--border-hairline", "--text-display", "--text-technical",
      "--scale-300", "--space-4", "--radius-2"
    ];
    var styles = getComputedStyle(root);
    var lines = [
      '<span class="t-comment">/* live values, read from tokens.css at runtime.</span>',
      '<span class="t-comment">   switch modes — the semantic layer remaps. */</span>',
      ":root {"
    ];
    tokens.forEach(function (t) {
      var v = styles.getPropertyValue(t).trim();
      if (v.indexOf(",") > -1 && v.indexOf("(") === -1) v = v.split(",")[0];
      lines.push('  <span class="t-name">' + t + '</span>: <span class="t-value">' + v + "</span>;");
    });
    lines.push("}");
    readout.innerHTML = lines.join("\n");
  }
  renderTokens();

  // ---- 3. Case study scrollspy ----------------------------------------------
  var subnavLinks = document.querySelectorAll(".case-subnav a[href^='#']");
  if (subnavLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    subnavLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          subnavLinks.forEach(function (a) { a.classList.remove("is-active"); });
          var link = byId[entry.target.id];
          if (link) {
            link.classList.add("is-active");
            link.scrollIntoView({ block: "nearest", inline: "nearest" });
          }
        }
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) observer.observe(el);
    });
  }

  // ---- 4. Scrollytelling sections ---------------------------------------------
  // Maps scroll progress through a [data-scrolly] block to its current step.
  // Only active at >=900px; below that, CSS lays the steps out statically.
  var scrollyMQ = window.matchMedia("(min-width: 900px)");
  document.querySelectorAll("[data-scrolly]").forEach(function (sc) {
    var copySteps = sc.querySelectorAll(".scrolly__copy .scrolly-step");
    var mediaSteps = sc.querySelectorAll(".scrolly__media .scrolly-step");
    var builds = sc.querySelectorAll("[data-build]");   // token stack layers (layout/16)
    var n = copySteps.length;
    if (!n) return;
    var current = -1, ticking = false;

    function setStep(i) {
      if (i === current) return;
      current = i;
      copySteps.forEach(function (el, k) { el.classList.toggle("is-current", k === i); });
      mediaSteps.forEach(function (el, k) { el.classList.toggle("is-current", k === i); });
      // cumulative layers: everything at or below the current step stays built
      builds.forEach(function (el) {
        var k = +el.getAttribute("data-build");
        el.classList.toggle("is-built", k <= i);
        el.classList.toggle("is-current", k === i);
      });
    }
    function update() {
      ticking = false;
      if (!scrollyMQ.matches) return;
      var rect = sc.getBoundingClientRect();
      var total = rect.height - window.innerHeight;
      if (total <= 0) { setStep(0); return; }
      var progress = Math.min(0.999, Math.max(0, -rect.top / total));
      setStep(Math.min(n - 1, Math.floor(progress * n)));
    }
    function onScroll() {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    update();
  });

  // ---- 5. Carousels -------------------------------------------------------------
  document.querySelectorAll("[data-carousel]").forEach(function (c) {
    var track = c.querySelector(".carousel__track");
    if (!track) return;
    function stepWidth() {
      var slide = track.querySelector(".carousel__slide");
      return slide ? slide.getBoundingClientRect().width + 24 : 320;
    }
    var prev = c.querySelector(".carousel__btn--prev");
    var next = c.querySelector(".carousel__btn--next");
    if (prev) prev.addEventListener("click", function () { track.scrollBy({ left: -stepWidth(), behavior: "smooth" }); });
    if (next) next.addEventListener("click", function () { track.scrollBy({ left: stepWidth(), behavior: "smooth" }); });
  });

  // ---- 6. Parallax gallery fallback (layout/15) ------------------------------------
  // Same math as the CSS keyframes in main.css: while a frame crosses the
  // viewport, a layer at --depth d is displaced by (d − 1) × passage. One
  // rAF-throttled scroll listener per frame, attached only while it's on screen.
  var parallaxFrames = document.querySelectorAll(".parallax__frame");
  if (parallaxFrames.length && !CSS.supports("animation-timeline: view()")) {
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    var parallaxMQ = window.matchMedia("(min-width: 768px)");
    parallaxFrames.forEach(function (frame) {
      var stage = frame.querySelector(".parallax__stage");
      var layers = Array.prototype.map.call(frame.querySelectorAll(".parallax__item"), function (el) {
        var cs = getComputedStyle(el);
        return {
          el: el,
          depth: parseFloat(cs.getPropertyValue("--depth")) || 1,
          driftX: parseFloat(cs.getPropertyValue("--drift-x")) || 0
        };
      });
      var onScreen = false, waiting = false;

      function update() {
        waiting = false;
        if (!onScreen) return;
        if (reduceMotion.matches || !parallaxMQ.matches) {
          layers.forEach(function (l) { l.el.style.transform = ""; });
          return;
        }
        var rect = frame.getBoundingClientRect();
        var vh = window.innerHeight;
        var passage = vh + stage.clientHeight;
        var progress = Math.min(1, Math.max(0, (vh - rect.top) / (vh + rect.height)));
        layers.forEach(function (l) {
          var x = l.driftX * stage.clientWidth * (progress - 0.5);
          var y = (l.depth - 1) * passage * (0.5 - progress);
          l.el.style.transform = "translate(" + x.toFixed(1) + "px, " + y.toFixed(1) + "px)";
        });
      }
      function onScroll() {
        if (!waiting) { waiting = true; requestAnimationFrame(update); }
      }
      new IntersectionObserver(function (entries) {
        onScreen = entries[0].isIntersecting;
        if (onScreen) { window.addEventListener("scroll", onScroll, { passive: true }); update(); }
        else { window.removeEventListener("scroll", onScroll); }
      }).observe(frame);
      window.addEventListener("resize", onScroll, { passive: true });
    });
  }

  // ---- 7. Grid overlay (press G) ----------------------------------------------
  var overlay = document.querySelector(".grid-overlay");
  if (overlay) {
    document.addEventListener("keydown", function (e) {
      var tag = (e.target.tagName || "").toLowerCase();
      if (tag === "input" || tag === "textarea" || e.metaKey || e.ctrlKey) return;
      if (e.key === "g" || e.key === "G") overlay.classList.toggle("is-visible");
    });
  }
})();
