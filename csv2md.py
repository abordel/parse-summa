#!/usr/bin/env python

import sys
import os
import re
import string

import pandas as pd


def create_markdown_page(question_num):
    '''
    Create filename.md in the current directory
    return a file handle
    '''
    filename = 'question_{}.md'.format(question_num)
    f = open(filename, 'w')

    return f

def write_header(question_num, question_text, file_handle):
    '''
    Write the question in markdown heading 1 at the top of the file
    '''
    str_to_write = '# {}\n\n'.format(string.capwords(question_text))
    f.write(str_to_write)

def write_question_body(question_body, file_handle):
    '''
    Write the body under the heading
    '''
    file_handle.write(question_body+'\n\n')

def write_articles(question_number, file_handle):
    '''Write the text of all the articles
    '''
    question_number = 'QUESTION {}'.format(question_number)
    articles = article_df[article_df.question_number == question_number]
    article_num = 0
    for i, row in articles.iterrows():
        article_num+=1
        str_to_write = '## {}\n\n'.format(string.capwords(row.article_text))
        f.write(str_to_write)
        new_text = replace_article_text(row.body_text)
        f.write(new_text+'\n')

def replace_article_text(article_text):
    '''Add markup and change for consistency
    '''
    # the replacement order matters
    article_replace = [('Objection 1: ','### *Objection 1*\n'),
                       ('Reply Obj. (\d+): ', '### *Reply to Objection \g<1>*\n'),
                       ('Obj. (\d+): ', '### *Objection \g<1>*\n'),
                       ('_On the contrary,_ ', '### *On the contrary*\n'),
                       ('_I answer that,_ ', '### *I answer that*\n'),
                       ]

    for s, r in article_replace:
        article_text = re.sub(s, r, article_text)
    return article_text

if __name__ == '__main__':
    question_csv = sys.argv[1]
    article_csv = sys.argv[2]
    outputdir = './'
    if len(sys.argv) > 3:
        outputdir = sys.argv[3]

    question_df = pd.read_csv(question_csv)
    article_df = pd.read_csv(article_csv)

    for i,row in question_df.iterrows():
        question_num = i+1
        f = create_markdown_page(question_num)
        write_header(question_num, row.question_text, f)
        write_question_body(row.body_text, f)
        write_articles(question_num, f)
        f.close()
        print(f.name)
