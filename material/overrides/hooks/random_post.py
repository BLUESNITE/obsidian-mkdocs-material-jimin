"""
랜덤 블로그 글 기능을 위한 MkDocs Hook
빌드 시 모든 문서 경로를 JSON 파일로 저장합니다.
"""
import json
import os
from pathlib import Path


def on_post_build(config, **kwargs):
    """빌드 후 모든 페이지 경로를 JSON 파일로 생성"""
    site_dir = config['site_dir']
    docs_dir = config['docs_dir']
    
    all_pages = []
    excluded_files = {'index.md', 'SAMPLE.MD'}
    excluded_dirs = {'_topdown', 'stylesheets', 'assets', '__pycache__'}
    
    for root, dirs, files in os.walk(docs_dir):
        # 제외할 디렉토리 필터링
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            if file.endswith('.md') and file not in excluded_files:
                rel_path = os.path.relpath(os.path.join(root, file), docs_dir)
                # URL 경로로 변환 (Windows 호환)
                url_path = rel_path.replace('.md', '/').replace('\\', '/')
                all_pages.append(url_path)
    
    # 페이지 정보를 JSON으로 저장
    output_data = {
        "pages": all_pages,
        "count": len(all_pages)
    }
    
    json_path = os.path.join(site_dir, 'pages.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Random post: {len(all_pages)}개의 페이지 경로가 pages.json에 저장되었습니다.")


def on_env(env, config, files, **kwargs):
    """Jinja2 환경에 랜덤 페이지 정보 추가 (템플릿에서 사용 가능)"""
    docs_dir = config['docs_dir']
    all_pages = []
    excluded_files = {'index.md', 'SAMPLE.MD'}
    
    for file in files:
        src_path = file.src_path
        if src_path.endswith('.md') and os.path.basename(src_path) not in excluded_files:
            url_path = src_path.replace('.md', '/').replace('\\', '/')
            all_pages.append(url_path)
    
    # 템플릿에서 {{ random_pages }} 로 접근 가능
    env.globals['random_pages'] = all_pages
    env.globals['random_pages_count'] = len(all_pages)
    
    return env
