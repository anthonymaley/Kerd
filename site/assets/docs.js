/* Kerd docs page. On a phone the hall plan is wider than its frame and scrolls
   sideways; open it centred on the stage, as the homepage does. Without this
   the plan opens at its left wall and still scrolls. */
(function () {
  var sc = document.querySelector('.index .plan-scroll');
  if (sc && sc.scrollWidth > sc.clientWidth) sc.scrollLeft = (sc.scrollWidth - sc.clientWidth) / 2;
})();
