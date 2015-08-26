#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

DESCRIPTION


EXAMPLES


AUTHOR

    Holger Dinkel <dinkel@embl.de>

"""
VERSION=0.1


import random
import string
import svgwrite
import io

def main():

    svg_file = io.open('passwordcard.svg', 'w', encoding='utf-8')
    dwg = svgwrite.Drawing(profile='tiny')
    passwords = ['myPass', 'another']
    line_height = 20
    letterwidth = 14
    attribs_header = {'font-family':'URW Palladio L', 'font-size':16, 'text-anchor':'start', 'class':'monofont'}
    attribs_main = {'font-family':'Nimbus Mono L', 'font-size':16, 'text-anchor':'start', 'class':'monofont'}

    header_row = u'■□▲△○●★☂☀☁☹☺♠♣♥♦♫€¥£$!?¡¿⊙◐◩�'
    characters = list(string.punctuation + string.lowercase + string.letters + string.lowercase + string.digits + string.letters + string.lowercase)

    for j, letter in enumerate(header_row):  # Need to convert to list so we can replace letters
#        dwg.add(dwg.text(unicode(letter), insert=(j*letterwidth+1, line_height-2), fill='black'))
        mytext = dwg.text(letter, insert=(j*letterwidth+1, line_height-4), fill='black')
        mytext.update(attribs_header)
        dwg.add(mytext)

    max_len = len(header_row)
    colors = ('#CFCFC4', '#AE5A41', '#03C03C', '#FDFD96', '#F49AC2', '#77DD77', '#1B85B8', '#AECFC6')
    assert len(passwords) <= len(colors), "Too many passwords. Max: %s" % len(colors)

    for i in range(len(colors) - len(passwords)):
        passwords.append('')
    random.shuffle(passwords)

    for i in range(len(colors)):
        random.shuffle(characters)
        text = ''.join(characters[:max_len])
        text = list(text)
        if i == 6:
            password = '73yod'
            index = 9
        else:
            password = passwords[i]
            index = random.choice(range(0, len(text) - len(password)))
        for j, letter in enumerate(password):  # Need to convert to list so we can replace letters
            text[j+index] = letter
        text = ''.join(text)
        dwg.add(dwg.rect((1, (i+1)*line_height), (max_len*14, line_height), fill=colors[i]))
        for j, letter in enumerate(text):  # Need to convert to list so we can replace letters
            mytext = dwg.text(letter, insert=(j*letterwidth+1, (i+2)*line_height-4), fill='black')
            mytext.update(attribs_main)
            dwg.add(mytext)

    dwg.write(svg_file)
    svg_file.close()

if __name__ == '__main__':
    main()
