// Enhanced Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInputs = document.querySelectorAll('input[name="q"]');
    const searchForm = document.querySelector('form[action*="search"]');
    
    // Search suggestions container
    let suggestionsContainer = null;
    
    // Create suggestions container
    function createSuggestionsContainer() {
        if (!suggestionsContainer) {
            suggestionsContainer = document.createElement('div');
            suggestionsContainer.className = 'search-suggestions absolute top-full left-0 right-0 bg-white dark:bg-dark-card border border-gray-200 dark:border-dark-border rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto hidden';
            document.body.appendChild(suggestionsContainer);
        }
        return suggestionsContainer;
    }
    
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Fetch search suggestions
    async function fetchSearchSuggestions(query) {
        if (!query || query.length < 2) return [];
        
        try {
            const response = await fetch(`/api/search/suggestions/?q=${encodeURIComponent(query)}`);
            if (response.ok) {
                const data = await response.json();
                return data.suggestions || [];
            }
        } catch (error) {
            console.error('Error fetching search suggestions:', error);
        }
        return [];
    }
    
    // Show search suggestions
    function showSuggestions(suggestions, input) {
        const container = createSuggestionsContainer();
        container.innerHTML = '';
        
        if (suggestions.length === 0) {
            container.classList.add('hidden');
            return;
        }
        
        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'suggestion-item px-4 py-3 hover:bg-orange-50 dark:hover:bg-dark-accent/10 cursor-pointer border-b border-gray-100 dark:border-dark-border last:border-b-0';
            
            const icon = document.createElement('i');
            icon.className = `fas ${suggestion.type === 'title' ? 'fa-book' : suggestion.type === 'category' ? 'fa-folder' : 'fa-tag'} text-orange-600 dark:text-dark-accent mr-3`;
            
            const text = document.createElement('span');
            text.className = 'text-gray-800 dark:text-dark-text';
            text.textContent = suggestion.text;
            
            item.appendChild(icon);
            item.appendChild(text);
            
            item.addEventListener('click', () => {
                input.value = suggestion.text;
                container.classList.add('hidden');
                input.focus();
                
                // Auto-submit form if it's a title suggestion
                if (suggestion.type === 'title') {
                    input.closest('form').submit();
                }
            });
            
            container.appendChild(item);
        });
        
        // Position the suggestions container
        const rect = input.getBoundingClientRect();
        container.style.position = 'fixed';
        container.style.top = `${rect.bottom + window.scrollY}px`;
        container.style.left = `${rect.left + window.scrollX}px`;
        container.style.width = `${rect.width}px`;
        container.style.maxHeight = '240px';
        
        container.classList.remove('hidden');
    }
    
    // Hide suggestions
    function hideSuggestions() {
        if (suggestionsContainer) {
            suggestionsContainer.classList.add('hidden');
        }
    }
    
    // Debounced search function
    const debouncedSearch = debounce(async (query, input) => {
        const suggestions = await fetchSearchSuggestions(query);
        showSuggestions(suggestions, input);
    }, 300);
    
    // Add event listeners to search inputs
    searchInputs.forEach(input => {
        // Input event for real-time suggestions
        input.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                debouncedSearch(query, input);
            } else {
                hideSuggestions();
            }
        });
        
        // Focus event
        input.addEventListener('focus', function(e) {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                debouncedSearch(query, input);
            }
        });
        
        // Blur event
        input.addEventListener('blur', function() {
            // Delay hiding to allow for clicks on suggestions
            setTimeout(hideSuggestions, 200);
        });
        
        // Keydown event for keyboard navigation
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                hideSuggestions();
                input.blur();
            }
        });
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-suggestions') && !e.target.closest('input[name="q"]')) {
            hideSuggestions();
        }
    });
    
    // Enhanced search form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = searchForm.querySelector('input[name="q"]');
            const query = searchInput.value.trim();
            
            if (!query) {
                e.preventDefault();
                searchInput.focus();
                return;
            }
            
            // Add loading state
            const submitButton = searchForm.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                submitButton.disabled = true;
                
                // Reset after a short delay
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 2000);
            }
        });
    }
    
    // Quick search functionality
    function setupQuickSearch() {
        const quickSearchButtons = document.querySelectorAll('[data-quick-search]');
        
        quickSearchButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const searchTerm = this.dataset.quickSearch;
                const searchInput = document.querySelector('input[name="q"]');
                
                if (searchInput) {
                    searchInput.value = searchTerm;
                    searchInput.closest('form').submit();
                }
            });
        });
    }
    
    // Initialize quick search
    setupQuickSearch();
    
    // Search history functionality
    function saveSearchHistory(query) {
        if (!query) return;
        
        let history = JSON.parse(localStorage.getItem('searchHistory') || '[]');
        history = history.filter(item => item !== query);
        history.unshift(query);
        history = history.slice(0, 10); // Keep only last 10 searches
        
        localStorage.setItem('searchHistory', JSON.stringify(history));
    }
    
    function getSearchHistory() {
        return JSON.parse(localStorage.getItem('searchHistory') || '[]');
    }
    
    // Show search history in suggestions
    function showSearchHistory(input) {
        const history = getSearchHistory();
        if (history.length === 0) return;
        
        const suggestions = history.map(query => ({
            type: 'history',
            text: query
        }));
        
        showSuggestions(suggestions, input);
    }
    
    // Add search history to suggestions
    searchInputs.forEach(input => {
        input.addEventListener('focus', function() {
            const query = this.value.trim();
            if (query.length === 0) {
                showSearchHistory(this);
            }
        });
    });
    
    // Save search history on form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            const searchInput = searchForm.querySelector('input[name="q"]');
            const query = searchInput.value.trim();
            saveSearchHistory(query);
        });
    }
});

// Search analytics (optional)
function trackSearch(query, results) {
    // You can implement analytics tracking here
    console.log(`Search performed: "${query}" - ${results} results`);
}

// Export functions for use in other scripts
window.SearchUtils = {
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    highlightSearchTerms: function(text, searchQuery) {
        if (!searchQuery) return text;
        
        const regex = new RegExp(`(${searchQuery})`, 'gi');
        return text.replace(regex, '<mark class="bg-yellow-200 dark:bg-yellow-800">$1</mark>');
    }
}; 