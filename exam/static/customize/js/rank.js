function toggleAllCheckboxes(selectAllId) {
    var checkboxes;
    if (selectAllId === 'selectAll1') {
        checkboxes = document.querySelectorAll('input[name="selected_subjects"]');
    } else if (selectAllId === 'selectAll2') {
        checkboxes = document.querySelectorAll('input[name="selected_groups"]');
    }

    var selectAllCheckbox = document.getElementById(selectAllId);

    // 获取全选按钮的当前状态
    var isChecked = selectAllCheckbox.checked;

    // 根据全选按钮的状态设置复选框的选中状态
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = isChecked;
    }
}
