const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const generateButton = document.getElementById("generate-portfolio");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const industry = document.getElementById("industry").value;
  const style = document.getElementById("style").value;
  const goals = document.getElementById("goals").value;
  const competitors = document.getElementById("competitors").value;

  // Append user message
  const userMsg = document.createElement("div");
  userMsg.className = "message user";
  userMsg.textContent = `Industry: ${industry}, Style: ${style}, Goals: ${goals}`;
  chatBox.appendChild(userMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  // Send data to backend
  const res = await fetch("/ai-assistant", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ industry, style, goals, competitors }),
  });

  const data = await res.json();

  // Append bot response
  const botMsg = document.createElement("div");
  botMsg.className = "message bot";
  botMsg.textContent = data.advice;
  chatBox.appendChild(botMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  // Show portfolio generation button
  generateButton.style.display = "block";
});

// Example: portfolio generation
generateButton.addEventListener("click", async () => {
  const res = await fetch("/generate-portfolio", { method: "POST" });
  const data = await res.json();
  alert("Portfolio generation started! Check your dashboard.");
});
