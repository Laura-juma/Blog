document.addEventListener('DOMContentLoaded', function() {

    // Mobile menu toggle
    var nav = document.getElementById('mainNav');
    var toggle = nav && nav.querySelector('.nav-toggle');
    if (toggle) {
        toggle.addEventListener('click', function() {
            var open = nav.classList.toggle('open');
            toggle.setAttribute('aria-expanded', open);
        });
    }

    // Dismissable flash messages
    document.querySelectorAll('[data-dismiss]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            btn.closest('.message').remove();
        });
    });

});
