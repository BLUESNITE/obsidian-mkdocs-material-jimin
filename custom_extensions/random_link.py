"""
랜덤 링크 마크다운 확장
~[[random]] 또는 ~[[random|버튼텍스트]] 문법으로 랜덤 페이지 버튼을 삽입합니다.
"""
import re
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from xml.etree import ElementTree as etree


class RandomLinkProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        full_match = m.group(1)
        parts = full_match.split('|')
        
        # 버튼 텍스트 (기본값: 🎲 랜덤 글 읽기)
        button_text = parts[1] if len(parts) > 1 and parts[1] else '🎲 랜덤 글 읽기'
        
        # 버튼 스타일 클래스 (기본값: md-button)
        button_class = parts[2] if len(parts) > 2 and parts[2] else 'md-button md-button--primary'
        
        # 버튼 요소 생성
        button = etree.Element('a')
        button.set('href', 'javascript:void(0)')
        button.set('onclick', 'goToRandomPage()')
        button.set('class', button_class)
        button.set('title', '랜덤 페이지로 이동')
        button.text = button_text
        
        return button, m.start(0), m.end(0)


class RandomLinkExtension(Extension):
    def extendMarkdown(self, md):
        # ~[[random]] 패턴 - 기존 동작하는 패턴과 동일한 구조
        md.inlinePatterns.register(RandomLinkProcessor(r'~\[\[(.*?)\]\]'), 'random_link', 175)


def makeExtension(**kwargs):
    return RandomLinkExtension(**kwargs)
