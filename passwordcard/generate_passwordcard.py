#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

DESCRIPTION

    Create a password card, optionally containing user provided passwords


EXAMPLES

    python generate_passwordcard.py 
    python generate_passwordcard.py mySecr33t 2 4
    python generate_passwordcard.py passw0rd 0 0 4n0th3r 3 5

AUTHOR

    Holger Dinkel <dinkel@embl.de>

"""
VERSION='0.3'


import sys
import optparse
import random
import string
import svgwrite
import io

def main():

    PASSWORDCARDNAME = 'passwordcard.svg'
    svg_file = io.open(PASSWORDCARDNAME, 'w', encoding='utf-8')
    dwg = svgwrite.Drawing(profile='tiny', size=('1024','800'))
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
    attribs_header = {'font-family':'URW Palladio L', 'font-size':14, 'text-anchor':'start', 'class':'monofont'}
    attribs_main = {'font-family':'Nimbus Mono L', 'font-size':14, 'text-anchor':'start', 'class':'monofont'}

#   header_row = list(u'■□▲△○●★☂☀☁☹☺♠♣♥♦♫€¥£$!?¡¿⊙◐◩�')
#   header_row = list(u'♔♕□△○★☔☀☁☹☺♠♣♥♦♫€$☏☑☒☣?♀♂♲⚡⚕⚖')
    header_row = list(u'♔♕⚅△○★☔☀☁☹☺♠♣♥♦♫€$☏☑☒☣?♀♂♲⚡⚕⚐')
    if options.shuffle_header:
        random.shuffle(header_row)
    header_row = ''.join(header_row)
    characters = list(string.punctuation + string.lowercase + string.letters + string.lowercase + string.digits + string.letters + string.lowercase)

    for j, letter in enumerate(header_row):  # Need to convert to list so we can replace letters
        mytext = dwg.text(letter, insert=(j*letterwidth, line_height-4), fill='black')
        mytext.update(attribs_header)
        dwg.add(mytext)

    max_len = len(header_row)
    colors = ('#7FCAFF', '#7F97FF', '#E77FFF', '#FF7FB0', '#FF9C7E', '#FFBD7E', '#FFF17E', '#CAF562', '#62F5C8', '#7FCAFF')

    assert len(passwords.keys()) <= len(colors), "Too many passwords. Max: %s" % len(colors)

#    for i in range(len(colors) - len(passwords)):
#        passwords.append('')
#    random.shuffle(passwords)

    for i in range(len(colors)):
        random.shuffle(characters)
        text = ''.join(characters[:max_len])
        for password, pos in passwords.items():
            row, column = pos
            if row == i:
                text = list(text)
                for j, letter in enumerate(password):  # Need to convert to list so we can replace letters
                    text[j+column] = letter
                text = ''.join(text)
#        index = random.choice(range(0, len(text) - len(password)))
        dwg.add(dwg.rect((0, (i+1)*line_height), (max_len*boxlength, line_height), fill=colors[i]))
        for j, letter in enumerate(text):  # Need to convert to list so we can replace letters
            mytext = dwg.text(letter, insert=(j*letterwidth, (i+2)*line_height-4), fill='black')
            mytext.update(attribs_main)
            dwg.add(mytext)

    dwg.write(svg_file)
    svg_file.close()
    print "Your PasswordCard has been created as '%s'" % PASSWORDCARDNAME

if __name__ == '__main__':
    try:
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version=VERSION)
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_option('-s', '--shuffle_header', action="store_true", dest='shuffle_header', default=False)
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

