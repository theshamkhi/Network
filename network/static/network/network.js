document.addEventListener('DOMContentLoaded', function() {
    
    // Post editing functionality
    document.querySelectorAll('.edit-post').forEach(button => {
        button.onclick = function() {
            const postId = this.getAttribute('data-postid');
            const postContentElement = document.getElementById(`post-content-${postId}`);

            if (postContentElement) {
                const originalText = postContentElement.textContent;
                if (this.innerHTML === '<i class="bi bi-pencil-square"></i>') {
                    // Replace the post content with a text area for editing
                    postContentElement.innerHTML = `<textarea class="form-control" id="edited-content-${postId}">${originalText}</textarea>`;
                    this.innerHTML = '<i class="bi bi-check-lg"></i>';
                } else if (this.innerHTML === '<i class="bi bi-check-lg"></i>') {
                    // Get the edited content from the text area
                    const editedContent = document.getElementById(`edited-content-${postId}`).value;

                    // Send a request to update the post content
                    fetch(`/edit/${postId}/`, {
                        method: 'POST',
                        body: JSON.stringify({ content: editedContent }),
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'), // Include the CSRF token
                        }
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.status === 'success') {
                            postContentElement.textContent = result.new_content;
                            this.innerHTML = '<i class="bi bi-pencil-square"></i>';
                        } else {
                            alert('Failed to update the post. Please try again.');
                        }
                    });
                }
            }
        };
    });

    // Like functionality
    document.querySelectorAll('.like-button').forEach(button => {
        button.onclick = function() {
            const postId = this.getAttribute('data-postid');
            const likeCountElement = document.getElementById(`like-count-${postId}`);
            const liked = this.querySelector('i').classList.contains('fas');
    
            fetch(`/like_post/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Include the CSRF token
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    this.innerHTML = '<i class="fas fa-heart"></i>';
                } else {
                    this.innerHTML = '<i class="far fa-heart text-light"></i>';
                }
                likeCountElement.textContent = data.likes_count;
            });
        };
    });

    // Follow/Unfollow the user
    document.querySelectorAll('.follow-button').forEach(button => {
        button.onclick = function() {
            const username = this.getAttribute('data-username');
            const isFollowing = this.getAttribute('data-is-following') === 'true';
            const followerCountElement = document.querySelector('.follower-count');
            const followingCountElement = document.querySelector('.following-count');
    
            // Send a request to follow/unfollow the user
            fetch(`/follow/${username}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Include the CSRF token
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.following) {
                    // User is now following
                    this.innerHTML = '<button class="btn btn-secondary unfollowbtn">Unfollow</button>';
                } else {
                    // User is not following
                    this.innerHTML = '<button class="btn btn-primary followbtn">Follow</button>';
                }
    
                // Update follower and following counts with labels
                followerCountElement.innerHTML = `${data.follower_count} Followers`;
                followingCountElement.innerHTML = `${data.following_count} Following`;
            });
        };
    });
    

    // Delete Post
    document.querySelectorAll('.delete-post').forEach(button => {
        button.onclick = function() {
            const postId = this.getAttribute('data-postid');
            
            // Send a request to delete the post
            fetch(`/delete_post/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.deleted) {
                    // Remove the post from the UI
                    const postElement = document.querySelector(`#post-content-${postId}`).closest('.card');
                    postElement.remove();
                } else {
                    alert('Failed to delete the post. Please try again.');
                }
            });
        };
    });

    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (currentPath === href) {
            link.classList.add('selected');
        }
    });
    
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}