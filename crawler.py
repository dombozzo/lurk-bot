#!/usr/bin/env python3
import os, requests, functools, queue, sys, signal
from bs4 import BeautifulSoup
from urllib.request import urlparse
import re

MAX_LINKS = 5
NUMBER_WORKERS = 1
ENGINE = "Google"
graph ={}

def usage(status):
    print('''Usage: [OPTIONS] \"SEARCH\"
        -m INT  [set max links]
        -c INT [set number workers]
        -e STRING [set search engine: google, yahoo, bing, ask]
        -a [get output from all engines]
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
        engine = 'ask'
    else:
        engine = 'bing'

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

            #     links.add(tag['href'])
    graph[engine] = coolest
    #links = map(functools.partial(prepend_links, url), links)
    #links = filter(validate_links, links)

    return coolest

def prepend_links(root, url):
    '''If link starts with /, add base url to it'''
    if root[-1] == '/':
        root = root[:-1]
    if url[0] == '/':
        return root + url
    else:
        return url

def validate_links(link):
    '''Validate if link has http or https and a nonempty domain'''
    return not (urlparse(link).scheme is '' or urlparse(link).netloc is '')

def make_request(q, visited):
    '''Make single request, process html and add links to queue'''
    # Get url
    url = q.get()

    #headers  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
    try:
        # Try to make request
        for _ in range(5):
            response = requests.get(url)

            if response.status_code == 200:
                break

        if response.status_code == 200:
            # Add url to visited
            visited.put_nowait(url)
            if visited.qsize() >= MAX_LINKS:
                shutdown()
                return

            # Get other links

            links = get_links(response.text, url)

            # Add other links to queue
            for link in links:
                q.put_nowait(link)
    except KeyboardInterrupt:
        shutdown()
    except:
        pass

def crawl(cmdargs):
    global MAX_LINKS, ENGINE
    # check min args
    if len(cmdargs) < 2:
        usage(1)
    # set search
    search = cmdargs[-1]
    # spaces -> +
    search = search.replace(' ','+')

    # parse options
    SEARCH_ALL = False
    args = cmdargs[1:]
    while len(args) and args[0].startswith('-') and len(args[0]) > 1:
        arg = args.pop(0)
        if arg == '-m':
            MAX_LINKS = int(args.pop(0))
        elif arg == '-c':
            NUMBER_WORKERS = int(args.pop(0))
        elif arg == '-a':
            SEARCH_ALL = True
        elif arg == '-e':
            ENGINE = args.pop(0)
        elif arg == '-h':
            usage(0)
        else:
            usage(1)

    q = queue.Queue(MAX_LINKS)
    visited = queue.Queue(MAX_LINKS)

    # set start URL w/ engine & search
    s = ""
    if not SEARCH_ALL:
        if ENGINE == "google":
            s = "https://www.google.com/search?q=" + search
        elif ENGINE == "bing":
            s = "https://www.bing.com/search?q=" + search
        elif ENGINE == "ask":
            s = "https://www.ask.com/web?q=" + search
        elif ENGINE == "yahoo":
            s = "https://search.yahoo.com/search?p=" + search

        q.put_nowait(s)
    else:
        q.put_nowait("https://www.google.com/search?q=" + search)
        q.put_nowait("https://www.bing.com/search?q=" + search)
        q.put_nowait("https://www.ask.com/web?q=" + search)
        q.put_nowait("https://search.yahoo.com/search?p=" + search)


    while not q.empty():
        make_request(q, visited)

    return(graph)

# if __name__ == "__main__":
#     signal.signal(signal.SIGINT, signal_handler)
#     main()
