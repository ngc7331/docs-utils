"""
This extension finds and removes all include block, which is introduced by pandoc's 
[include-files filter](https://github.com/pandoc-ext/include-files).
"""

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.extensions.fenced_code import FencedBlockPreprocessor
from markdown.extensions.attr_list import get_attrs_and_remainder

class IncludeBlockPreprocessor(FencedBlockPreprocessor):
    def run(self, lines: list[str]) -> list[str]:
        """
        This function is modified from the function of the same name in markdown.
        extensions.fenced_code.FencedBlockPreprocessor.

        The licensing information for the original code is as follows:
            Original code Copyright 2007-2008 [Waylan Limberg](http://achinghead.com/).
            All changes Copyright 2008-2014 The Python Markdown Project
            License: [BSD](https://opensource.org/licenses/bsd-license.php)
        """

        text = "\n".join(lines)
        index = 0
        while 1:
            m = self.FENCED_BLOCK_RE.search(text, index)
            if m:
                lang, id, classes, config = None, '', [], {}
                if m.group('attrs'):
                    attrs, remainder = get_attrs_and_remainder(m.group('attrs'))
                    if remainder:  # Does not have correctly matching curly braces, so the syntax is invalid.
                        index = m.end('attrs')  # Explicitly skip over this, to prevent an infinite loop.
                        continue
                    id, classes, config = self.handle_attrs(attrs)
                    if len(classes):
                        lang = classes.pop(0)

                if lang == 'include':
                    # replace the whole include block with a \n
                    text = f'{text[:m.start()]}\n{text[m.end():]}'
                    index = m.start() + 1
                else:
                    # not include block, skip it.
                    index = m.end()
            else:
                break
        return text.split("\n")

class RemoveIncludeExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(IncludeBlockPreprocessor(md, self.getConfigs()), 'remove_include', 26)

def makeExtension(**kwargs):
    return RemoveIncludeExtension(**kwargs)
