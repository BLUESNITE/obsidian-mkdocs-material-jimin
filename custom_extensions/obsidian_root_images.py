import re
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from xml.etree import ElementTree as etree

class ObsidianImageProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        image_data = m.group(1).split('|')
        image_root = image_data[0]
        image_name = image_data[1]
        image_path = f"stylesheets/_topdown/{image_root}/{image_name}"

        # 옵션이 있는 경우 처리
        bg_color = image_data[2] if len(image_data) > 2 and image_data[2] != '' else None  # 값이 있을 때만 사용
        width = image_data[3] if len(image_data) > 3 and image_data[3] != '' else None  # 값이 있을 때만 사용
        height = image_data[4] if len(image_data) > 4 and image_data[4] != '' else None  # 값이 있을 때만 사용
        css_class = image_data[5] if len(image_data) > 5 and image_data[5] != '' else None  # 클래스 값이 있을 때만 사용

        img = etree.Element('img')
        img.set('src', image_path)
        img.set('alt', image_name)
        
        style = '' # 스타일 설정
        if bg_color:
            style += f'background-color: {bg_color};'
        if width:
            style += f' width: {width};'
        if height:
            style += f' height: {height};'
        if style:  # 스타일이 있을 때만 추가
            img.set('style', style)

        if css_class: # 클래스가 있을 경우 class 속성 추가
            img.set('class', css_class)
        
        return img, m.start(0), m.end(0)

class ObsidianImageExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(ObsidianImageProcessor(r'@\[\[(.*?)\]\]'), 'obsidian_root_images', 175)

def makeExtension(**kwargs):
    return ObsidianImageExtension(**kwargs)