// ========================================
// 🎲 랜덤 페이지 이동 기능
// ========================================
async function goToRandomPage() {
  try {
    // pages.json에서 모든 페이지 목록 가져오기
    const response = await fetch('/pages.json');
    if (!response.ok) {
      throw new Error('pages.json을 불러올 수 없습니다.');
    }
    const data = await response.json();
    const pages = data.pages;
    
    if (pages.length === 0) {
      alert('랜덤으로 이동할 페이지가 없습니다.');
      return;
    }
    
    // 현재 페이지와 다른 페이지로 이동
    const currentPath = window.location.pathname;
    let randomPage;
    let attempts = 0;
    
    do {
      const randomIndex = Math.floor(Math.random() * pages.length);
      randomPage = '/' + pages[randomIndex];
      attempts++;
    } while (randomPage === currentPath && attempts < 10 && pages.length > 1);
    
    // 페이지 이동
    window.location.href = randomPage;
  } catch (error) {
    console.error('랜덤 페이지 로드 실패:', error);
    alert('랜덤 페이지를 불러오는데 실패했습니다.');
  }
}

// 키보드 단축키: Shift + R 로 랜덤 페이지 이동
document.addEventListener('keydown', function(e) {
  if (e.shiftKey && e.key === 'R' && !e.ctrlKey && !e.altKey && !e.metaKey) {
    // 입력 필드에서는 동작하지 않음
    if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
      e.preventDefault();
      goToRandomPage();
    }
  }
});

// ========================================
// first-hidden-text
// ========================================
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
