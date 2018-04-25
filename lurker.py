#!/usr/bin/env python3
import sys
import crawler
import build_graph

tempgraph = crawler.crawl(sys.argv)
graph = build_graph.build(tempgraph)
print(graph)
