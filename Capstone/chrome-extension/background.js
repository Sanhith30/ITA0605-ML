// Background Service Worker for Manifest V3 Chrome Extension

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "updateBadge") {
    const { score } = message;

    let badgeText = "OK";
    let badgeColor = "#166534"; // Forest green

    if (score > 20 && score <= 60) {
      badgeText = "WARN";
      badgeColor = "#92400e"; // Amber
    } else if (score > 60) {
      badgeText = "RISK";
      badgeColor = "#991b1b"; // Crimson
    }

    // Update extension badge text and background color
    chrome.action.setBadgeText({ text: badgeText });
    chrome.action.setBadgeBackgroundColor({ color: badgeColor });

    sendResponse({ status: "success" });
  }
  return true;
});
