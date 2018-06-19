"""Strings utility file."""
import re

char_Set = dict(
    l_dbl_quote=u'\u201C',
    r_dbl_quote=u'\u201D',
    l_sgl_quote=u'\u2018',
    r_sgl_quote=u'\u2019'
)


def strip_list(ls: list) -> list:
    """Strip whitespace from strings in list.

    Arguments:
        arr {list} -- list to be stripped

    Returns:
        list -- Stripped list

    """
    stripped_list = []
    if ls != []:
        for s in ls:
            stripped_list.append(s.strip())
        return stripped_list
    else:
        return ['']


def split_string(text: str, splitter: str = ',') -> list:
    """Split string at splitter when splitter is not enclosed in quotes.

    Arguments:
        string {str} -- string to split

    Keyword Arguments:
        splitter {str} -- splitter character (default: {','})

    Returns:
        list -- split string

    """
    if text != '':
        string_regex = re.compile(r'([{\u2018}][\w\s\S]*?[\u2019]|[\'][\w\s\S]*?[\']|["][\w\s\S]*?["]|[\u201C][\w\s\S]*?[\u201D])')
        strings = []
        for i, n in enumerate(string_regex.finditer(text)):
            strings.append(str(n.group(1)[1:-1]))
            text = text.replace(n.group(1), f'\'{i}\'')
        text_split = text.split(splitter)

        for i, t in enumerate(text_split):
            text_split[i] = text_split[i].strip()
            for j, s in enumerate(strings):
                text_split[i] = t.replace(f'\'{j}\'', f'\'{s}\'')
        return text_split
    else:
        print('hu')
        return ['']
