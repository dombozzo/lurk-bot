#!/usr/bin/env python3
import sys
import crawler
import build_graph
#import plot_graph

#crawl the web
tempgraph, search = crawler.crawl(sys.argv)
print("Output of crawler function:")
print(tempgraph)
print()
#turn the graph into dictionary json format for the plot
graph = build_graph.build(tempgraph)
print("Output of build function:")
print(graph)

#plot graph
#plot_graph.make_plot(graph, search)

#print success
print("\nYour search was a success! See plotly for results.")
