import sys
from pathlib import Path

def on_config(config):
    sys.path.append(str(Path(__file__).parent))

# Auto Index 기능
EXCLUDE_DIRS = ['blog', 'stylesheets', '_topdown', '__pycache__']
EXCLUDE_FILES = ['.DS_Store', 'index.md']

def on_page_markdown(markdown, page, config, files):
    """index.md 파일에 하위 디렉토리/파일 목록을 자동 추가"""
    
    # index.md 파일이 아니면 처리하지 않음
    if not page.file.name.endswith('index.md'):
        return markdown
        
    # 현재 파일의 소스 경로
    src_path = Path(page.file.abs_src_path)
    current_dir = src_path.parent
    
    # docs 디렉토리 확인
    docs_dir = Path(config['docs_dir'])
    
    # 하위 항목 수집
    items = []
    
    try:
        for item in sorted(current_dir.iterdir()):
            # 숨김 파일 및 제외 항목 스킵
            if item.name.startswith('.') or item.name in EXCLUDE_FILES:
                continue
                
            if item.is_dir():
                # 제외 디렉토리 스킵
                if item.name in EXCLUDE_DIRS:
                    continue
                # 하위 디렉토리 추가
                items.append({
                    'name': item.name,
                    'path': item,
                    'type': 'dir'
                })
            elif item.is_file() and item.suffix == '.md':
                # 마크다운 파일 추가
                items.append({
                    'name': item.stem,
                    'path': item,
                    'type': 'file'
                })
    except (PermissionError, OSError):
        return markdown
        
    # 자동 인덱스 생성
    if not items:
        return markdown
        
    # 기존 마크다운 유지
    auto_index_lines = [markdown, '']
    
    # 목차가 이미 있는지 확인
    if '## 목차' not in markdown:
        auto_index_lines.append('## 목차')
        auto_index_lines.append('')
    
    for item in items:
        try:
            rel_path = item['path'].relative_to(docs_dir)
            # Windows 경로를 URL 경로로 변환
            url_path = str(rel_path).replace('\\', '/')
            
            if item['type'] == 'dir':
                link = f"[📁 {item['name']}](/{url_path}/)"
            else:
                # .md 확장자 제거
                url_path = url_path.replace('.md', '')
                link = f"[📄 {item['name']}](/{url_path})"
            
            auto_index_lines.append(f"- {link}")
        except (ValueError, OSError):
            continue
    
    auto_index_lines.append('')
    
    return '\n'.join(auto_index_lines)