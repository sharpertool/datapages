(function($, claraplayer, superagent) {
    var card = $('.block.embed-3d > .chart-card.card');
    var buttonZoom = card.find('.card-links > [data-action=zoom]');
    var buttonDownload = card.find('.card-links > [data-action=download]');
    var media = card.find('.card-body > .media');

    buttonZoom && buttonZoom.on('click', zoomHandler);
    buttonDownload && buttonDownload.on('click', downloadHandler);

    if (media.length && media.find('> .embed').length) {
        initializeClara(media.find('> .embed'));
    }

    function downloadHandler (e) {
        var uuid = $(this).data('uuid');

        document.body.style.cursor = "wait"

        superagent.get(`/clara/download/${uuid}`)
            .responseType('blob')
            .then(function (response) {
                document.body.style.cursor = "default"

                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(response.body);
                link.download = `${new Date().getTime()}.zip`
                document.body.appendChild(link)
                link.click()
                document.body.removeChild(link)
            })
            .catch(function (errors) {
                console.log(errors)
            })
    }

    function zoomHandler () {
        if (!media.find('.modal').length) {
            var lightbox = createLightbox(media);

            // Register lightbox shown event
            lightbox.on('shown.bs.modal', function (e) {
                initializeClara(lightbox.find('.embed'));
            });

            media.append(lightbox);
        }

        media.find('.modal').modal('show');
    }

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
})($, claraplayer, superagent);