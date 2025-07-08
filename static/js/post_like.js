document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function () {
        if (this.classList.contains('liked')) {
            // Already liked, do nothing
            return;
        }
        const postId = this.dataset.postId;

        fetch(`/blog/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
            .then(res => {
                if (res.status === 401) {
                    window.location = '/users/login/';
                    return null;
                }
                return res.json();
            })
            .then(data => {
                if (!data) return;
                if (data.liked) {
                    this.classList.add('liked');
                    this.disabled = true;
                }
                this.querySelector('.like-count').textContent = data.likes;
                if (data.error === 'Already liked') {
                    this.classList.add('liked');
                    this.disabled = true;
                }
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
