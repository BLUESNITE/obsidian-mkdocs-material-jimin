// first-hidden-text
document.addEventListener("DOMContentLoaded", function () {
  function updateDataTitles() {
    document.querySelectorAll(".first-hidden-text").forEach(function (element) {
      let text = element.getAttribute("data-first");
      if (text) {
        let cleanedText = text.replace(/[0-9]+\.\s*/, ""); // 숫자와 점 제거
        element.setAttribute("data-title", cleanedText);
      }
    });
  }

  // Initial update when DOM is loaded
  updateDataTitles();

  // Optional: Update when navigating via JavaScript (e.g., on-click or AJAX content)
  document.body.addEventListener("click", function (event) {
    if (event.target.matches("a, .some-other-selector")) {
      setTimeout(updateDataTitles, 100); // Allow time for content to load/update
    }
  });

  // Optional: Watch for dynamic content changes (e.g., from AJAX)
  const observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      if (mutation.type === "childList") {
        updateDataTitles();
      }
    });
  });

  observer.observe(document.body, { childList: true, subtree: true });
});
