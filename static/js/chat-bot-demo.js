document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById("send-button");
    const userInput = document.getElementById("user-input");
    const messagesContainer = document.getElementById("messages-container");

    // 기본 메시지를 화면에 추가하는 함수
    function displayBotMessage(message) {
        const botMessageElement = document.createElement("div");
        botMessageElement.classList.add("chat-message", "bot-message");
        botMessageElement.innerHTML = message; // innerHTML을 사용하여 HTML 태그 인식
        messagesContainer.appendChild(botMessageElement);
    }

    // 페이지가 로드되었을 때 기본 메시지를 추가
    const defaultMessages = ["안녕하세요!<br> 전력거래소 관리 AI 입니다.", "무엇이 궁금하신가요?"];
    defaultMessages.forEach(message => {
        displayBotMessage(message);
    });
    scrollToBottom(messagesContainer);

    sendButton.addEventListener("click", async () => {
        const userMessage = userInput.value;
        displayUserMessage(userMessage);
        scrollToBottom(messagesContainer);
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json; charset=UTF-8",
            },
            body: JSON.stringify(userMessage),
        })
        .then(response => response.text())
        .then(data => {
            const botMessageElement = document.createElement("div");
            botMessageElement.classList.add("chat-message", "bot-message");
            botMessageElement.innerHTML = data; // innerHTML을 사용하여 HTML 태그 인식
            messagesContainer.appendChild(botMessageElement);
            scrollToBottom(messagesContainer);
        });
    });

    function displayUserMessage(message) {
        const userMessageElement = document.createElement("div");
        userMessageElement.classList.add("chat-message", "user-message");
        userMessageElement.textContent = message;
        messagesContainer.appendChild(userMessageElement);
        userInput.value = "";
    }

    function scrollToBottom(element) {
        element.scrollTop = element.scrollHeight;
    }

    function handleInputKeyPress(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // 기본 엔터 동작 방지
            sendButton.click(); // send 버튼 클릭
        }
    }

    userInput.addEventListener("keydown", handleInputKeyPress);
});
