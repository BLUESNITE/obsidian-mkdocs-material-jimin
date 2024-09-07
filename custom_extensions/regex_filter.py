import re
from mkdocs.plugins import BasePlugin
from jinja2 import Environment

class RegexFilterPlugin(BasePlugin):
    def on_env(self, env: Environment, **kwargs):
        # regex_replace 필터 추가
        def regex_replace(s, pattern, replacement):
            return re.sub(pattern, replacement, s)
        
        env.filters['regex_replace'] = regex_replace
