// Menu
const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
    dropdownButton.addEventListener("click", () => {
        dropdownMenu.classList.toggle("show");
    });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
    photoInput.onchange = () => {
        const [file] = photoInput.files;
        if (file) {
            photoPreview.src = URL.createObjectURL(file);
        }
    };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;



// Auto-hide message after 3 seconds
setTimeout(() => {
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => {
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 400); // Remove from DOM after fade-out
    });
}, 1500); // 1.5 seconds




// For Showing how many files selected from File Explorer
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file-upload');
    const fileCountSpan = document.getElementById('file-count');
    const chatForm = document.querySelector('.chat-form');

    // Only run if file input exists
    if (fileInput && fileCountSpan) {

        fileInput.addEventListener('change', () => {
            const count = fileInput.files.length;

            if (count === 0) {
                fileCountSpan.textContent = '';
            } else if (count === 1) {
                fileCountSpan.textContent = '1 file selected';
            } else {
                fileCountSpan.textContent = `${count} files selected`;
            }
        });
    }

    // Clear file count on form submit
    if (chatForm && fileCountSpan) {
        chatForm.addEventListener('submit', () => {
            fileCountSpan.textContent = '';
        });
    }
});
