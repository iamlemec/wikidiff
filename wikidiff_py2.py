# extract birth of article from wiki data
# fast parse: Liza Daly, http://www.ibm.com/developerworks/xml/library/x-hiperfparse/

import re
import sys
import argparse
import difflib
import io
from HTMLParser import HTMLParser
from lxml.etree import iterparse, XMLPullParser
html = HTMLParser()
open = io.open

# parse input arguments
parser = argparse.ArgumentParser(description='USPTO patent parser.')
parser.add_argument('source', type=str, help='path to xml file to parse')
parser.add_argument('output', type=str, help='path to csv output')
parser.add_argument('--log', type=str, help='log file to output to')
parser.add_argument('--limit', type=int, default=None, help='number of articles to parse')
args = parser.parse_args()

# namespaces
ns = '{http://www.mediawiki.org/xml/export-0.10/}'
page_tag = ns + 'page'
revn_tag = ns + 'revision'
ts_tag = ns + 'timestamp'
id_tag = ns + 'id'
title_tag = ns + 'title'
ns_tag = ns + 'ns'
text_tag = ns + 'text'

# get descendent text
def get_text(parent, tag, default=''):
    child = parent.find(tag)
    return (child.text or default) if child is not None else default

# preserve memory
def clear(elem):
    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]

# revert html codes
def html_unescape(text):
    text = html.unescape(text)
    text = text.replace(u'\xa0', u' ')
    return text

# regularize to token list
def reduce_wiki(text):
    text = re.sub(r'([^\w ]|_)', ' ', text) # remove non-alphanumeric, unicode aware
    text = re.sub(r' {2,}', ' ', text) # compress spaces again
    return text.lower().strip() # to lowercase and trim

def tokenize_wiki(text):
    wiki = html_unescape(text)
    red = reduce_wiki(wiki)
    return red.split()

# set up files
fin = open(args.source, encoding='utf-8')
fout = open(args.output, 'w', encoding='utf-8')
flog = open(args.log, 'w', encoding='utf-8', buffering=1) if args.log is not None else sys.stdout
plog = lambda s: flog.write(unicode(s)+'\n')

# create differ
sm = difflib.SequenceMatcher()

# this parser is bad and wrong
in_art = None
n_art = 0
text = None
for (i, line) in enumerate(fin):
    if i % 1000000 == 0:
        plog(i)

    ret = re.match('( *)<([^>]*?)>', line)
    if ret:
        (ind, tag) = ret.groups()
        ind = len(ind)
        body = line[ret.end():]
        ret = re.match('([^<]*?)</[^>]*?>', body)
        if ret:
            (body,) = ret.groups()
            oner = True
        else:
            oner = False
    else:
        tag = None
        if text is not None:
            if line.endswith('</text>\n'):
                text += line[:-8]
                try:
                    toks = tokenize_wiki(text)
                except:
                    plog('PARSE ERROR: %s, %s, %s' % (aid, rid, title))
                    toks = []
                text = None
            else:
                text += line
        continue

    if tag == '/page':
        if in_art:
            n_art += 1
            if args.limit and n_art >= args.limit:
                break
        in_art = None

    if in_art == False:
        continue

    if tag == 'page':
        in_art = None
        last_toks = []
    elif tag == 'ns':
        if body == '0':
            plog(title)
            in_art = True
        else:
            in_art = False
    elif tag == 'id':
        if ind == 4:
            aid = body
        elif ind == 6:
            rid = body
    elif tag == 'title':
        title = body
    elif tag == 'timestamp':
        date = body
    elif tag.startswith('text'):
        if oner:
            try:
                toks = tokenize_wiki(body)
            except:
                plog('PARSE ERROR: %s, %s, %s' % (aid, rid, title))
                toks = []
            text = None
        else:
            text = body
    elif tag == '/text':
        try:
            toks = tokenize_wiki(text)
        except:
            plog('PARSE ERROR: %s, %s, %s' % (aid, rid, title))
            toks = []
        text = None
    elif tag == '/revision':
        if toks is None:
            revn = []

        sm.set_seqs(last_toks, toks)
        plus = []
        for (op, s1, e1, s2, e2) in sm.get_opcodes():
            if op == 'insert' or op == 'replace':
                plus += toks[s2:e2]

        if len(plus) > 0:
            fout.write('%s,%s,%s,%s,%s,"%s"\n' % (aid, rid, date, len(toks), len(plus), ' '.join(plus)))

        last_toks = toks

# clean up
fout.close()
plog(n_art)
