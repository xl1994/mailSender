# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 16:19:08 2017

@author: xionglei
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

index_url = 'https://www.aeaweb.org/journals/aer'
b_url = 'https://www.aeaweb.org'

def getHtml(url):
    try:
        response = requests.get(url)
        html = response.content
    except Exception as e:
        print('getHtml::', str(e))
        html = False
    return html

def currentIssue(html):
    global b_url
    try:
        soup = BeautifulSoup(html, 'lxml')
        target = soup.find('a', class_ = 'current-issue-link button highlight')
        current_issue = b_url + target['href']
    except Exception as e:
        print('currentIssue::', str(e))
        current_issue = False
    return current_issue

def paperUrl(current_issue_html, first_row=False):
    df = pd.DataFrame(columns=['TITLE', 'URL'])
    global b_url
    try:
        soup = BeautifulSoup(html, 'lxml')
        target = soup.findAll('article', class_ = 'journal-article')
    except Exception as e:
        print('paperUrl::', str(e))
        target = False
    i = 0
    if not (target == False):
        for item in target:
            title = item.h3.a.text
            url = b_url + item.h3.a['href']
            df.loc[i]=[title, url]
            i = i + 1
        if not first_row:
            df = df.drop(0,axis=0)
    else:
        df = False
    return df

def parseAbstract(html):
    try:
        soup=BeautifulSoup(html, 'lxml')
        target = soup.find('section', class_ = 'article-information abstract')
    except Exception as e:
        print('parseAbstract::', str(e))
        target = False
    if not (target == False):
        tmp = list(target.strings)
        abstract = tmp[2].strip()
    else:
        abstract = False
    return abstract

def issuesAbstract(p_infos):
    # p_infos : DataFrame contain information about paper title and url
    p_urls = list(p_infos['URL'])
    p_titles = list(p_infos['TITLE'])
    df = pd.DataFrame(columns=['TITLE', 'ABSTRACT'])
    for index, name in enumerate(p_urls):
        if not p_titles[index]=='Front Matter':
            html = getHtml(name)
            abstract = parseAbstract(html)
            df.loc[index] = [p_titles[index], abstract]
    return df
    

if '__main__' == __name__:
    html = getHtml(index_url)
    soup = BeautifulSoup(html, 'lxml')
    target = soup.find('a', class_ = 'current-issue-link button highlight')
    current_issue = b_url + target['href']
    # get current issue list 
    html = getHtml(current_issue)
    p_infos = paperUrl(html)
    p_detail = issuesAbstract(p_infos)
    #for i in df.index:
    #   url = df.loc[i,'url']
    #    html = getHtml(url)
    #    print(df.loc[i,'title'])
    #    abstract = parseAbstract(html)
    #    print(abstract)