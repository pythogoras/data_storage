#!/usr/bin/env python3.10.8
# -*- coding: utf-8 -*-
'''

Create an XML file with nested elements and use the XPath search language.
Try to search for the contents according to the created XML document,complicating your requests and adding new elements, if necessary.

author:: @vimer
'''
import re
from xml.etree import ElementTree as etr

_DATA_PATH = 'data_xml/pacients.xml'


class SearchError(Exception):
    pass


class Search:
    def __init__(self) -> None:
        self.__body = etr.parse(_DATA_PATH).getroot()

    def __valid_full_name(self, word: str) -> bool:
        regex = r'^[A-Z][a-z]+\w[A-Z][a-z]+$'
        valid = re.search(regex, word)
        return bool(valid)

    def __valid_gender(self, word: str) -> bool:
        valid = False
        if word == 'M' or word == 'F':
            valid = True
        return valid

    def __valid_age(self, word: str) -> bool:
        regex = r'^/d{1,2}$'
        valid = re.search(regex, word)
        return valid

    def __element_search(self, word: str, tag: str, name: str = None) -> None:
        persons = self.__body.findall('.//{tag}[.="{word}"]..')
        for persona in persons:
            special = persona.tag
            first_name = persona.findtext('first_name')
            last_name = persona.findtext('last_name')
            gender = persona.findtext('gender')
            age = persona.findtext('age')
            if name is None or name == first_name:
                print(f'{special}: {first_name} {last_name}; {gender}; {age}')

    def _search(self, word: str) -> None:
        if self.__valid_full_name(word):
            first_name, last_name = word.split(' ')
            self.__element_search(last_name, 'last_name', first_name)
        elif self.__valid_gender(word):
            self.__element_search(word, 'gender')
        elif self.__valid_age(word):
            self.__element_search(word, 'age')
        else:
            raise SearchError('not correct search word!')


if __name__ == '__main__':
    search = Search()
    while True:
        search_word = input('>>> ')
        try:
            if re.search(r'^pacient :: ', search_word):
                pass
            elif re.search(r'^doctor :: ', search_word):
                pass
            elif re.search(r'^disease :: ', search_word):
                pass
            else:
                search._search(search_word)
        except SearchError as error:
            print(error)
