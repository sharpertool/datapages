(function(w, d) {

    var print_button = d.getElementById('print');

    print_button.addEventListener('click', function(e) {
        w.print();
    });
})(window, document);
