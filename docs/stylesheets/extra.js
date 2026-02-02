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

// ========================================
// 🔍 검색 링크 기능
// ========================================
document.addEventListener('DOMContentLoaded', function() {
  // 초기 변환
  convertSearchLinks();
  
  // MkDocs Material의 페이지 네비게이션 감지
  const observer = new MutationObserver(function(mutations) {
    convertSearchLinks();
  });
  
  const content = document.querySelector('.md-content');
  if (content) {
    observer.observe(content, { childList: true, subtree: true });
  }
  
  // 검색 링크 클릭 이벤트 (이벤트 위임)
  document.body.addEventListener('click', function(event) {
    const target = event.target.closest('.search-link');
    
    if (target) {
      event.preventDefault();
      event.stopPropagation();
      
      const searchTerm = target.getAttribute('data-search') || target.textContent;
      if (!searchTerm) return;
      
      // 검색 실행
      triggerSearch(searchTerm);
      
      return false;
    }
  }, true);
  
  function convertSearchLinks() {
    const content = document.querySelector('.md-content');
    if (!content) return;
    
    // 모든 텍스트 노드 순회
    const walker = document.createTreeWalker(
      content,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: function(node) {
          // 이미 변환된 링크 내부는 스킵
          if (node.parentElement && node.parentElement.classList.contains('search-link')) {
            return NodeFilter.FILTER_REJECT;
          }
          // [[...]] 패턴이 있는 노드만 처리
          if (node.nodeValue && node.nodeValue.includes('[[') && node.nodeValue.includes(']]')) {
            return NodeFilter.FILTER_ACCEPT;
          }
          return NodeFilter.FILTER_SKIP;
        }
      }
    );
    
    const nodesToReplace = [];
    let node;
    
    while (node = walker.nextNode()) {
      nodesToReplace.push(node);
    }
    
    nodesToReplace.forEach(textNode => {
      const text = textNode.nodeValue;
      const regex = /\[\[([^\]]+)\]\]/g;
      const matches = [...text.matchAll(regex)];
      
      if (matches.length === 0) return;
      
      const fragment = document.createDocumentFragment();
      let lastIndex = 0;
      
      matches.forEach(match => {
        // 매치 앞의 텍스트 추가
        if (match.index > lastIndex) {
          fragment.appendChild(
            document.createTextNode(text.substring(lastIndex, match.index))
          );
        }
        
        // 검색 링크 생성
        const link = document.createElement('a');
        link.href = 'javascript:void(0)';
        link.className = 'search-link';
        link.setAttribute('data-search', match[1]);
        link.textContent = match[1];
        fragment.appendChild(link);
        
        lastIndex = match.index + match[0].length;
      });
      
      // 남은 텍스트 추가
      if (lastIndex < text.length) {
        fragment.appendChild(
          document.createTextNode(text.substring(lastIndex))
        );
      }
      
      // 텍스트 노드를 fragment로 교체
      textNode.parentNode.replaceChild(fragment, textNode);
    });
  }
  
  function triggerSearch(query) {
    // 검색 입력창 직접 찾기
    const searchInput = document.querySelector('[data-md-component="search-query"]') || 
                        document.querySelector('input[placeholder*="검색"]') ||
                        document.querySelector('#__search');
    
    if (searchInput) {
      // 검색창이 닫혀있으면 열기
      const searchLabel = document.querySelector('label[for="__search"]');
      if (searchLabel && !searchInput.value) {
        searchLabel.click();
      }
      
      // 검색어 입력
      setTimeout(() => {
        searchInput.value = query;
        searchInput.focus();
        
        // 검색 트리거
        const inputEvent = new Event('input', { bubbles: true });
        searchInput.dispatchEvent(inputEvent);
        
        const keyEvent = new KeyboardEvent('keyup', { 
          bubbles: true,
          key: 'Enter',
          keyCode: 13
        });
        searchInput.dispatchEvent(keyEvent);
      }, 150);
    }
  }
});
