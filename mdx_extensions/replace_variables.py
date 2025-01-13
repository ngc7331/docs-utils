from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension


class ReplaceVariablesProcessor(InlineProcessor):
    def __init__(self, pattern, variables, md=None):
        self.variables = variables
        super(ReplaceVariablesProcessor, self).__init__(pattern, md)

    def handleMatch(self, m, data):
        key = m.group(1)
        if key in self.variables:
            return self.variables[key], m.start(0), m.end(0)
        return None, None, None

class ReplaceVariablesExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'variables' : [{}, "varibles to replace"],
        }
        super(ReplaceVariablesExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        META_VAR_PATTERN = r'\{\{(.*?)\}\}'  # like {{xxxx}}
        md.inlinePatterns.register(ReplaceVariablesProcessor(META_VAR_PATTERN, self.getConfig('variables'), md), 'meta-var', 175)

def makeExtension(**kwargs):
    return ReplaceVariablesExtension(**kwargs)
