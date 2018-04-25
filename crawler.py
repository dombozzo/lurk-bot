#!/usr/bin/env python3
import os, requests, functools, queue, multiprocessing, sys, signal
from bs4 import BeautifulSoup
from urllib.request import urlparse
import re

MAX_LINKS = 4
NUMBER_WORKERS = 1
ENGINE = "google"
graph ={}

def usage(status):
    print('''Usage: {} [OPTIONS] \"SEARCH\"
        -m INT  [set max links]
        -c INT [set number workers]
        -e STRING [set search engine: google, yahoo, bing, ask]
        -a [get output from all engines]
        -h help '''.format(sys.argv[0]))
    sys.exit(status)

def signal_handler(signal, frame):
    sys.exit(0)

def shutdown(q):
    print('shutting')
    while not q.empty():
        q.get_nowait()

def get_links(html, url):
    '''Extract all links from an html page'''
    links = set()
    soup = BeautifulSoup(html, "lxml")

    coolest = set()
    # Extract all links from html of html
    for tag in soup.find_all('a', href=True):
        if len(re.findall(ENGINE, tag['href'])) == 0:
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
    print(coolest)
    links = map(functools.partial(prepend_links, url), links)
    links = filter(validate_links, links)

    return links

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

def make_request(url, q, visited, process):
    '''Make single request, process html and add links to queue'''
    # headers  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
    try:
        # Try to make request
        for _ in range(5):
            #response = requests.get(url, headers=headers)
            response = requests.get(url)

            if response.status_code == 200:
                break

        if response.status_code == 200:
            # Add url to visited
            visited.put_nowait(url)
            if visited.qsize() >= MAX_LINKS:
                shutdown(q)
                return
            #print('{}: Visited url: {}, visited: {}, length of queue: {}'.format(process, url, visited.qsize(), q.qsize()))
            #print("Engine: {}   Search: {}".format(ENGINE,sys.argv[-1]))

            # Get other links
            links = get_links(response.text, url)
            graph[url] = list(links)
            #print(graph)
            # Add other links to queue
            for link in links:
                q.put_nowait(link)
    except KeyboardInterrupt:
        shutdown(q)
    except:
        pass

def crawl(q, visited, process):
    started = False
    while not q.empty() or not started:
        started = True
        make_request(q.get(), q, visited, process)

    #this is where the graph is completely built
    #print(graph)

def main():
    global MAX_LINKS, NUMBER_WORKERS, ENGINE

    # check min args
    if len(sys.argv) < 2:
        usage(1)
    # set search
    search = sys.argv[-1]
    # spaces -> +
    search = search.replace(' ','+')

    # parse options
    SEARCH_ALL = False
    args = sys.argv[1:]
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

    pool = multiprocessing.Pool(NUMBER_WORKERS)
    m = multiprocessing.Manager()
    q = m.Queue(MAX_LINKS)
    visited = m.Queue(MAX_LINKS)

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

    print("Engine: {}   Search: {}  URL: {}".format(ENGINE,sys.argv[-1],s))

    q.put_nowait(s)
    pool.map(functools.partial(crawl, q, visited), range(NUMBER_WORKERS))
    pool.close()



if __name__ == "__main__":
    # Catch Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)

    main()
