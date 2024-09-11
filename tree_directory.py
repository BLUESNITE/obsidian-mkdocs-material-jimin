import os

# 탐색할 디렉토리 경로 설정
root_dir = "C:\\project\\blog\\obsidian-mkdocs-material-jimin\\docs"  # 여기에 탐색할 최상위 폴더 경로 입력

# 제외할 폴더 이름 리스트
exclude_folders = ['stylesheets', '_topdown']

def get_nav_structure(root_dir):
    nav_structure = []
    # Home: index.md 항목 고정
    nav_structure.append("- Home: index.md")
    
    for root, dirs, files in os.walk(root_dir):
        # 제외할 폴더를 필터링
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        
        # 현재 경로의 상대 경로를 구함
        rel_path = os.path.relpath(root, root_dir)
        depth = rel_path.count(os.sep) + 1  # 뎁스 카운팅
        folder_name = os.path.basename(root)
        
        # 최상위 디렉토리는 제외하고 서브 디렉토리부터 처리
        if root != root_dir:
            # index.md 파일 처리
            if 'index.md' in files:
                nav_structure.append(f"{'  ' * depth}- {rel_path}:")
                nav_structure.append(f"{'  ' * (depth + 1)}- {rel_path}/index.md")
            
            for file in files:
                if file.endswith('.md') and file != 'index.md':
                    # .md 파일 경로 처리
                    file_name = os.path.splitext(file)[0]
                    nav_structure.append(
                        f"{'  ' * (depth + 1)}- {file_name}: {rel_path}/{file}"
                    )
    
    return nav_structure

def print_nav_structure(nav_structure):
    for line in nav_structure:
        print(line)

if __name__ == "__main__":
    nav_structure = get_nav_structure(root_dir)
    print_nav_structure(nav_structure)
