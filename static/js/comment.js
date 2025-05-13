// document.addEventListener('DOMContentLoaded', function () {
//     const commentForm = document.getElementById('comment-form');
//     const commentBody = document.getElementById('comment-body');
//     const parentIdInput = document.getElementById('parent_id');
//     const commentsContainer = document.getElementById('comments-container');
//     const commentCount = document.getElementById('comment-count');
//
//     let socket = null;
//     let reconnectAttempts = 0;
//     const maxReconnectAttempts = 5;
//
//     function connectWebSocket() {
//         const storyId = document.getElementById("comment-data").dataset.storyId;
//         const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
//         const ws_path = `${ws_scheme}://${window.location.host}/ws/comments/${storyId}/`;
//         console.log('Connecting to WebSocket:', ws_path);
//
//         try {
//             socket = new WebSocket(ws_path);
//
//             socket.onopen = function (e) {
//                 console.log('WebSocket connection established');
//                 reconnectAttempts = 0;
//             };
//
//             socket.onmessage = function (e) {
//                 console.log('Received message:', e.data);
//                 const data = JSON.parse(e.data);
//                 addCommentToDOM(data);
//                 updateCommentCount();
//             };
//
//             socket.onclose = function (e) {
//                 console.log('WebSocket connection closed:', e.code, e.reason);
//                 if (reconnectAttempts < maxReconnectAttempts) {
//                     reconnectAttempts++;
//                     console.log(`Attempting to reconnect (${reconnectAttempts}/${maxReconnectAttempts})...`);
//                     setTimeout(connectWebSocket, 3000);
//                 } else {
//                     console.error('Max reconnection attempts reached');
//                 }
//             };
//
//             socket.onerror = function (err) {
//                 console.error('WebSocket error:', err);
//             };
//         } catch (err) {
//             console.error('Error creating WebSocket:', err);
//         }
//     }
//
//     // Initial connection
//     connectWebSocket();
//
//     // Handle comment form submission
//     commentForm.addEventListener('submit', function (e) {
//         e.preventDefault();
//
//         if (!socket || socket.readyState !== WebSocket.OPEN) {
//             console.error('WebSocket not connected. Current state:', socket ? socket.readyState : 'null');
//             alert('Connection lost. Please refresh the page.');
//             return;
//         }
//
//         const commentDataDiv = document.getElementById('comment-data');
//         const userId = commentDataDiv.dataset.userId;
//
//         const formData = {
//             action: 'new_comment',
//             body: commentBody.value,
//             user_id: userId,
//             parent_id: parentIdInput.value || null
//         };
//
//         console.log('Sending comment:', formData);
//         socket.send(JSON.stringify(formData));
//         commentBody.value = '';
//         parentIdInput.value = '';
//         commentBody.placeholder = "अपनी टिप्पणी लिखें...";
//     });
//
//     // Handle reply buttons
//     document.querySelectorAll('.reply-btn').forEach(button => {
//         button.addEventListener('click', function () {
//             const commentId = this.dataset.commentId;
//             parentIdInput.value = commentId;
//             commentBody.focus();
//             commentBody.placeholder = "Reply to comment...";
//         });
//     });
//
//     function addCommentToDOM(comment) {
//         const commentHTML = `
//             <div class="comment-item bg-orange-50 dark:bg-dark-bg p-6 rounded-xl" data-comment-id="${comment.id}">
//                 <div class="flex items-start space-x-4">
//                     <div class="flex-shrink-0">
//                         <div class="w-10 h-10 rounded-full bg-orange-600 dark:bg-dark-accent flex items-center justify-center text-white">
//                             ${comment.user.name[0]}
//                         </div>
//                     </div>
//                     <div class="flex-1">
//                         <div class="flex items-center justify-between mb-2">
//                             <h3 class="font-semibold text-orange-800 dark:text-dark-text">${comment.user.name}</h3>
//                             <span class="text-sm text-gray-500 dark:text-dark-text-secondary">Just now</span>
//                         </div>
//                         <p class="text-gray-600 dark:text-dark-text-secondary">${comment.body}</p>
//                         <div class="flex items-center space-x-4 mt-4">
//                             <button class="reply-btn text-gray-500 dark:text-dark-text-secondary hover:text-orange-600 dark:hover:text-dark-accent transition duration-300" data-comment-id="${comment.id}">
//                                 <i class="fas fa-reply mr-1"></i> जवाब दें
//                             </button>
//                             <button class="like-btn text-gray-500 dark:text-dark-text-secondary hover:text-orange-600 dark:hover:text-dark-accent transition duration-300" data-comment-id="${comment.id}">
//                                 <i class="fas fa-thumbs-up mr-1"></i> पसंद
//                             </button>
//                         </div>
//                         <div class="replies-container mt-4 space-y-4 pl-8"></div>
//                     </div>
//                 </div>
//             </div>
//         `;
//
//         if (comment.parent_id) {
//             // Find parent comment and append reply
//             const parentComment = document.querySelector(`[data-comment-id="${comment.parent_id}"]`);
//             if (parentComment) {
//                 const repliesContainer = parentComment.querySelector('.replies-container');
//                 const replyHTML = `
//                     <div class="reply-item bg-white dark:bg-dark-card p-4 rounded-lg" data-comment-id="${comment.id}">
//                         <div class="flex items-start space-x-3">
//                             <div class="w-8 h-8 rounded-full bg-orange-600 dark:bg-dark-accent flex items-center justify-center text-white text-sm">
//                                 ${comment.user.name[0]}
//                             </div>
//                             <div class="flex-1">
//                                 <div class="flex items-center justify-between mb-1">
//                                     <h4 class="font-semibold text-orange-800 dark:text-dark-text text-sm">${comment.user.name}</h4>
//                                     <span class="text-xs text-gray-500 dark:text-dark-text-secondary">Just now</span>
//                                 </div>
//                                 <p class="text-gray-600 dark:text-dark-text-secondary text-sm">${comment.body}</p>
//                                 <div class="flex items-center space-x-3 mt-2">
//                                     <button class="reply-btn text-xs text-gray-500 dark:text-dark-text-secondary hover:text-orange-600 dark:hover:text-dark-accent transition duration-300" data-comment-id="${comment.id}">
//                                         <i class="fas fa-reply mr-1"></i> जवाब दें
//                                     </button>
//                                     <button class="like-btn text-xs text-gray-500 dark:text-dark-text-secondary hover:text-orange-600 dark:hover:text-dark-accent transition duration-300" data-comment-id="${comment.id}">
//                                         <i class="fas fa-thumbs-up mr-1"></i> पसंद
//                                     </button>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                 `;
//                 repliesContainer.insertAdjacentHTML('beforeend', replyHTML);
//             }
//         } else {
//             // Add new top-level comment
//             commentsContainer.insertAdjacentHTML('afterbegin', commentHTML);
//         }
//
//         // Add event listeners to new buttons
//         const newReplyButtons = document.querySelectorAll('.reply-btn');
//         newReplyButtons.forEach(button => {
//             button.addEventListener('click', function () {
//                 const commentId = this.dataset.commentId;
//                 parentIdInput.value = commentId;
//                 commentBody.focus();
//                 commentBody.placeholder = "Reply to comment...";
//             });
//         });
//     }
//
//     function updateCommentCount() {
//         const count = document.querySelectorAll('.comment-item').length;
//         commentCount.textContent = `${count} टिप्पणियाँ`;
//     }
// });