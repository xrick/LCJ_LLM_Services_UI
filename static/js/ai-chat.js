document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages');
    const userMessageInput = document.getElementById('user-message');
    const sendMessageButton = document.getElementById('send-message');

    // 發送消息到後端
    const sendMessage = async () => {
        const userMessage = userMessageInput.value.trim();
        if (!userMessage) return;

        // 在聊天框中顯示用戶消息
        appendMessage('user', userMessage);

        try {
            const response = await fetch('/api/ai-chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            const data = await response.json();
            if (response.ok) {
                appendMessage('ai', data.response);
            } else {
                appendMessage('error', '無法處理您的請求');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            appendMessage('error', '發送消息時出錯');
        }

        // 清空輸入框
        userMessageInput.value = '';
    };

    // 動態添加消息
    const appendMessage = (sender, message) => {
        const messageElement = document.createElement('div');
        messageElement.className = `p-2 rounded-lg ${
            sender === 'user' ? 'bg-blue-500 text-white self-end' : 'bg-gray-200 text-gray-800 self-start'
        }`;
        messageElement.textContent = message;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight; // 滾動到底部
    };

    // 綁定按鈕事件
    sendMessageButton.addEventListener('click', sendMessage);
    userMessageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
