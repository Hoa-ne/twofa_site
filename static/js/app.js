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
s                  }, 1500);
                }).catch(err => {
                    console.error("Lỗi copy: ", err);
                });
            }
        });
    });

    // === XỬ LÝ NÚT LIKE (AJAX) ===
    // (Đã xóa)

    // === (THÊM MỚI) XỬ LÝ HERO SLIDESHOW (TRANG CHỦ) ===
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

});