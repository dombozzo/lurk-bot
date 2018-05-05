Project Dependencies and Installation Guide:
--------------------------------------------
To be able to run lurkbot, a machine must have the following python
libraries compatible with python3:
sys
os
requests
re
functools
queue
signal
bs4
urllib
re
igraph
plotly

All of these were installed to our local machines by using
pip install (library)
It may be necessary to add "sudo" at the beginning of these commands as well.

Once all of these libraries are installed on a machine, one must also
create and link an account on plot.ly to the machine. This is done by creating
a plotly account at plot.ly. Once an account is created, instructions for
linking the plotly account with a machine are found at
https://plot.ly/python/getting-started/
Follow these instructions, but stop once you get to the section entitled
"Online Plot Privacy"

After all of these libaries are installed and a plotly account is linked
to the machine, the user is ready to run lurkbot.

Utilizing lurkbot:
------------------
The usage function for lurkbot.py can be found by typing the command
python ./lurker.py -h
The usage function is shown below:
Usage: [OPTIONS] "SEARCH"
        -m INT  [set max links]
        -a [get output from all engines]
        -e ENGINE [google,yahoo,ask,bing]
        -h help

To elaborate upon this usage function, there are two modes to run lurkbot in:

1. Search all engines (default)
In this mode, one can run lurkbot by typing
python ./lurker.py "SEARCH ENTITY"
where SEARCH ENTITY is what you would like to search the web for
This is comparable to running the script with the -a flag.
In this mode, all four search engines (google, bing, ask, and yahoo) are used
to create a network graph of search engine results. The program will scrape
urls from each of the search engines and create a network graph on the plotly
account set up on your local machine. To view the network graph, log into
your plotly account online.

2. Search one engine (-e ENGINE)
If you aren't concerned with the results of all four search engines, but would
instead like to view the results of only one search engine, use the -e ENGINE
flag to indicate which of the four search engines you would like to use.
For example,
python ./lurker.py -e google "nike shoes"
Will generate a network graph based on the results of a google search for
nike shoes.

Description of Makefile and Test-Suite:
---------------------------------------
