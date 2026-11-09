const BACKEND_URL = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", () => {
  const urlBox = document.getElementById("url-box");
  const protocolBadge = document.getElementById("protocol-badge");
  const scanBtn = document.getElementById("scan-btn");
  const loader = document.getElementById("loader");
  const resultBox = document.getElementById("result-box");
  const errorBox = document.getElementById("error-box");
  const threatBadge = document.getElementById("threat-badge");
  const threatScore = document.getElementById("threat-score");
  const meterFill = document.getElementById("meter-fill");
  const confidenceText = document.getElementById("confidence-text");
  const reasonsList = document.getElementById("reasons-list");
  const openConsoleBtn = document.getElementById("open-console-btn");

  let currentTabUrl = "";

  // 1. Detect active browser tab URL
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs && tabs[0] && tabs[0].url) {
      currentTabUrl = tabs[0].url;
      urlBox.textContent = currentTabUrl;

      // Update protocol tag
      if (currentTabUrl.startsWith("https://")) {
        protocolBadge.textContent = "HTTPS";
        protocolBadge.className = "protocol-tag protocol-https";
      } else if (currentTabUrl.startsWith("http://")) {
        protocolBadge.textContent = "HTTP";
        protocolBadge.className = "protocol-tag protocol-http";
      } else {
        protocolBadge.textContent = "INTERNAL";
        protocolBadge.className = "protocol-tag";
      }

      // Check if URL is standard inspectable HTTP/HTTPS
      if (!currentTabUrl.startsWith("http://") && !currentTabUrl.startsWith("https://")) {
        urlBox.textContent = "Cannot inspect browser internal pages (requires standard HTTP/HTTPS site).";
        scanBtn.disabled = true;
      }
    } else {
      urlBox.textContent = "Unable to detect active tab context.";
      scanBtn.disabled = true;
    }
  });

  // 2. Open full web console link
  if (openConsoleBtn) {
    openConsoleBtn.addEventListener("click", () => {
      chrome.tabs.create({ url: "http://localhost:5173" });
    });
  }

  // 3. Scan button click handler
  scanBtn.addEventListener("click", async () => {
    if (!currentTabUrl) return;

    scanBtn.disabled = true;
    loader.style.display = "block";
    resultBox.style.display = "none";
    errorBox.style.display = "none";

    let pageHtml = "";

    // Extract rendered DOM from the active tab context
    try {
      const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (activeTab && activeTab.id) {
        const scriptResults = await chrome.scripting.executeScript({
          target: { tabId: activeTab.id },
          func: () => document.documentElement.outerHTML,
        });
        if (scriptResults && scriptResults[0] && scriptResults[0].result) {
          pageHtml = scriptResults[0].result;
        }
      }
    } catch (scriptErr) {
      console.warn("Direct DOM extraction failed; backend crawler will fetch directly:", scriptErr);
    }

    try {
      const response = await fetch(`${BACKEND_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: currentTabUrl, html: pageHtml }),
      });

      if (!response.ok) {
        throw new Error(`Server returned status HTTP ${response.status}`);
      }

      const data = await response.json();

      // Configure badge style
      threatBadge.textContent = `${data.prediction} : ${data.risk_level}`;
      let badgeClass = "badge badge-safe";
      let meterColor = "var(--safe)";

      if (data.risk_score > 20 && data.risk_score <= 60) {
        badgeClass = "badge badge-warn";
        meterColor = "var(--warn)";
      } else if (data.risk_score > 60) {
        badgeClass = "badge badge-danger";
        meterColor = "var(--danger)";
      }

      threatBadge.className = badgeClass;
      threatScore.textContent = data.risk_score;
      threatScore.style.color = meterColor;

      meterFill.style.width = `${data.risk_score}%`;
      meterFill.style.backgroundColor = meterColor;

      confidenceText.textContent = `Confidence: ${data.confidence}% (${data.risk_level})`;

      // Populate SHAP reasons
      reasonsList.innerHTML = "";
      if (data.reasons && data.reasons.length > 0) {
        data.reasons.forEach((reason) => {
          const li = document.createElement("li");
          const tag = document.createElement("span");
          tag.className = "reason-tag";

          if (data.prediction === "Phishing") {
            tag.textContent = "CRIT";
            tag.style.color = "var(--danger)";
            li.style.borderLeftColor = "var(--danger)";
          } else {
            tag.textContent = "PASS";
            tag.style.color = "var(--safe)";
            li.style.borderLeftColor = "var(--safe)";
          }

          const textSpan = document.createElement("span");
          textSpan.textContent = reason;

          li.appendChild(tag);
          li.appendChild(textSpan);
          reasonsList.appendChild(li);
        });
      }

      resultBox.style.display = "block";

      // Notify background service worker to update tab badge
      chrome.runtime.sendMessage({
        action: "updateBadge",
        score: data.risk_score,
        prediction: data.prediction,
      });

    } catch (err) {
      console.error(err);
      errorBox.textContent = "Backend service unreachable on http://localhost:8000. Start the FastAPI backend server to inspect this page.";
      errorBox.style.display = "block";
    } finally {
      scanBtn.disabled = false;
      loader.style.display = "none";
    }
  });
});
