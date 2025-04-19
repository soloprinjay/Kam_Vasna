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

