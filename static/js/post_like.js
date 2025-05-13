document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function () {
        const postId = this.dataset.postId;

        fetch(`/blog/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
            .then(res => res.json())
            .then(data => {
                if (data.liked) {
                    this.classList.add('liked');
                }
                this.querySelector('.like-count').textContent = data.likes;
            });
    });
});

function getCSRFToken() {
    let csrfToken = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return csrfToken || '{{ csrf_token }}';
}




// Star rating functionality

document.addEventListener('DOMContentLoaded', function () {
    const starRatings = document.querySelectorAll('.star-rating');

    starRatings.forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        let selectedRating = 0;

        stars.forEach((star, index) => {
            // Click event
            star.addEventListener('click', () => {
                selectedRating = index + 1;
                stars.forEach((s, i) => {
                    s.classList.toggle('active', i < selectedRating);
                });
            });

            // Hover events
            star.addEventListener('mouseenter', () => {
                stars.forEach((s, i) => {
                    s.classList.toggle('active', i <= index);
                });
            });

            star.addEventListener('mouseleave', () => {
                stars.forEach((s, i) => {
                    s.classList.toggle('active', i < selectedRating);
                });
            });
        });
    });
});
