
    // Preview-Button Popover
    document.addEventListener('DOMContentLoaded', function () {
        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl, {
                trigger: 'click',
                html: true,
                title: 'Zusätzliche Informationen',
                content: 'Lade...'
            });
        });

        popoverTriggerList.forEach(function (popoverTriggerEl) {
            popoverTriggerEl.addEventListener('shown.bs.popover', function () {
                var docId = this.getAttribute('data-doc-id');
                fetch('/preview/' + docId)
                    .then(response => response.json())
                    .then(data => {
                        var popover = bootstrap.Popover.getInstance(this);
                        popover.setContent({
                            '.popover-body': 'Geladene Daten: ' + JSON.stringify(data)
                        });
                        popover.update();
                    })
                    .catch(error => {
                        console.error('Fehler beim Laden der Daten: ', error);
                    });
            });
        });
    });