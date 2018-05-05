#!/usr/bin/env python3
import os, requests, functools, queue, sys, signal
from bs4 import BeautifulSoup
from urllib.request import urlparse
import re

# Globals
MAX_LINKS = 5
E_NAMES = {"google","yahoo","bing","ask"}
ENGINE = "google"
graph ={}

def usage(status=0):
    print('''Usage: [OPTIONS] \"SEARCH\"
        -m INT  [set max links]
        -a [get output from all engines]
        -e ENGINE [google,yahoo,ask,bing]
        -h help ''')
    sys.exit(status)

def signal_handler(signal, frame):
    sys.exit(0)

def shutdown():
    sys.exit(0)

def get_links(html, url):
    '''Extract all links from an html page'''
    links = set()
    soup = BeautifulSoup(html, "lxml")

    if (url.find('google') != -1):
        engine = "google"
    elif (url.find('yahoo')!= -1):
        engine = "yahoo"
    elif (url.find('ask')!= -1):
        engine = "ask"
    else:
        engine = "bing"

    coolest = set()
    # Extract all links from html of html
    for tag in soup.find_all('a', href=True):
        if len(re.findall(engine, tag['href'])) == 0:
            matches = re.findall(r"http.*com",tag['href'])
            for match in matches:
                money = re.findall(r"//.*\.",match)
                money =  money[0][2:-1]
                fp = money.find('.')
                if fp != -1:
                    money = money[fp+1:]

                if len(money) < 50:
                    coolest.add(money)
    graph[engine] = coolest
    return coolest

def make_request(q, visited):
    '''Make single request, process html and add links to queue'''
    # Get url
    url = q.get()

    try:
        # try to make request
        for _ in range(5):
            response = requests.get(url)

            if response.status_code == 200:
                break

        if response.status_code == 200:
            # add url to visited
            visited.put_nowait(url)
            if visited.qsize() >= MAX_LINKS:
                shutdown()
                return

            # get other links
            links = get_links(response.text, url)

            # Add other links to queue
            for link in links:
                q.put_nowait(link)
    except KeyboardInterrupt:
        shutdown()
    except:
        pass

def crawl(cmdargs):
    global MAX_LINKS, ENGINE, E_NAMES

    # check min args
    if len(cmdargs) < 2:
        usage(1)

    # parse options (from lurker)
    SEARCH_ALL = True
    args = cmdargs[1:]
    search = ""
    while len(args) and len(args[0]) > 1:
        arg = args.pop(0)
        if arg == '-m': # set max links
            MAX_LINKS = int(args.pop(0))
        elif arg == '-a': # search all engines
            SEARCH_ALL = True
        elif arg == '-e': # for single engine search
            SEARCH_ALL = False
            ENGINE = args.pop(0).lower()
            if ENGINE not in E_NAMES: # invalid search engine entered
                usage(1)
        elif arg == '-h': # usage
            usage(0)
        else: # set search & manipulate to match URL format
            search = arg.replace(' ','+')

    # make sure search got set
    if not search:
        usage(1)

    q = queue.Queue(MAX_LINKS)
    visited = queue.Queue(MAX_LINKS)

    # set start URL w/ engine & search
    URL = ""
    if not SEARCH_ALL: # search single engine
        if ENGINE == "google":
            URL = "https://www.google.com/search?q=" + search
        elif ENGINE == "bing":
            URL = "https://www.bing.com/search?q=" + search
        elif ENGINE == "ask":
            URL = "https://www.ask.com/web?q=" + search
        elif ENGINE == "yahoo":
            URL = "https://search.yahoo.com/search?p=" + search

        q.put_nowait(URL) # push created URL (from single engine) onto queue
    else: # push all URLs onto queue
        q.put_nowait("https://www.google.com/search?q=" + search)
        q.put_nowait("https://www.bing.com/search?q=" + search)
        q.put_nowait("https://www.ask.com/web?q=" + search)
        q.put_nowait("https://search.yahoo.com/search?p=" + search)


    while not q.empty(): # make requests to build out `graph`
        make_request(q, visited)

    # return finished product with results from all searches
    return graph, cmdargs[-1]
