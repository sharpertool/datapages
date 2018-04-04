(function(w, d) {

    var _target = '.card-carousel-indicator';
    var indicator = document.querySelector(_target);
    var _list = indicator.children;

    for( var k of _list) {
        k.addEventListener('click', function(e) {
            var siblings = e.target.parentNode.children;

            for(var s of siblings) {
                s.classList.remove('active');
            }

            e.target.classList.add('active');

        });
    }

})(window, document);
