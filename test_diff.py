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

print("DIFF TEST #1 (inspect values manually): ")
os.system("diff testfile1.txt output1.txt")

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

print("DIFF TEST # 2 (inspect values manually): ")
os.system("diff testfile2.txt output2.txt")
