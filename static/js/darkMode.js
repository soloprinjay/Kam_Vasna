// Function to initialize theme based on user preference or system setting
function initializeTheme() {
    // Check if theme is stored in localStorage
    const savedTheme = localStorage.getItem('theme');
    const htmlElement = document.documentElement;

    console.log('Initializing theme. Saved theme:', savedTheme);

    if (savedTheme) {
        // Apply saved theme
        htmlElement.classList.remove('light', 'dark');
        htmlElement.classList.add(savedTheme);
        console.log('Applied saved theme:', savedTheme);
    } else {
        // Check system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const defaultTheme = prefersDark ? 'dark' : 'light';
        htmlElement.classList.remove('light', 'dark');
        htmlElement.classList.add(defaultTheme);
        localStorage.setItem('theme', defaultTheme);
        console.log('Applied system preference theme:', defaultTheme);
    }

    // Update icons based on theme
    updateIcons();
}

// Function to update icons based on current theme
function updateIcons() {
    const isDark = document.documentElement.classList.contains('dark');
    const moonIcons = document.querySelectorAll('.theme-icon-moon');
    const sunIcons = document.querySelectorAll('.theme-icon-sun');

    moonIcons.forEach(icon => {
        if (isDark) {
            icon.classList.add('hidden');
        } else {
            icon.classList.remove('hidden');
        }
    });

    sunIcons.forEach(icon => {
        if (isDark) {
            icon.classList.remove('hidden');
        } else {
            icon.classList.add('hidden');
        }
    });

    console.log('Updated icons. Dark mode is:', isDark);
}

// Function to toggle between dark and light mode
function toggleDarkMode() {
    const htmlElement = document.documentElement;
    const isDark = htmlElement.classList.contains('dark');
    
    console.log('Toggling theme. Current isDark:', isDark);

    // Toggle theme
    htmlElement.classList.remove('light', 'dark');
    const newTheme = isDark ? 'light' : 'dark';
    htmlElement.classList.add(newTheme);
    
    // Save preference
    localStorage.setItem('theme', newTheme);
    console.log('Set new theme:', newTheme);

    // Update icons
    updateIcons();
}

// Add click event listeners to buttons
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded');
    
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const darkModeToggleMobile = document.getElementById('dark-mode-toggle-mobile');

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
        console.log('Added click event listener to desktop dark mode toggle');
    }

    if (darkModeToggleMobile) {
        darkModeToggleMobile.addEventListener('click', toggleDarkMode);
        console.log('Added click event listener to mobile dark mode toggle');
    }

    // Initialize theme
    initializeTheme();
}); 