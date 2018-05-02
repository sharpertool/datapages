(function() {
    var cards = document.querySelectorAll('.card.chart-card');

    console.log('Cards: ', cards);

    function expandHandler(e) {
        console.log('expand button clicked', e, this);
    }

    function shareHandler(e) {
        console.log('share button clicked', e, this);
    }

    function zoomHandler(e) {
        if (this.media.querySelector('.modal') === null) {
            var lightbox = createLightbox(this.media);
            this.media.appendChild(lightbox);
        }
        $(this.media.querySelector('.modal')).modal('show');
    }

    function drawHandler(e) {
        console.log('draw button clicked', e, this);
    }

    function downloadHandler(e) {
        console.log('download button clicked', e, this);
    }

    function createLightbox(media) {
        media = media.querySelector('iframe') || media.querySelector('img');
        media = media.cloneNode(true);
        media.setAttribute('height', '1100px');

        var lightbox = document.createElement('div');
        lightbox.setAttribute('class', 'modal fade');
        lightbox.setAttribute('tabindex', '-1');
        lightbox.setAttribute('role', 'dialog');
        lightbox.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-body">
                        ${media.outerHTML}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        `;

        return lightbox;
    }

    cards.forEach(function(item) {
        var media = item.querySelector('.media');
        var buttonShare = item.querySelector('.card-links > [data-action=share]');
        var buttonZoom = item.querySelector('.card-links > [data-action=zoom]');
        var buttonDownload = item.querySelector('.card-links > [data-action=download]');
        var buttonDraw = item.querySelector('.card-links > [data-action=draw]');
        var buttonExpand = item.querySelector('[data-action=expand]');

        // Registering click event to the control buttons
        buttonShare && buttonShare.addEventListener('click', shareHandler.bind({ media: media }));
        buttonZoom && buttonZoom.addEventListener('click', zoomHandler.bind({ media: media }));
        buttonDownload && buttonDownload.addEventListener('click', downloadHandler.bind({ media: media }));
        buttonDraw && buttonDraw.addEventListener('click', drawHandler.bind({ media: media }));
        buttonExpand && buttonExpand.addEventListener('click', expandHandler.bind({ media: media }));
    });
})()