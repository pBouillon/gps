import sys
from collections import Counter
from json import loads
from requests import get
from time import sleep
from argparse import ArgumentParser

# MIT License
#
# Copyright (c) 2018 Pierre Bouillon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

GITHUB_API_URL = 'https://api.github.com/'
GITHUB_API_NF = 'Not Found'

GITHUB_API_HOLD = 60 * 31
GITHUB_API_HOLD_SLICE = 60

REQUEST_PER_USE = 2
REQUEST_WARN_TRIG = 10


class Gps:
    """References Gps

    Attributes:
        __summary  (dict)    : main info of a GitHub profile
        __lang_c   (Counter) : repos count per language
        __requests (int)     : remaining requests
    """

    def __init__(self):
        """ Gps constructor
        """
        self.__summary = {}
        self.__lang_c = Counter()
        self.__requests = 0

        self.__update_lim()

    @staticmethod
    def __start_timer() -> None:
        """
        """
        cpt = GITHUB_API_HOLD

        print('Unable to reach API, waiting ...')
        while cpt:
            print('{} second(s) left'.format(cpt))
            sleep(GITHUB_API_HOLD_SLICE)
            cpt -= GITHUB_API_HOLD_SLICE

    def __update_lim(self) -> None:
        """ Updates the request limit
        """
        lim = get(GITHUB_API_URL + "rate_limit")
        lim = loads(lim.text or lim.content)["rate"]["remaining"]
        self.__requests = int(lim)

    def __get_usr_info(self, url: str) -> None:
        """ Gather the GitHub user infos

        Locally updates the requests count
        If possible, gather information into __summary
        Else exits

        Parameter:
            url (str) : GitHub API url for the profile
        """
        self.__requests -= 1
        req = get(url)
        profile_info = loads(req.text or req.content)

        try:
            self.__summary['user'] = profile_info['login']
            self.__summary['name'] = profile_info['name']
            self.__summary['bio'] = profile_info['bio']
            self.__summary['since'] = profile_info['created_at']
        except KeyError:
            if profile_info['message'] == GITHUB_API_NF:
                exit('Cannot find this profile')
            exit('Something went wrong...')

    def __get_usr_repo(self, url: str) -> None:
        """ Gather user's repos infos

        Localy updates the requests count
        Then increment the counter with repos infos

        Parameter:
            url (str) : GitHub API url for the profile
        """
        self.__requests -= 1
        req = get(url)
        repos_info = loads(req.text or req.content)

        self.__lang_c = Counter()
        for repo in repos_info:
            lang = repo['language'] if repo['language'] else 'Unknown'
            self.__lang_c[lang] += 1

    def get_language_count(self) -> Counter:
        """ Getter for __lang_c
        """
        return self.__lang_c

    def get_profile_summary(self) -> dict:
        """ Getter for __summary
        """
        return self.__summary

    def get_remaining_requests(self) -> int:
        """ Getter for __requests
        """
        return self.__requests

    def gps_for(self, username: str) -> tuple:
        """ Get info on a specific profile

        Ensure Gps can perform requests
        Then gather information

        Parameter:
            username (str) : searched user

        Returns:
            (tuple) : github user's info, counter per language
        """
        if self.__requests - REQUEST_PER_USE <= 0:
            self.__start_timer()
            self.__update_lim()
        if self.__requests < REQUEST_WARN_TRIG:
            print(
                'WARNING: {} requests remaining.'
                .format(self.__requests)
            )

        self.__get_usr_info(GITHUB_API_URL + 'users/' + username)
        self.__get_usr_repo(GITHUB_API_URL + 'users/' + username + '/repos')

        return self.__summary, self.__lang_c

    def formatted_res(self) -> str:
        """ Format intern results and returns it

        Return:
            (str) : formatted result for display
        """
        total_rep = sum(self.__lang_c.values())

        msg = '\nUser {}'
        if self.__summary['name'] is None:
            msg = msg.format(self.__summary['user'])
        else:
            msg += ' ({})'
            msg = msg.format(
                self.__summary['name'],
                self.__summary['user']
            )
        msg += ':\n'

        msg += '\t| '
        if self.__summary['bio'] is None:
            msg += '<no bio provided>\n'
        else:
            msg += '{}\n'
            msg = msg.format(self.__summary['bio'])

        msg += '\t| Registered since {}\n'
        msg += '\t| {} public '
        msg += 'repositories\n' if total_rep > 1 else 'repository\n'
        msg += '\n'

        msg = msg.format(
            self.__summary['since'][:10],
            total_rep
        )

        if len(self.__lang_c.keys()) > 0:
            msg += 'Repositories summary:\n'

            sorted_rep = {}
            for lang, cpt in self.__lang_c.most_common():
                if cpt not in sorted_rep:
                    sorted_rep[cpt] = []
                sorted_rep[cpt].append(lang)

            for tot, langs in sorted_rep.items():
                msg += '\t| x{} '
                msg += 'repos ' if tot > 1 else 'repo '
                msg += 'written in :\n'
                msg = msg.format(tot)
                for lang in sorted(langs):
                    msg += '\t|\t* ' + lang + '\n'
                msg += '\t|\n'
        else:
            msg += 'This user does not have any public repository\n'

        return msg.expandtabs(4)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("username", nargs="?", type=str,
        help="Your GitHub profile name")
    args = parser.parse_args()
        
    if not args.username:
        print("ERROR: No username was provided!")
        sys.exit(1)

    g = Gps()
    g.gps_for(args.username)

    print(g.formatted_res())
