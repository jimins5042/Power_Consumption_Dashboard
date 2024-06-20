document.addEventListener('DOMContentLoaded', function () {
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


        fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json; charset=UTF-8",
            },
            body: JSON.stringify(userMessage),
        })
            .then(response => response.json())
            .then(data => {
                // Destroy existing DataTable instance (if any)
                console.log("Received data:", data);
                const tableBody = document.querySelector('#dataTable tbody');
                tableBody.innerHTML = '';
                const maxLength = 20; // 최대 길이 설정 (예시로 20자)

                data.data.forEach(row => {
                    const tr = document.createElement('tr');
                    const data2 = document.createElement('td');
                    //dateTd.textContent = row[0];
                    // row[0] 문자열의 길이가 maxLength보다 길면 자름

                    const data1 = document.createElement('td');
                    data1.textContent = row[2];
                    tr.appendChild(data1);

                    if (row[0].length > maxLength) {
                        data2.textContent = row[0].substring(0, maxLength) + '...';
                    } else {
                        data2.textContent = row[0];
                    }

                    tr.appendChild(data2);

                    const data3 = document.createElement('td');
                    data3.textContent = parseFloat(row[1]).toFixed(2);
                    tr.appendChild(data3);

                    tableBody.appendChild(tr);
                });

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
})
;
