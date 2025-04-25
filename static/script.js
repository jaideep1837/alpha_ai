async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();
    inputField.value = ""; // Clear input field
    if (message === "") return;

    // Append user message to chat
    appendMessage("user", message);

    // Send request to Django backend
    const response = await fetch("http://127.0.0.1:8000/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message }),
    });

    const data = await response.json();
    console.log(data.response);
    appendMessage("bot", data.response); // Append bot response to chat

    
}

function appendMessage(sender, text) {
    const chatContainer = document.getElementById("chat-container");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll to latest message
}

function handleKeyPress(event) {
    if (event.key === "Enter") sendMessage();
}

function clearChat() {
    document.getElementById("chat-container").innerHTML = "";
}