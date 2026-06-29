const chatWindow = document.getElementById("chatWindow");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const emptyState = document.getElementById("emptyState");
const newChatBtn = document.getElementById("newChatBtn");

// Holds the whole conversation in memory (no backend storage, per our design)
let conversation = [];

// API endpoint — same origin since FastAPI serves this frontend too
const API_URL = "/api/chat";

// --- Auto-resize the textarea as the user types ---
messageInput.addEventListener("input", () => {
  messageInput.style.height = "auto";
  messageInput.style.height = Math.min(messageInput.scrollHeight, 160) + "px";
});

// --- Submit on Enter, newline on Shift+Enter ---
messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    chatForm.requestSubmit();
  }
});

// --- New chat button just clears state ---
newChatBtn.addEventListener("click", () => {
  conversation = [];
  chatWindow.innerHTML = "";
  chatWindow.appendChild(emptyState);
});

function addMessageToDOM(role, text) {
  // Remove empty state once the conversation starts
  if (emptyState.isConnected) emptyState.remove();

  const row = document.createElement("div");
  row.className = `message-row ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  row.appendChild(bubble);
  chatWindow.appendChild(row);
  chatWindow.scrollTop = chatWindow.scrollHeight;

  return bubble; // return so we can update it live while streaming
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const text = messageInput.value.trim();
  if (!text) return;

  // 1. Show user's message immediately
  addMessageToDOM("user", text);
  conversation.push({ role: "user", content: text });

  // Reset input
  messageInput.value = "";
  messageInput.style.height = "auto";
  sendBtn.disabled = true;

  // 2. Create an empty assistant bubble we'll fill in as tokens stream
  const assistantBubble = addMessageToDOM("assistant", "");
  assistantBubble.classList.add("streaming");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: conversation }),
    });

    if (!response.ok || !response.body) {
      throw new Error(`Server responded with ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullReply = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunkText = decoder.decode(value, { stream: true });
      fullReply += chunkText;
      assistantBubble.textContent = fullReply;
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    assistantBubble.classList.remove("streaming");
    conversation.push({ role: "assistant", content: fullReply });
  } catch (err) {
    assistantBubble.classList.remove("streaming");
    assistantBubble.textContent =
      "Something went wrong reaching Skipy. Please check the server and try again.";
    console.error(err);
  } finally {
    sendBtn.disabled = false;
    messageInput.focus();
  }
});
