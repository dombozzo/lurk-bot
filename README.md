Project Dependencies and Installation Guide:
--------------------------------------------
To be able to run lurkbot, a machine must have the following python
libraries compatible with python3:
- sys
- os
- requests
- re
- functools
- queue
- signal
- bs4
- urllib
- re
- igraph
- plotly

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

Since our programs are written in python, the Makefile for lurk-bot is
relatively simple, primarily intended for use in testing. The Makefile contains
the following options:
- test (which is same as test-all)
- test-all (runs test-wc and test-diff)
- test-diff (runs ./test_diff.py)
- test-wc (runs ./test_wc.py)
- clean

The scripts test_wc.py and test_diff.py are used to test the output
of lurk-bot for correctness. Both scripts use a predetermined input
(test_graph) to run lurk-bot and a known output (output.txt) to verify the
correctness of the results.

As hinted by the name, test_diff uses the Unix command `diff` to compare
lurk-bot output (testfile.txt) to a known output file (output.txt).
Since lurk-bot utilizes python (unordered) sets for its implementation, the
result of this test script can often be deceiving. We recommend that the user
go manually inspect the output of diff; often the files will have the same
content in a different ordering.

Since using test_diff can produce slightly confusing output, test_wc is a
simple means to compare lurk-bot output with known output. test_wc
uses the character count (Unix command `wc`) from each file to determine
(with relative authority) if the two outputs are identical. We are aware that
this test can technically be tricked/faulty, but for the scope of our project
it is an extremely efficient and accurate means for gauging the
correctness of our application.


