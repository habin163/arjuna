# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Data Generator

This module contains classes and functions that generate data.
'''

import uuid
import random
from mimesis import Person
from mimesis import Address
from mimesis import locales
from mimesis import Text

Locales = locales

class _gen:
    pass

class processor:
    '''
        Processes data by calling the provided callable with provided arguments.

        Arguments:
            callable: The callable to be called in processing.
            *args: Arbitrary positional args to be passed to the callable.

        Keyword Arguments:
            **kwargs: Arbitrary keyword arguments to tbe passed to the callable.
    '''

    def __init__(self, callable, *args, **kwargs):
        self.__callble = callable
        self.__args = args
        self.__kwargs = kwargs

    def process(self, data):
        '''
            Processes data in the provided data object by calling the callable with arguments provided in constructor.

            Arguments:
                data: Data object
        '''
        if type(self.__callble) is str:
            return getattr(data, self.__callble)(*self.__args, **self.__kwargs)
        else:
            return self.__callble(data_iterator, *self.__args, **self.__kwargs)  

class composer:
    '''
        Combines data in an iterable by calling the provided callable with provided arguments.

        Arguments:
            callable: The callable to be called in composing.
            *args: Arbitrary positional args to be passed to the callable.

        Keyword Arguments:
            **kwargs: Arbitrary keyword arguments to tbe passed to the callable.
    '''

    def __init__(self, callable, *args, **kwargs):
        self.__callble = callable
        self.__args = args
        self.__kwargs = kwargs

    def compose(self, data_iter):
        '''
            Combine data in the provided iterable by calling the callable with arguments provided in constructor.

            Arguments:
                data_iter: Data iterable
        '''
        return self.__callble(data_iter, *self.__args, **self.__kwargs)  

def _same(in_data):
    return in_data

class generator(_gen):
    '''
        Generate data by calling the provided callable with provided arguments.

        Arguments:
            callable: The callable to be called in composing. By default, same generated object is returned.
            *args: Arbitrary positional args to be passed to the callable.

        Keyword Arguments:
            processor: This callable is called after data is generated by passing generated data as argument. Useful for data transformation of any kind. If its type is string, it is assumed to be a method of the data which the data callable generated.
            **kwargs: Arbitrary keyword arguments to tbe passed to the callable.
    '''

    def __init__(self, callable, *args, processor=_same, **kwargs):
        self.__callble = callable
        self.__args = args
        self.__kwargs = kwargs
        self.__processor = processor

    def generate(self):
        '''
            Generate data by calling the callable with arguments provided in constructor.

            After generation the coverter callable is called with this data before returning the data.
        '''
        data = self.__callble(*self.__args, **self.__kwargs)
        if type(self.__processor) is str:
            return getattr(data, self.__processor)()
        elif isinstance(self.__processor, processor):
            return self.__processor.process(data)
        else:
            return self.__processor(data)

class composite(_gen):
    '''
        Composite Data Generator.

        Generate data by composing the output of all generators, callables or static data.

        Arguments:
            *generators_or_data: Arbitrary generators, functions or static data objects.

        Keyword Arguments:
            composer: This callable is called after data sequence is generated by passing generated data sequence as argument. Useful for data transformation of any kind.
    '''

    def __init__(self, *generators_or_data, composer=_same):
        self.__generators_or_data = generators_or_data
        self.__composer = composer

    def generate(self):
        '''
            Generate data by composing the output of all generators, callables or static data.
            
            The composer callable is called after data sequence is generated by passing generated data sequence as argument. Useful for data transformation of any kind.
        '''
        out = list()
        for gen_or_data in self.__generators_or_data:
            if hasattr(gen_or_data, '__call__'):
                out.append(gen_or_data())
            elif isinstance(gen_or_data, generator):
                out.append(gen_or_data.generate())
            else:
                out.append(gen_or_data)

        if isinstance(self.__composer, composer):
            return self.__composer.compose(out)
        else:
            return self.__composer(out)

class Random:
    '''
        Provides methods to create random strings and numbers of different kinds.
    '''

    @classmethod
    def ustr(cls, *, prefix: str=None) -> str:
        '''
            Generate a unique UUID string

            Keyword Arguments:
                prefix: (Optional) prefix to be added to the generated UUID string.

            Returns:
                A string that is unique for current session.
        '''
        prefix = prefix and prefix + "-" or ""
        return "{}{}".format(prefix, uuid.uuid4())

    @classmethod
    def first_name(cls, *, locale=Locales.EN):
        '''
            Generate a first name.

            Keyword Arguments:
                locale: (Optional) locale for generating first name

            Returns:
                A generated first name
        '''
        return Person(locale).first_name()

    @classmethod
    def last_name(cls, *, locale=Locales.EN):
        '''
            Generate a last name.

            Keyword Arguments:
                locale: (Optional) locale for generating last name

            Returns:
                A generated last name
        '''
        return Person(locale).last_name()

    @classmethod
    def name(cls, *, locale=Locales.EN):
        '''
            Generate a full name (first name and last name).

            Keyword Arguments:
                locale: (Optional) locale for generating phone number

            Returns:
                A generated full name
        '''
        return "{} {}".format(cls.first_name(locale=locale), cls.last_name(locale=locale))

    @classmethod
    def phone(cls, *, locale=Locales.EN):
        '''
            Generate a phone number.

            Keyword Arguments:
                locale: (Optional) locale for generating phone number

            Returns:
                A generated phone number
        '''
        return cls.first_name(locale=locale)

    @classmethod
    def email(cls, *, locale=Locales.EN):
        '''
            Generate an email address.

            Keyword Arguments:
                locale: (Optional) locale for generating email address

            Returns:
                A generated email address
        '''
        return Person(locale).email()

    @classmethod
    def street_name(cls, *, locale=Locales.EN):
        '''
            Generate a street name

            Keyword Arguments:
                locale: (Optional) locale for generating street name

            Returns:
                A generated street name
        '''
        return Address(locale).street_name()

    @classmethod
    def street_number(cls, *, locale=Locales.EN):
        '''
            Generate a street number

            Keyword Arguments:
                locale: (Optional) locale for generating street number

            Returns:
                A generated street number
        '''
        return Address(locale).street_number()

    @classmethod
    def house_number(cls, *, locale=Locales.EN):
        '''
            Generate a house number

            Keyword Arguments:
                locale: (Optional) locale for generating house number

            Returns:
                A generated house number
        '''
        return cls.street_number(locale=locale)

    @classmethod
    def postal_code(cls, *, locale=Locales.EN):
        '''
            Generate a postal code

            Keyword Arguments:
                locale: (Optional) locale for generating postal code

            Returns:
                A generated postal code
        '''
        return Address(locale).postal_code()

    @classmethod
    def city(cls, *, locale=Locales.EN):
        '''
            Generate a city name.

            Keyword Arguments:
                locale: (Optional) locale for generating city name

            Returns:
                A generated city name
        '''
        return Address(locale).city()

    @classmethod
    def country(cls, *, locale=Locales.EN):
        '''
            Generate a country name

            Keyword Arguments:
                locale: (Optional) locale for generating country name

            Returns:
                A generated country name
        '''
        return Address(locale).country()

    @classmethod
    def sentence(cls, *, locale=Locales.EN):
        '''
            Generate a sentence

            Keyword Arguments:
                locale: (Optional) locale for generating sentence

            Returns:
                A generated sentence
        '''
        return Text(locale).sentence()

    @classmethod
    def fixed_length_number(cls, *, length):
        '''
            Generate a fixed length number

            Keyword Arguments:
                length: Number of digits in generated number.

            Returns:
                A generated fixed length number

            Note:
                A number of minimum length 1 is always generated.
        '''
        arr0 = [str(random.randint(1,9))]
        arr = []
        if length >= 2:
            arr = [str(random.randint(0,9)) for i in range(length-1)]
        arr0.extend(arr)
        return int("".join(arr0))

    @classmethod
    def int(cls, *, end, begin=0):
        '''
            Generate a random integer.

            Keyword Arguments:
                end: (inclusive) upper limit for the integer
                begin: (inclusive) lower limit for the integer. Default is 0.

            Returns:
                A generated integer
        '''
        return random.randint(begin, end)

        
