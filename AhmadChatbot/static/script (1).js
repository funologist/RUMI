const chat = document.getElementById('chat');
const composer = document.getElementById('composer');
const input = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');

function scrollToBottom() {
  chat.scrollTop = chat.scrollHeight;
}

function addMessage(role, text) {
  const msg = document.createElement('div');
  msg.className = `msg msg-${role}`;

  const avatar = document.createElement('div');
  if (role === 'bot') {
    avatar.className = 'avatar avatar-bot';
    avatar.innerHTML = '<span></span><span></span><span></span>';
  } else {
    avatar.style.width = '0';
  }

  const bubble = document.createElement('div');
  bubble.className = `bubble bubble-${role}`;
  bubble.textContent = text;

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  chat.appendChild(msg);
  scrollToBottom();
  return bubble;
}

function addTypingIndicator() {
  const msg = document.createElement('div');
  msg.className = 'msg msg-bot';
  msg.id = 'typingMsg';

  const avatar = document.createElement('div');
  avatar.className = 'avatar avatar-bot';
  avatar.innerHTML = '<span></span><span></span><span></span>';

  const bubble = document.createElement('div');
  bubble.className = 'bubble bubble-bot';
  bubble.innerHTML = '<span class="typing"><span></span><span></span><span></span></span>';

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  chat.appendChild(msg);
  scrollToBottom();
}

function removeTypingIndicator() {
  const el = document.getElementById('typingMsg');
  if (el) el.remove();
}

async function sendMessage(text) {
  addMessage('user', text);
  input.value = '';
  sendBtn.disabled = true;
  addTypingIndicator();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    removeTypingIndicator();

    if (!res.ok) {
      addMessage('bot', `Something went wrong: ${data.error || 'unknown error'}`);
    } else {
      addMessage('bot', data.reply);
    }
  } catch (err) {
    removeTypingIndicator();
    addMessage('bot', 'Connection error. Is the server running?');
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

composer.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  sendMessage(text);
});

resetBtn.addEventListener('click', async () => {
  await fetch('/api/reset', { method: 'POST' });
  chat.innerHTML = '';
  addMessage('bot', "Fresh start. What's on your mind?");
});

input.focus();
