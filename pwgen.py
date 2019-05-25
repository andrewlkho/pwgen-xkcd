#!/usr/bin/env python3

import argparse
import re
import secrets
import sys


def get_wordlist(file):
    '''Read the wordlist into a python list.'''
    try:
        f = open(file)
        words = f.readlines()
    except IOError:
        print(
            'Error: could not open supplied filename: {}'.format(file),
            file=sys.stderr
        )
        sys.exit(1)

    # Some (including the EFF wordlist) contain numbers indexing each line
    exclude = re.compile(r'[^a-zA-Z]+')
    words = [re.sub(exclude, '', w) for w in words]

    # Remove blank lines and words longer than 9 characters long; make all
    # lowercase
    words = [w.lower() for w in words if w and len(w) <= 9]

    # Check there are at least 1000 words in the wordlist
    if len(words) < 1000:
        print('Error: Insufficient words in dictionary', file=sys.stderr)
        sys.exit(1)

    f.close()
    return words


def main():
    description = '''
        Passphrase generator à la xkcd (https://www.xkcd.com/936/)
        '''
    epilog = '''
        If both -c and -w are specified, -w is used.  If neither are supplied
        then a 32 character long passphrase (i.e. -c 32) is created.
        '''
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('file', help='path to wordlist')
    parser.add_argument('-c', default=32, type=int,
                        help='passphrase length in characters')
    parser.add_argument('-w', type=int,
                        help='passphrase length in words')
    parser.add_argument('-e', action='store_true',
                        help='print password to STDERR in addition to STDOUT')
    args = parser.parse_args()

    words = get_wordlist(args.file)
    words_minlen = min([len(w) for w in words])
    words_maxlen = max([len(w) for w in words])
    separator = '-'

    # If passphrase length is requested in words
    if args.w:
        # Sanity check length of args.w
        if args.w < 1:
            print('Error: w should be an integer > 1', file=sys.stderr)
            sys.exit(1)
        proto = separator.join([secrets.choice(words) for i in range(args.w)])

    # If passphrase length is requested in characters (or unspecified)
    else:
        max_chars = args.c if args.c else 32

        # Reduce max_chars to give room for a number at the end
        max_chars = max_chars - len(separator) - 1

        # Sanity check length of max_chars
        if max_chars < words_minlen:
            print(
                'Error: c should be >= {}'.format(
                    words_minlen + len(separator) + 1
                ),
                file=sys.stderr
            )
            sys.exit(1)

        # Initialise the prototype passphrase
        proto = ''

        while len(proto) < max_chars:
            # The separator for this iteration
            proto_sep = separator if proto else ''

            # If there is room for only one more word
            if max_chars - len(proto) <= len(proto_sep) + words_maxlen:
                len_range = [max_chars - len(proto) - len(proto_sep)]

            # If there is room for more than one word but this word can't be
            # too long
            elif max_chars - len(proto) < (len(proto_sep) + words_maxlen
                                           + len(separator) + words_minlen):
                len_range = range(
                    words_minlen,
                    (max_chars - len(proto)
                     - len(proto_sep) - len(separator) - words_minlen
                     + 1)
                )

            # If there is room for a word of any length
            else:
                len_range = range(words_minlen, words_maxlen + 1)

            # Add a word of appropriate length
            to_add = secrets.choice([w for w in words if len(w) in len_range])
            proto = proto_sep.join([proto, to_add])

    # Capitalise the first letter
    proto = proto.capitalize()

    # Add a number at the end
    proto = separator.join([proto, str(secrets.randbelow(10))])

    # Print the passphrase
    print(proto)
    if args.e:
        print(proto, file=sys.stderr)


if __name__ == '__main__':
    main()
