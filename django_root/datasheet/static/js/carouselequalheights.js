(function(w, d) {

    var carousel_item = document.querySelectorAll('.carousel-item');
    var heights = [],
    tallest;
    carousel_item.forEach(function(value, key) {
        heights.push(value.offsetHeight)
    });

    tallest = Math.max.apply(null, heights); //cache largest value

    carousel_item.forEach(function(value, key) {
        value.style.height = tallest + 'px'
    });

})(window, document);
