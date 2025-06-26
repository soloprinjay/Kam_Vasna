 // Toggle menu dropdown (UI only)
    function toggleMenu(btn) {
        const dropdown = btn.parentNode.querySelector('.menu-dropdown');
        // Close all other dropdowns
        document.querySelectorAll('.menu-dropdown').forEach(function(menu) {
            if (menu !== dropdown) menu.classList.add('hidden');
        });
        // Toggle this dropdown
        dropdown.classList.toggle('hidden');
    }
    // Open share popup (UI only)
    function openSharePopupStatic(link) {
        document.getElementById('share-popup').classList.remove('hidden');
        document.getElementById('share-link-input').value = link || window.location.href;
        document.getElementById('copy-link-btn').textContent = 'Copy Link';
        // Close all dropdowns
        document.querySelectorAll('.menu-dropdown').forEach(function(menu) { menu.classList.add('hidden'); });
    }
    // Close share popup (UI only)
    function closeSharePopup() {
        document.getElementById('share-popup').classList.add('hidden');
    }
    window.addEventListener('DOMContentLoaded', function() {
        var copyBtn = document.getElementById('copy-link-btn');
        if (copyBtn) {
            copyBtn.onclick = function() {
                var input = document.getElementById('share-link-input');
                input.select();
                input.setSelectionRange(0, 99999); // For mobile devices
                document.execCommand('copy');
                this.textContent = 'Copied!';
                setTimeout(() => { this.textContent = 'Copy Link'; }, 1500);
            };
        }
    });