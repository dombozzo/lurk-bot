#!/usr/bin/env python3
import sys
import crawler
import build_graph
import plot_graph

#crawl the web
tempgraph, search = crawler.crawl(sys.argv)

#turn the graph into dictionary json format for the plot
graph = build_graph.build(tempgraph)

#plot graph
plot_graph.make_plot(graph, search)

#print success
print('Your search was a success! See plotly for results.')
