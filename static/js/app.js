// Chạy code khi trang đã tải xong
document.addEventListener("DOMContentLoaded", () => {
    
    // === XỬ LÝ NÚT COPY ===
    const copyButtons = document.querySelectorAll(".copy-btn");
    copyButtons.forEach(button => {
        button.addEventListener("click", () => {
            const targetSelector = button.dataset.copyTarget;
            const targetElement = document.querySelector(targetSelector);
            
            if (targetElement) {
                // Sửa: Lấy text từ (innerText hoặc value của input)
                const textToCopy = targetElement.value || targetElement.innerText;
                
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

    // === XỬ LÝ HERO SLIDESHOW (TRANG CHỦ) ===
    const slideshow = document.querySelector(".hero-slideshow");
    if (slideshow) {
        const slides = slideshow.querySelectorAll(".slide");
        let currentSlide = 0;

        // Hiển thị slide đầu tiên ngay lập tức
        if (slides.length > 0) {
            slides[currentSlide].classList.add("active");
        }

        // Chuyển slide mỗi 5 giây
        setInterval(() => {
            if (slides.length > 0) {
                // Ẩn slide hiện tại
                slides[currentSlide].classList.remove("active");
                
                // Tính slide tiếp theo
                currentSlide = (currentSlide + 1) % slides.length;
                
                // Hiện slide tiếp theo
                slides[currentSlide].classList.add("active");
            }
        }, 5000); // 5000ms = 5 giây
    }
    
}); // <-- Đây là dấu ngoặc }); KẾT THÚC của file