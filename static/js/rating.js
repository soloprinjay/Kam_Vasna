// WebSocket connection
const ratingSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/rating/' + postId + '/'
);

ratingSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Received WebSocket message:', data);
    
    if (data.type === 'rating_update') {
        const ratingData = data.rating;
        console.log('Rating data:', ratingData);
        
        if (ratingData.error) {
            console.error('Error:', ratingData.error);
            return;
        }
        
        // Update the rating display
        const averageRating = ratingData.average;
        const ratingCount = ratingData.count;
        const userRating = ratingData.user_rating;
        
        // Update average rating display
        const averageRatingElement = document.getElementById('average-rating');
        if (averageRatingElement) {
            averageRatingElement.textContent = averageRating.toFixed(1);
        }
        
        // Update rating count
        const ratingCountElement = document.getElementById('rating-count');
        if (ratingCountElement) {
            ratingCountElement.textContent = ratingCount;
        }
        
        // Update user's rating stars
        const userRatingStars = document.querySelectorAll('.user-rating-star');
        userRatingStars.forEach((star, index) => {
            if (index < userRating) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }
};

ratingSocket.onclose = function(e) {
    console.error('Rating socket closed unexpectedly');
};

// Function to send rating
function sendRating(rating) {
    const message = {
        'type': 'rating',
        'rating': rating,
        'user_id': userId
    };
    console.log('Sending rating:', message);
    ratingSocket.send(JSON.stringify(message));
}

// Add click event listeners to stars
document.querySelectorAll('.rating-star').forEach((star, index) => {
    star.addEventListener('click', () => {
        const rating = index + 1;
        sendRating(rating);
    });
}); 