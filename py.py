from __future__ import unicode_literals
import os
import re

REGEX_FOR_DEFINITIONS = r'(?<=\\begin{definition})[\w\W]+?(?=\\end{definition})'
REGEX_FOR_PROPERTIES = r'(?<=\\begin{property})[\w\W]+?(?=\\end{property})'
REGEX_FOR_THEOREMS = r'(?<=\\begin{theorem})[\w\W]+?(?=\\end{theorem})'
REGEX_FOR_STATEMENTS = r'(?<=\\begin{statement})[\w\W]+?(?=\\end{statement})'

MATCHER = re.compile(REGEX_FOR_DEFINITIONS)
template = u'{} "[latex]{}[/latex]" "functional_analysis definition"\n'
COUNTER = 0


def gen_cards(text):
    global COUNTER
    raw_tokens = MATCHER.finditer(text)
    for raw_token in raw_tokens:
        answer_field = re.sub(u'\\label{[\w\W]+?}', u'', unicode(raw_token.group(0).decode('cp1251')))
        yield template.format(str(COUNTER), answer_field)
        COUNTER += 1


def get_cards(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            with open(os.path.join(root, file)) as f:
                for token in gen_cards(f.read()):
                    yield token


if __name__ == '__main__':
    tokens = get_cards('modified_source')
    with open('result\\cards.txt', 'w') as file:
        for token in tokens:
            file.write(token.encode('utf-8'))