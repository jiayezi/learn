function toggleAllCheckboxes() {
            var checkboxes = document.querySelectorAll('input[type="checkbox"]');
            var selectAllCheckbox = document.getElementById('selectAll');

            // 获取全选按钮的当前状态
            var isChecked = selectAllCheckbox.checked;

            // 根据全选按钮的状态设置复选框的选中状态
            for (var i = 0; i < checkboxes.length; i++) {
                checkboxes[i].checked = isChecked;
            }
        }


// 获取按钮和弹出式窗口
  var modalBtn = document.getElementById("openConfigBtn");
  var modal = document.getElementById("config_list");
  var modalContainer = document.getElementById("modalContainer");

  // 当按钮被点击时显示弹出式窗口
  modalBtn.onclick = function() {
    centerModal();
    modal.style.display = "block";
    modalContainer.style.display = "block"; // 显示背景层
  }

  // 获取关闭按钮
  var closeBtn = modal.querySelector(".close");

  // 当关闭按钮被点击时隐藏弹出式窗口
  closeBtn.onclick = function() {
    modal.style.display = "none";
    modalContainer.style.display = "none"; // 隐藏背景层
  }

  // 使弹出式窗口可拖动
  var isDragging = false;
  var modalContent = modal.querySelector(".modal-content");

  modalContent.addEventListener("mousedown", function(event) {
    isDragging = true;
    var offsetX = event.clientX - modal.offsetLeft;
    var offsetY = event.clientY - modal.offsetTop;

    document.onmousemove = function(event) {
      if (isDragging) {
        var x = event.clientX - offsetX;
        var y = event.clientY - offsetY;

        modal.style.left = x + "px";
        modal.style.top = y + "px";
      }
    };

    document.onmouseup = function() {
      isDragging = false;
      document.onmousemove = null;
      document.onmouseup = null;
    };
  });

  // 控制弹出式窗口被打开时的位置
  function centerModal() {
    var windowWidth = window.innerWidth;
    var windowHeight = window.innerHeight;
    var modalWidth = modal.offsetWidth;
    var modalHeight = modal.offsetHeight;

    var leftPos = (windowWidth - modalWidth) / 3;
    var topPos = (windowHeight - modalHeight) / 4;

    modal.style.left = leftPos + "px";
    modal.style.top = topPos + "px";
  }

  // 当窗口大小变化时重新居中弹出式窗口
  window.onresize = function() {
    if (modal.style.display === "block") {
      centerModal();
    }
  };