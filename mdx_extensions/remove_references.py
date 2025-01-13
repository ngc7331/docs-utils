from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
import re

class RemoveReferencesPreprocessor(Preprocessor):
    def run(self, lines):
        cleaned_lines = [
            re.sub(r'\[@[a-zA-Z0-9:_-]+\]', '', line) for line in lines
        ]
        return cleaned_lines

class RemoveReferencesExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(RemoveReferencesPreprocessor(md), 'remove_references', 29)

def makeExtension(**kwargs):
    return RemoveReferencesExtension(**kwargs)
