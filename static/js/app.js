// Chạy code khi trang đã tải xong
document.addEventListener("DOMContentLoaded", () => {
    
    // === XỬ LÝ NÚT COPY ===
    const copyButtons = document.querySelectorAll(".copy-btn");
    copyButtons.forEach(button => {
        button.addEventListener("click", () => {
            const targetSelector = button.dataset.copyTarget;
            const targetElement = document.querySelector(targetSelector);
            
            if (targetElement) {
                const textToCopy = targetElement.innerText;
                navigator.clipboard.writeText(textToCopy).then(() => {
                    // Thông báo copy thành công
                    const originalText = button.innerText;
                    button.innerText = "Đã copy!";
                    setTimeout(() => {
                        button.innerText = originalText;
                    }, 1500);
                }).catch(err => {
                    console.error("Lỗi copy: ", err);
                });
            }
        });
    });

    // === XỬ LÝ NÚT LIKE (AJAX) ===
    
    // Lấy CSRF token từ thẻ <meta>
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Gắn sự kiện click cho tất cả các nút like
    document.querySelectorAll(".like-btn").forEach(button => {
        button.addEventListener("click", () => {
            const postId = button.dataset.postId;
            toggleLike(postId);
        });
    });

    // Hàm gửi request AJAX
    async function toggleLike(postId) {
        const url = `/forum/post/${postId}/toggle-like/`;

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest" // Báo cho Django đây là AJAX
                },
            });

            if (!response.ok) {
                throw new Error("Lỗi mạng hoặc server");
            }

            const data = await response.json();
            
            // Cập nhật giao diện
            updateLikeButton(postId, data.liked, data.total_likes);

        } catch (error) {
            console.error("Lỗi khi like:", error);
        }
    }

    // Hàm cập nhật nút bấm và số like
    function updateLikeButton(postId, liked, totalLikes) {
        const button = document.querySelector(`.like-btn[data-post-id="${postId}"]`);
        const likeCountSpan = document.querySelector(`#like-count-${postId}`);

        if (button && likeCountSpan) {
            // Cập nhật số like
            likeCountSpan.innerText = totalLikes;
            
            // Cập nhật trạng thái (màu sắc) của nút
            if (liked) {
                button.classList.add("liked");
            } else {
                button.classList.remove("liked");
            }
        }
    }
});