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
