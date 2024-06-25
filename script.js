const chatContainer = document.querySelector('.chat-container');
const chatMessages = document.querySelector('.chat-messages');
const userInput = document.querySelector('#user-input');
const sendBtn = document.querySelector('#send-btn');
const micBtn = document.querySelector('#mic-btn');

let conversation = [];

// Send button click event
sendBtn.addEventListener('click', () => {
    const userInputValue = userInput.value.trim();
    if (userInputValue!== '') {
        sendRequest(userInputValue);
        userInput.value = '';
    }
});

// Mic button click event
micBtn.addEventListener('click', () => {
    // Initialize speech recognition
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.maxResults = 10;

    recognition.onresult = event => {
        const transcript = event.results[0][0].transcript;
        sendRequest(transcript);
    };

    recognition.start();
});

// Send request to backend
function sendRequest(userInputValue) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/ask', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            displayResponse(response);
        }
    };

    xhr.send(JSON.stringify({ userInput: userInputValue }));
}

// Display response from backend
function displayResponse(response) {
    const messageHTML = `
        <div class="message">
            <p>${response.userInput}</p>
            <p>${response.response}</p>
        </div>
    `;
    chatMessages.innerHTML += messageHTML;
    conversation.push(response);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
