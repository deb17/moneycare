var elements;
var windowHeight;

function init() {
  elements = document.querySelectorAll('.hidden');
  windowHeight = window.innerHeight;
}

function checkPosition() {
  for (var i = 0; i < elements.length; i++) {
    var element = elements[i];
    if (element.classList.contains('animate__animated')) continue;

    var positionFromTop = elements[i].getBoundingClientRect().top;
    if (positionFromTop - windowHeight <= -200) {
      element.classList.add('animate__animated');
      if (i%2 === 0) {
        element.classList.add('animate__slideInRight');
      } else {
        element.classList.add('animate__slideInLeft');
      }
      element.classList.remove('hidden');
    }
  }
}

window.addEventListener('scroll', checkPosition);
window.addEventListener('resize', init);

init();
checkPosition();
