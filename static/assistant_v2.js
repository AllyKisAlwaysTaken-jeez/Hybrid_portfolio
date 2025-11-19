const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const generateBtn = document.getElementById("generate-portfolio");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const industry = document.getElementById("industry").value.trim();
  const style = document.getElementById("style").value.trim();
  const goals = document.getElementById("goals").value.trim();
  const competitors = document.getElementById("competitors").value.trim();

  if (!industry || !style || !goals) return;

  addMessage(`Industry: ${industry}, Style: ${style}, Goals: ${goals}`, "user");

  const response = await fetch("/ai-assistant", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ industry, style, goals, competitors })
  });

  const data = await response.json();
  addMessage(data.advice, "bot");

  // Show the generate button after first assistant advice
  generateBtn.style.display = "block";

  chatForm.reset();
});

generateBtn.addEventListener("click", async () => {
  const response = await fetch("/generate-portfolio", { method: "POST" });
  const data = await response.json();
  if (data.status === "success") {
    addMessage("🚀 Portfolio generation triggered!", "bot");
  }
});

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.innerHTML = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}
