import re
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from xml.etree import ElementTree as etree

class ObsidianCalloutsProcessor(BlockProcessor):
    RE = re.compile(r'^\s*>\s*\[!(\w+)\]\s*(.*)')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            callout_type = m.group(1).lower()
            title = m.group(2)

            div = etree.SubElement(parent, 'div')
            div.set('class', f'admonition {callout_type}')
            
            title_elem = etree.SubElement(div, 'p')
            title_elem.set('class', 'admonition-title')
            title_elem.text = title

            content = []
            for line in block.split('\n')[1:]:
                if line.startswith('> '):
                    content.append(line[2:])
                else:
                    break
            
            if content:
                self.parser.parseChunk(div, '\n'.join(content))

        return True

class ObsidianCalloutsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(ObsidianCalloutsProcessor(md.parser), 'obsidian_callouts', 175)

def makeExtension(**kwargs):
    return ObsidianCalloutsExtension(**kwargs)