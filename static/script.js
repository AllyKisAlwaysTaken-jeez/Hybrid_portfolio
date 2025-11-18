const form = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");

function addMessage(content, sender) {
  const message = document.createElement("div");
  message.classList.add("message", sender);
  message.innerHTML = content;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addLoadingBubble() {
  const loading = document.createElement("div");
  loading.classList.add("message", "bot");
  loading.id = "loading";
  loading.innerHTML = "💭 Thinking...";
  chatBox.appendChild(loading);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLoadingBubble() {
  const loading = document.getElementById("loading");
  if (loading) loading.remove();
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const industry = document.getElementById("industry").value;
  const style = document.getElementById("style").value;
  const goals = document.getElementById("goals").value;
  const competitors = document.getElementById("competitors").value;

  const userMessage = `
    Industry: <strong>${industry}</strong><br>
    Style: <strong>${style}</strong><br>
    Goals: <strong>${goals}</strong>
  `;
  addMessage(userMessage, "user");
  form.reset();
  addLoadingBubble();

  try {
    const res = await fetch("/generate-advice", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ industry, style, goals, competitors })
    });
    const data = await res.json();
    removeLoadingBubble();

    const botMessage = `
      <strong>📋 Copywriting Advice:</strong><br>${data.copywriting.replace(/\n/g, "<br>")}<br><br>
      <strong>🔍 SEO Tips:</strong> ${data.seo_tips.recommended_keywords.join(", ")}<br>
      <strong>🎨 Design Guidelines:</strong><br>
      ${data.design_guidelines.map(g => `• ${g}`).join("<br>")}
    `;
    addMessage(botMessage, "bot");
  } catch (err) {
    removeLoadingBubble();
    addMessage(`❌ Error: ${err.message}`, "bot");
  }
});
