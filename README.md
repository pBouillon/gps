# gps
Github Profile Summary (gps) is a small command-line tool 
to get an overview of a Github user's activity

Inspired by [this cool repo](https://github-profile-summary.com/), 
it's a shorter version that does not require you to browse on the internet.


## usage

```shell
~$ python gps.py pBouillon

User Pierre Bouillon (pBouillon):
    |Developer, student and tech enthusiast.
    |Registered since 2016-10-05
    |27 public repositories

Repositories per languages:
    Python    : 17
    Unknow    : 2
    Java      : 2
    Assembly  : 1
    C         : 1
    C++       : 1
    CSS       : 1
    JavaScript: 1
    HTML      : 1

~$ python gps.py a_non_existing_user
Cannot find this profile
```

## improvements
- [x] better handling for None values
- [ ] better handling on API limit reach
- [ ] increase allowed requests
- [x] show sum of all repos
- [ ] better display for repo per language

## contributions
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Contributions are welcome !
