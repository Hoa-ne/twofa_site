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

    // === XỬ LÝ NÚT HIỂN THỊ MẬT KHẨU ===
    const togglePasswordButtons = document.querySelectorAll(".password-toggle-btn");
    
    togglePasswordButtons.forEach(button => {
        button.addEventListener("click", () => {
            const targetSelector = button.dataset.target;
            const targetInput = document.querySelector(targetSelector);
            
            if (targetInput) {
                // Kiểm tra trạng thái hiện tại
                if (targetInput.type === "password") {
                    // Nếu đang là password -> chuyển sang text
                    // SỬA LỖI: Xóa ký tự 's' ở dòng dưới
                    targetInput.type = "text";
                    button.innerText = "Ẩn";
                } else {
                    // Nếu đang là text -> chuyển về password
                    targetInput.type = "password";
                    button.innerText = "Hiện";
                }
            }
        });
    });
    
}); // <-- Đây là dấu ngoặc }); KẾT THÚC của file