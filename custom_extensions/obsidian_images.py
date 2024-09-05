import re
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from xml.etree import ElementTree as etree

class ObsidianImageProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        image_name = m.group(1)
        
        # 이미지 경로를 적절히 변환
        # 예: 'images/' 디렉토리에 이미지가 있다고 가정
        image_path = f"_topdown/{image_name}"
        
        img = etree.Element('img')
        img.set('src', image_path)
        img.set('alt', image_name)
        
        return img, m.start(0), m.end(0)

class ObsidianImageExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(ObsidianImageProcessor(r'!\[\[(.*?)\]\]'), 'obsidian_image', 175)

def makeExtension(**kwargs):
    return ObsidianImageExtension(**kwargs)