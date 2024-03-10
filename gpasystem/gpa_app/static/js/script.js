document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.getElementById('sidebar-wrapper');
    var collapsibles = sidebar.querySelectorAll('.collapse');
    console.log("collapse")

    sidebar.addEventListener('show.bs.collapse', function(e) {
        collapsibles.forEach(function(collapsible) {
            if (collapsible !== e.target) {
                var collapseInstance = bootstrap.Collapse.getInstance(collapsible);
                if (collapseInstance) {
                    collapseInstance.hide();
                }
            }
        });
    });
});
