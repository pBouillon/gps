"""
MIT License

Copyright (c) 2018 Pierre Bouillon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import collections
from collections import Counter

import json
from json import loads

import requests
from requests import get

import time
from time import sleep

GITHUB_API_URL  = 'https://api.github.com/'
GITHUB_API_NF   = 'Not Found'
GITHUB_API_HOLD = 60 * 31

REQUEST_PER_USE = 2 

class Getter :
    def __init__(self) :
        """
        """
        self.__summary  = {}
        self.__lang_c   = Counter()
        self.__requests = 0

        self.__update_lim()

    def __update_lim (self):
            """
            """
            lim = get (GITHUB_API_URL + "rate_limit")
            lim = loads (lim.text or lim.content)["rate"]["remaining"]
            self.__requests = int(lim)

    def __get_usr_info (self, url):
        """
        """
        self.__requests -= 1
        req = get(url)
        profile_info = loads (req.text or req.content)

        try:
            if profile_info['message'] == GITHUB_API_NF:
                exit ('Cannot find this profile')
        except KeyError:
            pass

        self.__summary['user'] = profile_info['login']
        self.__summary['name'] = profile_info['name']
        self.__summary['bio' ] = profile_info['bio' ]
        self.__summary['since'] = profile_info['created_at']

    def __get_usr_repo (self, url):
        """
        """
        self.__requests -= 1
        req = get(url)
        repos_info = loads (req.text or req.content)

        for repo in repos_info :
            lang = repo['language']
            self.__lang_c[lang] += 1

    def gps_for(self, username) :
        """
        """
        if self.__requests - REQUEST_PER_USE <= 0:
            print (
                'Unable to reach API, waiting {} seconds'
                .format(GITHUB_API_HOLD)
            )
            sleep (GITHUB_API_HOLD)
            self.__update_lim()

        self.__get_usr_info (GITHUB_API_URL + 'users/' + username)
        self.__get_usr_repo (GITHUB_API_URL + 'users/' + username + '/repos')

        return (self.__summary, self.__lang_c)

    def show_res(self):
        """
        """
        msg = 'User {} ({}):\n'
        msg+= '\t"{}"\n'
        msg+= '\tRegistered since {}\n\n'
        msg+= 'Repositories per languages:\n'

        msg = msg.format (
                self.__summary['name'],
                self.__summary['user'],
                self.__summary['bio'],
                self.__summary['since'][:10]
            )

        for lang, repos_cpt in self.__lang_c.most_common() :
            if lang is None:
                msg += '\tOther : ' + str(repos_cpt) + '\n'
            else:  
                msg += '\t' + lang + ': ' + str(repos_cpt) + '\n'

        msg = msg.expandtabs(4)
        print (msg)