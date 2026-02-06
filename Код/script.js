// Simple counter tracker with localStorage persistence
// - Immediate reset (no confirmation)
// - Small "pop" animation on value change

(function () {
  'use strict';

  const STORAGE_KEY = 'counterValue_v1';
  const DEFAULT_VALUE = 0;

  const counterEl = document.getElementById('counter');
  const incrementBtn = document.getElementById('increment');
  const resetBtn = document.getElementById('reset');

  let value = DEFAULT_VALUE;

  // Safe localStorage helpers (handles browsers that block access)
  function safeGet(key) {
    try {
      return localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }

  function safeSet(key, val) {
    try {
      localStorage.setItem(key, String(val));
    } catch (e) {
      // ignore write errors (private modes)
    }
  }

  function loadValue() {
    const raw = safeGet(STORAGE_KEY);
    if (raw === null) return DEFAULT_VALUE;
    const parsed = parseInt(raw, 10);
    return Number.isFinite(parsed) ? parsed : DEFAULT_VALUE;
  }

  function saveValue(v) {
    safeSet(STORAGE_KEY, v);
  }

  function render() {
    counterEl.textContent = String(value);
    // Toggle reset button style when not zero
    if (value !== 0) {
      resetBtn.classList.add('danger');
    } else {
      resetBtn.classList.remove('danger');
    }
  }

  // small pop animation on change
  function animatePop() {
    counterEl.classList.remove('pop');
    // force reflow to restart the animation
    void counterEl.offsetWidth;
    counterEl.classList.add('pop');
    // cleanup after animation (in case it doesn't fire)
    clearTimeout(counterEl._popTimeout);
    counterEl._popTimeout = setTimeout(() => counterEl.classList.remove('pop'), 400);
  }

  // Actions
  function increment() {
    value = value + 1;
    render();
    animatePop();
    saveValue(value);
  }

  function reset() {
    value = DEFAULT_VALUE;
    render();
    animatePop();
    saveValue(value);
  }

  // Initialize
  function init() {
    value = loadValue();
    render();

    incrementBtn.addEventListener('click', increment);
    resetBtn.addEventListener('click', function () {
      // Reset immediately (no confirmation)
      if (value === 0) return;
      reset();
    });

    // Accessibility: keyboard shortcuts: I to increment, R to reset
    document.addEventListener('keydown', function (e) {
      const tag = (e.target && e.target.tagName) || '';
      // ignore typing in inputs
      if (tag === 'INPUT' || tag === 'TEXTAREA' || e.metaKey || e.ctrlKey) return;

      if (e.key === 'I' || e.key === 'i') {
        increment();
      } else if (e.key === 'R' || e.key === 'r') {
        if (value !== 0) reset();
      }
    });
  }

  // Run init when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();