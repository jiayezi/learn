document.addEventListener("DOMContentLoaded", function() {
    var fileInput = document.getElementById("id_file");
    var uploadButton = document.querySelector("button[type='submit']");
    var fileNameDisplay = document.getElementById("file_name_display");

    fileInput.addEventListener("change", function() {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = fileInput.files[0].name;
        } else {
            fileNameDisplay.textContent = "没有选择文件";
        }
    });

    uploadButton.addEventListener("click", function(event) {
        if (fileInput.files.length === 0) {
            event.preventDefault(); // 阻止默认提交行为
            fileNameDisplay.textContent = "没有选择文件";
        }
    });
});
