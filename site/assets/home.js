/* Kerd homepage: pick a seat on the hall plan, and light the small plan for the
   story passage in view. No libraries. Without it the page still reads: the
   conductor's card shows, seat links jump to their cards, and the small plan is
   lit for the first passage. */
(function () {
  document.documentElement.classList.add('js');

  var hall = document.getElementById('hall');
  if (hall) {
    var start = /^#seat-([a-z]+)$/.exec(location.hash);
    if (start && hall.querySelector('a.seat[data-seat="' + start[1] + '"]')) {
      hall.setAttribute('data-on', start[1]);
    }
    /* With JS the picked seat decides; a #seat-… link only sets the first
       pick, so its :target no longer pins that card (see home.css). */
    hall.classList.add('live');
    hall.querySelectorAll('a.seat').forEach(function (a) {
      var key = a.getAttribute('data-seat');
      function pick() { hall.setAttribute('data-on', key); }
      a.addEventListener('mouseenter', pick);
      a.addEventListener('focus', pick);
      a.addEventListener('click', function (e) { e.preventDefault(); pick(); });
    });
  }

  var mini = document.getElementById('mini');
  var cap = document.getElementById('mini-cap');
  var beats = Array.prototype.slice.call(document.querySelectorAll('.beat'));
  if (mini && cap && beats.length) {
    var light = function (b) {
      beats.forEach(function (x) { x.classList.toggle('is-on', x === b); });
      mini.setAttribute('data-lit', b.getAttribute('data-lit'));
      cap.textContent = b.querySelector('.direction').textContent;
    };
    beats.forEach(function (b) { b.addEventListener('click', function () { light(b); }); });
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) light(e.target); });
      }, { rootMargin: '-40% 0px -55% 0px' });
      beats.forEach(function (b) { io.observe(b); });
    }
    light(beats[0]);
  }

  var sc = document.querySelector('.plan-scroll');
  if (sc && sc.scrollWidth > sc.clientWidth) sc.scrollLeft = (sc.scrollWidth - sc.clientWidth) / 2;
})();
