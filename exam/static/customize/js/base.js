// 显示菜单
function toggleMenu() {
  var menu = document.getElementById("dropdownMenu");
  menu.style.display = (menu.style.display === "block") ? "none" : "block";
}

function hideMenu() {
  var menu = document.getElementById("dropdownMenu");
  menu.style.display = "none";
}

// 实现全选按钮的功能
function toggleAllCheckboxes(selectAllId, checkboxName) {
    var checkboxes = document.querySelectorAll('input[name="' + checkboxName + '"]');
    var selectAllCheckbox = document.getElementById(selectAllId);

    // 获取全选按钮的当前状态
    var isChecked = selectAllCheckbox.checked;

    // 根据全选按钮的状态设置复选框的选中状态
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = isChecked;
    }
}
