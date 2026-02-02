#!/usr/bin/env python3
"""
Auto Index Generator
각 디렉토리의 index.md 파일에 하위 항목 목록을 자동으로 추가하는 스크립트
"""
from pathlib import Path

EXCLUDE_DIRS = ['blog', 'stylesheets', '_topdown', '__pycache__', 'site', '.git']
EXCLUDE_FILES = ['.DS_Store', 'index.md']

def generate_index_content(directory: Path, docs_dir: Path, depth: int = 0) -> list:
    """디렉토리의 하위 항목 목록 생성 (재귀적)"""
    items = []
    
    try:
        for item in sorted(directory.iterdir()):
            # 숨김 파일 및 제외 항목 스킵
            if item.name.startswith('.') or item.name in EXCLUDE_FILES:
                continue
                
            if item.is_dir():
                # 제외 디렉토리 스킵
                if item.name in EXCLUDE_DIRS:
                    continue
                items.append({
                    'name': item.name,
                    'path': item,
                    'type': 'dir'
                })
            elif item.is_file() and item.suffix == '.md':
                items.append({
                    'name': item.stem,
                    'path': item,
                    'type': 'file'
                })
    except (PermissionError, OSError) as e:
        print(f"⚠️  {directory}: {e}")
        return []
        
    if not items:
        return []
        
    # 목차 생성
    lines = []
    indent = "  " * depth  # 들여쓰기
    
    for item in items:
        try:
            if item['type'] == 'dir':
                if depth == 0:
                    link = f"#### 📁 {item['name']}"
                else:
                    link = f"{indent}- {item['name']}"
                lines.append(link)
                
                # 하위 디렉토리 재귀 처리
                sub_lines = generate_index_content(item['path'], docs_dir, depth + 1)
                lines.extend(sub_lines)
            else:
                if depth == 0:
                    link = f"#### 📄 {item['name']}"
                else:
                    link = f"{indent}- {item['name']}"
                lines.append(link)
        except (ValueError, OSError):
            continue
    
    return lines

def update_index_file(index_path: Path, docs_dir: Path):
    """index.md 파일 업데이트 (완전히 새로 작성)"""
    directory = index_path.parent
    
    # 새로운 목차 생성
    lines = generate_index_content(directory, docs_dir)
    
    if not lines:
        return False
    
    # 파일 완전히 덮어쓰기
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    
    return True

def main():
    """모든 index.md 파일 업데이트"""
    project_dir = Path(__file__).parent
    docs_dir = project_dir / 'docs'
    
    if not docs_dir.exists():
        print("❌ docs 디렉토리를 찾을 수 없습니다.")
        return
    
    print(f"📁 docs 디렉토리: {docs_dir}")
    print("🔍 index.md 파일 검색 중...\n")
    
    count = 0
    updated = 0
    
    # docs 디렉토리 내의 모든 index.md 찾기
    for index_path in docs_dir.rglob('index.md'):
        # docs/index.md는 제외 (최상위)
        if index_path == docs_dir / 'index.md':
            continue
        
        # 제외 디렉토리 체크
        should_skip = False
        for exclude in EXCLUDE_DIRS:
            if exclude in index_path.parts:
                should_skip = True
                break
        
        if should_skip:
            continue
        
        count += 1
        rel_path = index_path.relative_to(docs_dir)
        
        try:
            if update_index_file(index_path, docs_dir):
                print(f"✅ {rel_path}")
                updated += 1
            else:
                print(f"⏭️  {rel_path} (하위 항목 없음)")
        except Exception as e:
            print(f"❌ {rel_path}: {e}")
    
    print(f"\n📊 총 {count}개 파일 처리, {updated}개 업데이트 완료")

if __name__ == '__main__':
    main()
