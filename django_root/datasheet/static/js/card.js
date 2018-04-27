(function() {
    var card, canvas, container;

    card = document.querySelector('.card.chart-card');

    canvas = document.createElement('canvas');
    canvas.setAttribute('height', '500px');
    canvas.setAttribute('width', '100%');

    container = card.querySelector('.image');
    container.appendChild(canvas);

    fabric.Object.prototype.selectable = false;

    if(typeof G_vmlCanvasManager != 'undefined') {
        canvas = G_vmlCanvasManager.initElement(canvas);
    }

    canvas = this.__canvas = new fabric.Canvas(canvas, {
        isDrawingMode: false,
        width: container.offsetWidth,
        height: container.offsetHeight
    });

    canvas.freeDrawingBrush.width = 10;

    fabric.Image.fromURL('/media/images/2018-03-10_17-03-29.original.png', function(image) {
        image.set({
            scaleX: canvas.width / image.width,
            scaleY: canvas.height / image.height,
            width: canvas.width,
            height: canvas.height,
            originX: 'left',
            originY: 'top'
        });
       canvas.setBackgroundImage(image, canvas.renderAll.bind(canvas));
    });

    card.querySelector('[data-action=draw]')
        .addEventListener('click', function(e) {
            canvas.isDrawingMode = !this.classList.contains('active');
            this.classList.toggle('active');
        });
})()