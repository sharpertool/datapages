(function($, claraplayer) {
    var cards = $('.card.chart-card');

    function zoomHandler () {
        if (!this.media.find('.modal').length) {
            var lightbox = createLightbox(this.media);

            // Register lightbox shown event
            lightbox.on('shown.bs.modal', function (e) {
                initializeClara(lightbox.find('.embed'));
            });

            this.media.append(lightbox);
        }

        this.media.find('.modal').modal('show');
    }

    function drawHandler () {
        console.log('draw button clicked');
    }

    function downloadHandler () {
        console.log('download button clicked');
    }

    function shareHandler () {
        console.log('share button clicked');
    }

    function expandHandler () {
        console.log('expand button clicked');
    }

    $.each(cards, function () {
        var media = $(this).find('.card-body > .media');
        var buttonZoom = $(this).find('.card-links > [data-action=zoom]');
        var buttonDraw = $(this).find('.card-links > [data-action=draw]');
        var buttonDownload = $(this).find('.card-links > [data-action=download]');
        var buttonShare = $(this).find('.card-links > [data-action=share]');
        var buttonExpand = $(this).find('[data-action=expand]');

        buttonZoom && buttonZoom.on('click', zoomHandler.bind({ media: media }));
        buttonDraw && buttonDraw.on('click', drawHandler.bind({ media: media }));
        buttonDownload && buttonDownload.on('click', downloadHandler.bind({ media: media }));
        buttonShare && buttonShare.on('click', shareHandler.bind({ media: media }));
        buttonExpand && buttonExpand.on('click', expandHandler.bind({ media: media }));

        if (media.length && media.find('> .embed').length) {
            initializeClara(media.find('> .embed'));
        }
    });

    function initializeClara (container) {
        var clara = claraplayer(container[0]);
        var uuid = container.data('uuid');

        clara.scene.filter({ type: 'camera' });

        clara.on('loaded', function () {
           console.log('Clara player is loaded and ready');
        });

        clara.sceneIO.fetchAndUse(uuid).then(function () {
           console.log('scene:', uuid, 'has been loaded');
        }).catch(function (error) {
            console.log('There was an error loading:', uuid)
        });
    }

    function createLightbox (container) {
        var uuid = container.find('> .embed').data('uuid');
        
        return $('<div></div>').addClass('modal fade')
            .attr({ tabindex: '-1', role: 'dialog' })
            .append(`
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-body">
                            <div class="embed"
                                 style="width: 100%; height: 900px;background: lightgray;"
                                 data-uuid="${uuid}"></div>
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            `);
    }
})($, claraplayer);