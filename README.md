# gps
Github Profile Summary (gps) is a small command-line tool 
to get an overview of a Github user's activity

Inspired by [this cool repo](https://profile-summary-for-github.com/search), 
it's a shorter version that does not require you to browse on the internet.

## usage

```shell
~$ pip install github_profile_summary

~$ python -m github_profile_summary
usage: python3 gps.py username

~$ python -m github_profile_summary a_non_existing_user
Cannot find this profile

~$ python -m github_profile_summary pBouillon
Profile's name: pBouillon

User Pierre Bouillon (pBouillon):
    | Developer, student and tech enthusiast.
    | Registered since 2016-10-05
    | 30 public repositories

Repositories summary:
    | x17 repos written in :
    |   * Python
    |
    | x4 repos written in :
    |   * Java
    |
    | x3 repos written in :
    |   * Unknown
    |
    | x2 repos written in :
    |   * JavaScript
    |
    | x1 repo written in :
    |   * C
    |   * C++
    |   * CSS
    |   * HTML
    |
```

You can also get only specify part of the user's infos
```Python
g = Getter()
g.get_remaining_requests() # check how many requests you can perform

g.gps_for ('user')
g.formated_res()        # returns all infos in a human readable str
g.get_profile_summary() # get infos on the user as a dict
g.get_language_count()  # get repos per language in a collections.Counter
```

## improvements
- [x] better handling for None values (Bio, Repos, Real Name, etc.)
- [x] better handling on API limit reach
- [x] show sum of all repos
- [x] better display for repo per language
- [x] languages sorted by alphabetical order on display

## contributions
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Contributions are welcome !
