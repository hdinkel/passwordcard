#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

DESCRIPTION

    Create a password card, optionally containing user provided passwords


EXAMPLES

    python generate_passwordcard.py
    python generate_passwordcard.py mySecr33t 2 4
    python generate_passwordcard.py passw0rd 0 0 4n0th3r 3 5

    Use a seed (SEED) and one row of digits:
        python generate_passwordcard.py -r SEED  -n 1

AUTHOR

    Holger Dinkel <dinkel@embl.de>

"""
VERSION = '0.4'


import sys
import optparse
import random
import string
import svgwrite
import io


def main():

    PASSWORDCARDNAME = 'passwordcard.svg'
    WIDTH, HEIGHT = 1024, 800
    GRID_COLOR = '#666666'

    # TODO: find better way to seed randomness
    if options.random_seed:
        random.seed(options.random_seed)

    if options.digit_rows:
        DIGIT_ROWS = int(options.digit_rows)
    else:
        DIGIT_ROWS = 0

    svg_file = io.open(PASSWORDCARDNAME, 'w', encoding='utf-8')
    dwg = svgwrite.Drawing(profile='tiny', size=(str(WIDTH), str(HEIGHT)))
    passwords = {}
    if len(args) > 0:
        assert len(args) % 3 == 0, "When providing passwords, you also need to provide a column and row for each password!"
        while len(args) > 0:
            password = args.pop(0)
            row = int(args.pop(0))
            column = int(args.pop(0))
            passwords[password] = (row, column)
    line_height = 18
    letterwidth = 10
    boxlength = 10
    attribs_header = {'font-family': 'Lucida Sans', 'font-weight': '600', 'font-size': 10, 'text-anchor': 'start', 'class': 'monofont'}
    attribs_main = {'font-family': 'monospace', 'font-size': 14, 'text-anchor': 'start', 'class': 'monofont'}


#   header_row = list(u'■□▲△○●★☂☀☁☹☺♠♣♥♦♫€¥£$!?¡¿⊙◐◩�')
#   header_row = list(u'♔♕□△○★☔☀☁☹☺♠♣♥♦♫€$☏☑☒☣?♀♂♲⚡⚕⚖')
    header_row = list(u'♔♕⚅△○★☔☀☁☹☺♠♣♥♦♫€$☏☑☒☣?♀♂♲⚡⚕⚐')

    if options.shuffle_header:
        random.shuffle(header_row)
    header_row = ''.join(header_row)
    characters = list(string.punctuation + string.lowercase + string.letters + string.lowercase + string.digits + string.letters + string.lowercase)
    digits = list(string.digits+string.digits+string.digits)

    max_len = len(header_row)
    colors = ('#7FCAFF', '#7F97FF', '#E77FFF', '#FF7FB0', '#FF9C7E', '#FFBD7E', '#FFF17E', '#CAF562', '#62F5C8', '#7FCAFF')

    assert len(passwords.keys()) <= len(colors), "Too many passwords. Max: %s" % len(colors)

    group = dwg.add(dwg.g(transform='translate(5,2)'))

    for j, letter in enumerate(header_row):  # Need to convert to list so we can replace letters
        mytext = dwg.text(letter, insert=(j*letterwidth, line_height-4), fill='black')
        mytext.update(attribs_header)
        group.add(mytext)

#    for i in range(len(colors) - len(passwords)):
#        passwords.append('')
#    random.shuffle(passwords)

    for i in range(len(colors)):
        random.shuffle(characters)
        if DIGIT_ROWS > 0:
            text = ''.join(random.sample(digits, max_len))
            DIGIT_ROWS -= 1
        else:
            text = ''.join(random.sample(characters, max_len))
        for password, pos in passwords.items():
            row, column = pos
            if row == i:
                text = list(text)
                for j, letter in enumerate(password):  # Need to convert to list so we can replace letters
                    text[j+column] = letter
                text = ''.join(text)
#        index = random.choice(range(0, len(text) - len(password)))
        group.add(dwg.rect((-3, (i+1)*line_height), (max_len*boxlength+5, line_height), fill=colors[i]))
        group.add(dwg.line((-3, (i+1)*line_height), (max_len*boxlength+3, (i+1)*line_height), stroke=GRID_COLOR, stroke_width='0.1'))
        for j, letter in enumerate(text):  # Need to convert to list so we can replace letters
            mytext = dwg.text(letter, insert=(j*letterwidth, (i+2)*line_height-4), fill='black')
            mytext.update(attribs_main)
            group.add(mytext)
    for i in range(1, len(header_row)):
        group.add(dwg.line((i*letterwidth, 0), (i*letterwidth, line_height*(len(colors)+1)), stroke=GRID_COLOR, stroke_width='0.1'))

    myborder = dwg.rect(insert=(2, 2), size=(letterwidth * 1.02 * len(header_row), (len(colors)+1) * line_height * 1.0), rx=2, ry=2, fill='white', stroke='black')
    myborder.fill(opacity='0.0')
    dwg.add(myborder)

#    dwg.add(dwg.line(start=(0, 0), end=(100, 100), fill='black', stroke='black'))
    dwg.write(svg_file)
    svg_file.close()
    print "Your PasswordCard has been created as '%s'" % PASSWORDCARDNAME

if __name__ == '__main__':
    try:
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version=VERSION)
        parser.add_option('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_option('-s', '--shuffle_header', action="store_true", dest='shuffle_header', default=False)
        parser.add_option('-r', '--random_seed', action="store", dest='random_seed')
        parser.add_option('-n', '--numbers', action="store", dest='digit_rows', help='use this many lines of rows with digits')
        (options, args) = parser.parse_args()
        main()
        sys.exit(0)
    except AssertionError, e:
        print 'ERROR:'
        print e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        sys.exit(8)
