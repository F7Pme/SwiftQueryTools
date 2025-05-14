// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function () {
    // 获取DOM元素 - 上传相关
    const fileUploadContainer = document.getElementById('file-upload-container');
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const uploadButton = document.getElementById('upload-button');
    const uploadStatus = document.getElementById('upload-status');
    const searchSection = document.getElementById('search-section');
    const fileInfo = document.getElementById('file-info');
    const fileStats = document.getElementById('file-stats');
    const resetButton = document.getElementById('reset-button');

    // 获取DOM元素 - 查询相关
    const swiftInput = document.getElementById('swift-input');
    const searchButton = document.getElementById('search-button');
    const resultContainer = document.getElementById('result-container');
    const bankRole = document.getElementById('bank-role');
    const messageType = document.getElementById('message-type');
    const directParticipant = document.getElementById('direct-participant');
    const messageTypeSelect = document.getElementById('message-type-select');
    const errorMessage = document.getElementById('error-message');

    // 创建建议列表容器
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'suggestions-container';
    suggestionsContainer.style.display = 'none';
    swiftInput.parentNode.insertBefore(suggestionsContainer, swiftInput.nextSibling);

    // 设置防抖延迟
    let debounceTimeout = null;
    const DEBOUNCE_DELAY = 300; // 毫秒

    // 初始化应用
    initApp();

    // 初始化应用
    function initApp() {
        // 检查是否已有数据加载
        checkDataStatus();

        // 设置文件上传事件监听
        setupFileUpload();

        // 绑定搜索按钮点击事件
        searchButton.addEventListener('click', performSearch);

        // 绑定输入框回车事件
        swiftInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });

        // 绑定输入框输入事件
        swiftInput.addEventListener('input', handleInput);

        // 绑定重置按钮事件
        resetButton.addEventListener('click', resetApplication);

        // 添加点击事件监听器，处理建议选择
        document.addEventListener('click', function (e) {
            // 检查点击是否在建议容器外
            if (!suggestionsContainer.contains(e.target) && e.target !== swiftInput) {
                suggestionsContainer.style.display = 'none';
            }
        });
    }

    // 检查数据状态
    function checkDataStatus() {
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                if (data.loaded) {
                    // 数据已加载，显示查询界面
                    showSearchInterface(data);
                }
            })
            .catch(error => {
                console.error('状态检查失败:', error);
            });
    }

    // 设置文件上传
    function setupFileUpload() {
        // 点击上传按钮触发文件选择
        uploadButton.addEventListener('click', function () {
            fileInput.click();
        });

        // 文件选择改变时上传文件
        fileInput.addEventListener('change', function () {
            if (fileInput.files.length > 0) {
                uploadFile(fileInput.files[0]);
            }
        });

        // 点击拖拽区域触发文件选择
        dropArea.addEventListener('click', function () {
            fileInput.click();
        });

        // 拖拽相关事件
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // 高亮拖拽区域
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, unhighlight, false);
        });

        function highlight() {
            dropArea.classList.add('active');
        }

        function unhighlight() {
            dropArea.classList.remove('active');
        }

        // 处理文件拖放
        dropArea.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;

            if (files.length > 0) {
                uploadFile(files[0]);
            }
        }
    }

    // 上传文件
    function uploadFile(file) {
        // 检查文件类型
        if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
            uploadStatus.innerHTML = '<span style="color: #f44336;">只支持Excel文件(.xlsx, .xls)</span>';
            return;
        }

        // 显示上传状态
        uploadStatus.innerHTML = `<span>正在上传: ${file.name}</span>
                               <div class="upload-progress">
                                  <div class="upload-progress-bar" style="width: 0%"></div>
                               </div>`;

        const progressBar = document.querySelector('.upload-progress-bar');

        // 创建FormData
        const formData = new FormData();
        formData.append('file', file);

        // 创建XMLHttpRequest
        const xhr = new XMLHttpRequest();

        // 上传进度
        xhr.upload.addEventListener('progress', function (e) {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressBar.style.width = percentComplete + '%';
            }
        });

        // 请求完成
        xhr.addEventListener('load', function () {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                uploadStatus.innerHTML = '<span style="color: #4CAF50;">文件上传成功!</span>';

                // 显示查询界面
                showSearchInterface(response.stats);
            } else {
                let errorMsg = '上传失败';
                try {
                    const response = JSON.parse(xhr.responseText);
                    errorMsg = response.error || errorMsg;
                } catch (e) { }

                uploadStatus.innerHTML = `<span style="color: #f44336;">${errorMsg}</span>`;
            }
        });

        // 请求错误
        xhr.addEventListener('error', function () {
            uploadStatus.innerHTML = '<span style="color: #f44336;">网络错误，请重试</span>';
        });

        // 发送请求
        xhr.open('POST', '/api/upload');
        xhr.send(formData);
    }

    // 显示查询界面
    function showSearchInterface(stats) {
        // 隐藏上传区域
        fileUploadContainer.style.display = 'none';

        // 显示查询区域
        searchSection.style.display = 'block';

        // 显示文件信息
        fileInfo.style.display = 'block';

        // 显示文件统计信息
        let statsHtml = '';
        if (stats.records) {
            statsHtml = `<p>已加载 ${stats.records} 条数据记录</p>`;
        }
        fileStats.innerHTML = statsHtml;

        // 清空并聚焦搜索框
        swiftInput.value = '';
        swiftInput.focus();
    }

    // 重置应用
    function resetApplication() {
        // 显示上传区域
        fileUploadContainer.style.display = 'block';
        uploadStatus.innerHTML = '';

        // 隐藏查询区域
        searchSection.style.display = 'none';

        // 隐藏文件信息
        fileInfo.style.display = 'none';

        // 清空结果
        resultContainer.style.display = 'none';
        errorMessage.textContent = '';

        // 清空输入
        swiftInput.value = '';
        fileInput.value = '';
    }

    // 处理输入事件
    function handleInput() {
        // 清除之前的延迟
        if (debounceTimeout) {
            clearTimeout(debounceTimeout);
        }

        // 设置新的延迟，防止频繁请求
        debounceTimeout = setTimeout(function () {
            const inputValue = swiftInput.value.trim().toUpperCase();

            // 清空错误信息
            errorMessage.textContent = '';

            // 如果输入为空，隐藏建议和结果
            if (!inputValue) {
                suggestionsContainer.style.display = 'none';
                resultContainer.style.display = 'none';
                return;
            }

            // 获取建议
            fetchSuggestions(inputValue);

            // 执行模糊查询
            if (inputValue.length >= 1) {
                executeFuzzySearch(inputValue);
            }
        }, DEBOUNCE_DELAY);
    }

    // 获取SWIFT代码建议
    function fetchSuggestions(prefix) {
        if (!prefix) {
            suggestionsContainer.style.display = 'none';
            return;
        }

        fetch(`/api/suggest?prefix=${encodeURIComponent(prefix)}`)
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

                displaySuggestions(data.suggestions);
            })
            .catch(error => {
                console.error('获取建议失败:', error);
                suggestionsContainer.style.display = 'none';
            });
    }

    // 显示建议列表
    function displaySuggestions(suggestions) {
        // 清空建议容器
        suggestionsContainer.innerHTML = '';

        if (!suggestions || suggestions.length === 0) {
            suggestionsContainer.style.display = 'none';
            return;
        }

        // 创建建议列表
        const ul = document.createElement('ul');
        ul.className = 'suggestions-list';

        suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.className = 'suggestion-item';
            li.textContent = suggestion;

            // 点击建议项填充到输入框并执行查询
            li.addEventListener('click', function () {
                swiftInput.value = suggestion;
                suggestionsContainer.style.display = 'none';
                performSearch();
            });

            ul.appendChild(li);
        });

        suggestionsContainer.appendChild(ul);
        suggestionsContainer.style.display = 'block';
    }

    // 执行模糊查询
    function executeFuzzySearch(swiftCode) {
        fetch(`/api/query?swift=${encodeURIComponent(swiftCode)}&exact=false`)
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

                displayResults(data);
            })
            .catch(error => {
                showError(error.message || '查询失败，请稍后重试');
            });
    }

    // 执行精确查询
    function performSearch() {
        // 获取输入的SWIFT代码
        const swiftCode = swiftInput.value.trim().toUpperCase();

        // 清空错误信息
        errorMessage.textContent = '';

        // 隐藏建议列表
        suggestionsContainer.style.display = 'none';

        // 检查输入是否为空
        if (!swiftCode) {
            showError('请输入SWIFT业务编号');
            return;
        }

        // 检查SWIFT代码格式 (通常为11位字母数字组合)
        if (!/^[A-Z0-9]{1,11}$/.test(swiftCode)) {
            showError('SWIFT业务编号格式不正确，应为不超过11位的字母数字');
            return;
        }

        // 调用API查询数据 (精确匹配)
        fetch(`/api/query?swift=${encodeURIComponent(swiftCode)}&exact=true`)
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