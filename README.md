# gps
Github Profile Summary (gps) is a small command-line tool 
to get an overview of a Github user's activity


## usage

```shell
~$ python gps.py pBouillon
User Pierre Bouillon (pBouillon):
    "Developer, student and tech enthusiast."
    Registered since 2016-10-05

Repositories per languages:
    Python: 17
    Other : 2
    Java: 2
    C++: 1
    JavaScript: 1
    Assembly: 1
    HTML: 1
    CSS: 1
    C: 1

~$ python gps.py a_non_existing_user
Cannot find this profile
```

## improvements
- [ ] better handling for None values
- [ ] better handling on API limit reach
- [ ] increase allowed requests
- [ ] show sum of all repos

## contributions
Contributions are welcome !
