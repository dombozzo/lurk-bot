#!/usr/bin/env python3

def build(g):
    tset= set() # ensures that no entry is added twice as a vertex
    graph = {} # final product: dictionary filled w/ lists of dictionaries
    location = {} # stores ordering of each vertex for reference
    i = 0 # also for tracking ordering

    # build node list
    nodes =[] # stores vertices of graph
    for engine in g:
        tset.add(engine)
        e = {}
        e['name']= engine
        e['group']=1
        nodes.append(e)
        location[engine] = i
        i +=1

        for link in g[engine]:
            if link not in tset and link not in g:
                temp= {}
                temp['name'] = link
                temp['group'] = 2
                tset.add(link)
                nodes.append(temp)
                location[link] = i
                i +=1


    graph['nodes'] = nodes

    # build edge list
    edges = [] # stores edges of graph
    for engine in g:
        for link in g[engine]:
            edge ={}
            edge['source'] = location[engine]
            edge['target'] = location[link]
            edge['value'] = 1
            edges.append(edge)

    graph['links'] = edges

    # return graph complete w/ node list & edge list
    return graph
