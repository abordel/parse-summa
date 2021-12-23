#!/usr/bin/env python

import sys
import os
import re

import pandas as pd

def get_question_body(question, summa_text):
    """
    Get all text under a question
    """
    question_number, question_text, question_subtext = question
    question_text = question_text.replace('*','\*')
    question_text_re = r'{}\n+{}\n+\({}\)\n+'.format(question_number, question_text, question_subtext)
    question_text = re.search(question_text_re, summa_text)
    start_idx = question_text.end()

    question_end_re = r'_{5,}\n'
    question_end = re.search(question_end_re, summa_text[start_idx:])
    end_idx = start_idx + question_end.start()

    question_body = summa_text[start_idx:end_idx]

    return question_body

def get_article_text(article, summa_text):
    """
    Get all text under an article
    """
    article_number, article_code, article_text = article
    # clean up the article_text for use as a regex
    # escape ?
    article_text = article_text.replace('?','\?')
    # escape *
    article_text = article_text.replace('*','\*')
    # escape [
    article_text = article_text.replace('[','\[')
    # escape ]
    article_text = article_text.replace(']','\]')
    # escape (
    article_text = article_text.replace('(','\(')
    # escape )
    article_text = article_text.replace(')','\)')

    article_re = r'{}\s+.+\n+{}\n+'.format(article_number, article_text)
    article_text = re.search(article_re, summa_text)
    start_idx = article_text.end()

    article_end_re = r'_{5,}\n'
    article_end = re.search(article_end_re, summa_text[start_idx:])
    end_idx = start_idx + article_end.start()

    article_body = summa_text[start_idx:end_idx]

    return article_body

if __name__ == '__main__':
    input_summa_file = sys.argv[1]
    basefile = os.path.splitext(input_summa_file)[0]
    output_file = basefile + '.md'

    f = open(input_summa_file, 'r')
    line = f.read()
    f.close()

    # First get all questions
    # Which are always marked by the word QUESTION in
    # all caps, followed by a number, and the name of the question
    # Each question will get its own file and entry into the index
    question_re = r'(QUESTION\s\d+)\n+(.+)\n+\((.+)\)\n+'
    questions = re.findall(question_re, line)
    question_df = pd.DataFrame(questions, columns=['question_number', 'question_text', 'question_subtext'])
    body_text = []
    for q in questions:
        print(q)
        body_text.append(get_question_body(q, line))
    question_df['body_text'] = body_text

    article_re = r'(\w+\sARTICLE)\s(\[.+\])\n+(.+)\n+'
    articles = re.findall(article_re, line[2970:])
    article_df = pd.DataFrame(articles, columns=['article_number', 'article_code', 'article_text'])
    article_text = []
    for a in articles:
        article_text.append(get_article_text(a, line))
    article_df['body_text'] = article_text
    # for each article put a column for the question
    # in the format expected by the question table
    question_nums = article_df['article_code'].str.extract(r'Q\.\s+(\d+)')
    article_questions = []
    for index, row in question_nums.iterrows():
        num = row.to_list()[0]
        article_questions.append('QUESTION {}'.format(num))
    article_df['question_number'] = article_questions

    question_df.to_csv('questions.csv')
    article_df.to_csv('articles.csv')
