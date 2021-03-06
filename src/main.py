from gps import Gps

from argparse import ArgumentParser
from sys import exit as quit

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

if __name__ == '__main__':
    parser = ArgumentParser(prog="gps.py")
    parser.add_argument(
        metavar="profile_name",
        dest="user",
        nargs="?",
        type=str,
        help="Your GitHub profile name"
    )
    args = parser.parse_args()
    user = args.user
    if not user:
        user = input("Profile's name: ")
        
    if len(user) == 0:
        print("ERROR: No username was provided!")
        quit(1)

    g = Gps()
    g.gps_for(user)

    print(g.formatted_res())
