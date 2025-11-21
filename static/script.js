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

document.getElementById("rewrite-form").addEventListener("submit", async function (e) {
  e.preventDefault(); // Stop form reload

  const data = {
      page: document.getElementById("section").value,
      content: {
          role: document.getElementById("job_role").value,
          keywords: document.getElementById("keywords").value,
          project: document.getElementById("project_info").value
      }
  };

  const response = await fetch("/ai-rewrite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
  });

  const result = await response.json();

  document.getElementById("rewrite-output").innerHTML =
      `<p><strong>Saved:</strong> ${result.page}</p>`;
});


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

// AI Rewrite Handler
document.getElementById("rewrite-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const section = document.getElementById("section").value;
  const job_role = document.getElementById("job_role").value;
  const keywords = document.getElementById("keywords").value;
  const project_info = document.getElementById("project_info").value;

  const payload = {
      section,
      job_role,
      keywords,
      project_info
  };

  const response = await fetch("/ai-rewrite", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
  });

  const data = await response.json();

  // Show rewritten text
  document.getElementById("rewrite-output").innerHTML = `
      <strong>Rewritten Text:</strong>
      <p>${data.rewritten_text}</p>
  `;
});
