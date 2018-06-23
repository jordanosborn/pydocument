"""Strings utility file."""
import re
from typing import List

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


def search_list(ls: list, search: str) -> int:
    """Search list of strings for first instance of substring.

    Arguments:
        ls {list} -- list to search
        search {str} -- string to search for

    Returns:
        int - returns index of list item that contains the first instance
        of the search string

    """
    index = -1
    for i, s in enumerate(ls):
        if search in s:
            index = i
            break
    return index


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
            text = text.replace(str(n.group(1)), f'\'{i}\'', 1)
        text_split = text.split(splitter)
        for i in range(len(text_split)):
            text_split[i] = text_split[i].strip()
            for j, s in enumerate(strings):
                text_split[i] = text_split[i].replace(f'\'{j}\'', f'\'{s}\'')
        return text_split
    else:
        return ['']


def join_all(ls: List[str], join_char: str) -> str:
    """Join all strings in a list.

    Arguments:
        ls {List[str]} -- list to join in to single string
        join_char {str} -- character to seperate concatenated strings

    Returns:
        str -- return concatenated list

    """
    return ''.join(s + join_char for s in ls)[0:-1]
