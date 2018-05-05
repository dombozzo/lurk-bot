#!/usr/bin/env python3
import sys
import crawler
import build_graph
#import plot_graph
import os

#crawl the web
testfile = open("testfile.txt", "w")

test_graph = {'a': {'1', '2', '3', '4'}, 'b': {'1', '2', '3'}, 'c': {'1', '2'}, 'd': {'1'}}
search = "test suite"

testfile.write("Output of crawler function:")
testfile.write(str(test_graph)+'\n')
testfile.write('\n')
#turn the graph into dictionary json format for the plot
test_graph = build_graph.build(test_graph)
testfile.write("Output of build function:")
testfile.write(str(test_graph)+'\n')

#plot graph
#plot_graph.make_plot(test_graph, search)

#print success of plotting
testfile.write('\n')
testfile.write('Your search was a success! See plotly for results.\n')
testfile.close()

# compare characters of correct output with test
test_wc = int(os.popen("wc testfile.txt").readlines()[0].split()[2])
correct_wc = int(os.popen("wc output.txt").readlines()[0].split()[2])

# output appropriate message
if test_wc == correct_wc:
    print("WC TEST:\tPASSED")
else:
    print("WC TEST:\tFAILED")


