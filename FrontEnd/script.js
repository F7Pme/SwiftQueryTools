// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function () {
    // 获取DOM元素
    const swiftInput = document.getElementById('swift-input');
    const searchButton = document.getElementById('search-button');
    const resultContainer = document.getElementById('result-container');
    const bankRole = document.getElementById('bank-role');
    const messageType = document.getElementById('message-type');
    const directParticipant = document.getElementById('direct-participant');
    const messageTypeSelect = document.getElementById('message-type-select');
    const errorMessage = document.getElementById('error-message');

    // 绑定搜索按钮点击事件
    searchButton.addEventListener('click', performSearch);

    // 绑定输入框回车事件
    swiftInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    // 执行查询
    function performSearch() {
        // 获取输入的SWIFT代码
        const swiftCode = swiftInput.value.trim().toUpperCase();

        // 清空错误信息
        errorMessage.textContent = '';

        // 检查输入是否为空
        if (!swiftCode) {
            showError('请输入SWIFT业务编号');
            return;
        }

        // 检查SWIFT代码格式 (通常为11位字母数字组合)
        if (!/^[A-Z0-9]{11}$/.test(swiftCode)) {
            showError('SWIFT业务编号格式不正确，应为11位字母数字');
            return;
        }

        // 调用API查询数据
        fetch(`/api/query?swift=${swiftCode}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('网络异常或服务器错误');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }

                // 显示查询结果
                displayResults(data);
            })
            .catch(error => {
                showError(error.message || '查询失败，请稍后重试');
            });
    }

    // 显示查询结果
    function displayResults(data) {
        // 如果有查询结果
        if (data && Array.isArray(data.results) && data.results.length > 0) {
            // 取第一条记录显示
            const result = data.results[0];

            // 填充数据到页面元素
            bankRole.textContent = result.bank_role || '未知';
            messageType.textContent = result.message_type || '未知';
            directParticipant.textContent = result.direct_participant || '无';

            // 如果有报文类型，选中下拉框中对应的选项
            if (result.message_type) {
                setSelectedOption(messageTypeSelect, result.message_type);
            }

            // 显示结果容器
            resultContainer.style.display = 'block';
        } else {
            showError('未找到相关记录');
        }
    }

    // 设置下拉框选中选项
    function setSelectedOption(selectElement, value) {
        for (let i = 0; i < selectElement.options.length; i++) {
            if (selectElement.options[i].value === value) {
                selectElement.selectedIndex = i;
                break;
            }
        }
    }

    // 显示错误信息
    function showError(message) {
        errorMessage.textContent = message;
        resultContainer.style.display = 'none';
    }
}); 