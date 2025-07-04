// Message utility functions
function showMessage(message, type = 'info') {
    // Remove existing message container if any
    const existingContainer = document.getElementById('message-container');
    if (existingContainer) {
        existingContainer.remove();
    }

    // Create message container
    const messageContainer = document.createElement('div');
    messageContainer.id = 'message-container';
    messageContainer.className = 'fixed top-20 right-4 z-50 ml-3';
    messageContainer.style.display = 'block';

    // Create message box
    const messageBox = document.createElement('div');
    messageBox.id = 'message-box';
    messageBox.className = 'bg-white dark:bg-dark-card shadow-lg rounded-lg p-4 mb-4 transform transition-all duration-300 ease-in-out max-w-fit';
    messageBox.style.transform = 'translateX(100%)';
    messageBox.style.opacity = '0';

    // Determine icon and color based on message type
    let iconSvg = '';
    let iconColor = '';
    
    switch(type) {
        case 'success':
            iconColor = 'text-green-400';
            iconSvg = '<svg class="h-6 w-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>';
            break;
        case 'error':
            iconColor = 'text-red-400';
            iconSvg = '<svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
            break;
        default:
            iconColor = 'text-blue-400';
            iconSvg = '<svg class="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>';
    }

    // Create message content
    messageBox.innerHTML = `
        <div class="flex items-center">
            <div class="flex-shrink-0">
                ${iconSvg}
            </div>
            <div class="ml-3">
                <p class="text-sm font-medium text-gray-900 dark:text-dark-text">
                    ${message}
                </p>
            </div>
        </div>
    `;

    // Append message box to container
    messageContainer.appendChild(messageBox);
    document.body.appendChild(messageContainer);

    // Animate in
    setTimeout(() => {
        messageBox.style.transform = 'translateX(0)';
        messageBox.style.opacity = '1';
    }, 100);

    // Auto hide after 5 seconds
    setTimeout(() => {
        messageBox.style.transform = 'translateX(100%)';
        messageBox.style.opacity = '0';
        
        setTimeout(() => {
            if (messageContainer.parentNode) {
                messageContainer.remove();
            }
        }, 300);
    }, 5000);
}

// Convenience functions
function showSuccess(message) {
    showMessage(message, 'success');
}

function showError(message) {
    showMessage(message, 'error');
}

function showInfo(message) {
    showMessage(message, 'info');
} 