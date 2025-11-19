const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const generateBtn = document.getElementById("generate-portfolio");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const industry = document.getElementById("industry").value;
  const style = document.getElementById("style").value;
  const goals = document.getElementById("goals").value;
  const competitors = document.getElementById("competitors").value;

  // Add user message to chat
  const userMessage = document.createElement("div");
  userMessage.className = "message user";
  userMessage.innerText = `Industry: ${industry}, Style: ${style}, Goals: ${goals}`;
  chatBox.appendChild(userMessage);

  chatBox.scrollTop = chatBox.scrollHeight;

  // Send to Flask assistant
  const response = await fetch("/ai-assistant", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ industry, style, goals, competitors })
  });

  const data = await response.json();

  // Add bot advice to chat
  const botMessage = document.createElement("div");
  botMessage.className = "message bot";
  botMessage.innerText = data.advice;
  chatBox.appendChild(botMessage);
  chatBox.scrollTop = chatBox.scrollHeight;

  // Show the generate portfolio button
  generateBtn.style.display = "block";
});

// Handle Generate Portfolio button
generateBtn.addEventListener("click", async () => {
  const industry = document.getElementById("industry").value;
  const style = document.getElementById("style").value;
  const goals = document.getElementById("goals").value;
  const competitors = document.getElementById("competitors").value;

  const response = await fetch("/generate-portfolio", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ industry, style, goals, competitors })
  });

  const data = await response.json();

  const botMessage = document.createElement("div");
  botMessage.className = "message bot";
  botMessage.innerText = "✅ Portfolio generated successfully!";
  chatBox.appendChild(botMessage);
  chatBox.scrollTop = chatBox.scrollHeight;

  generateBtn.style.display = "none"; // hide button again
});
