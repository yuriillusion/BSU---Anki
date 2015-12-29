from __future__ import unicode_literals
import os
import re

TYPES = ["definition", "property", "theorem", "statement"]
REGEX_TEMPLATE = r'(?<=\\begin{{{0}}})[\w\W]+?(?=\\end{{{0}}})'
CARD_TEMPLATE = u'{} "[latex]{}[/latex]" "functional_analysis {}"\n'
COUNTER = 0


def gen_cards(text):
    global COUNTER
    for type in TYPES:
        matcher = re.compile(REGEX_TEMPLATE.format(type))
        raw_tokens = matcher.finditer(text)
        for raw_token in raw_tokens:
            answer_field = re.sub(u'\\label{[\w\W]+?}', u'', unicode(raw_token.group(0).decode('cp1251')))
            yield CARD_TEMPLATE.format(str(COUNTER), answer_field, type)
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