This is a passphrase generator which generates passphrase based on an algorithm 
inspired by [xkcd #936](https://www.xkcd.com/936/).

Requires python ≥ 3.6.

## Usage

    usage: pwgen.py [-h] [-c C] [-w W] [-e] file
    
    Passphrase generator à la xkcd (https://www.xkcd.com/936/)
    
    positional arguments:
      file        path to wordlist
    
    optional arguments:
      -h, --help  show this help message and exit
      -c C        passphrase length in characters
      -w W        passphrase length in words
      -e          print password to STDERR in addition to STDOUT
    
    If both -c and -w are specified, -w is used. If neither are supplied then a 32
    character long passphrase (i.e. -c 32) is created.


I use it with the [EFF wordlist][1].  The `-e` argument is useful for doing 
`pwgen.py eff_large_wordlist.txt | pbcopy`.

[1]: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases

![Password Strength](http://imgs.xkcd.com/comics/password_strength.png)
