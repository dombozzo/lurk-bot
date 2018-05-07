#!/usr/bin/env python3
import sys
import crawler
import build_graph
#import plot_graph
import os

# testfiles to save test output
testfile1 = open("testfile1.txt", "w")
testfile2 = open("testfile2.txt", "w")

# test graphs (w/ known output)
test_graph1 = {'a': {'1', '2', '3', '4'}, 'b': {'1', '2', '3'}, 'c': {'1', '2'}, 'd': {'1'}}
test_graph2 = {'a': {'x', 'y', 'z', 'w'}, 'b': {'z', 'w', 'k'}, 'c': {'z', 'k'}, 'd': {'x','z'}}

# TEST #1
#search = "test suite 1"

testfile1.write("Output of crawler function:\n")
testfile1.write(str(test_graph1)+'\n')
testfile1.write('\n')
#turn the graph into dictionary json format for the plot
test_graph1 = build_graph.build(test_graph1)
testfile1.write("Output of build function:\n")
testfile1.write(str(test_graph1)+'\n')

#plot graph 1
#plot_graph.make_plot(test_graph1, search)

#print success
testfile1.write('\n')
testfile1.write('Your search was a success! See plotly for results.\n')
testfile1.close()

# compare characters of correct output with test
test_wc1 = int(os.popen("wc testfile1.txt").readlines()[0].split()[2])
correct_wc1 = int(os.popen("wc output1.txt").readlines()[0].split()[2])

# output appropriate message
if test_wc1 == correct_wc1:
    print("WC TEST1:\tPASSED")
else:
    print("WC TEST1:\tFAILED")

# TEST #2
#search = "test suite 2"

testfile2.write("Output of crawler function:\n")
testfile2.write(str(test_graph2)+'\n')
testfile2.write('\n')
# turn the graph into dictionary json format to prepare for plotting
test_graph2 = build_graph.build(test_graph2)
testfile2.write("Output of build function:\n")
testfile2.write(str(test_graph2)+'\n')

#plot graph 2
#plot_graph.make_plot(test_graph2, search)

#print success
testfile2.write('\n')
testfile2.write('Your search was a success! See plotly for results.\n')
testfile2.close()

# compare characters of correct output with test
test_wc2 = int(os.popen("wc testfile2.txt").readlines()[0].split()[2])
correct_wc2 = int(os.popen("wc output2.txt").readlines()[0].split()[2])

# output appropriate message
if test_wc2 == correct_wc2:
    print("WC2 TEST:\tPASSED")
else:
    print("WC2 TEST:\tFAILED")


