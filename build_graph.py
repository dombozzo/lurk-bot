#!/usr/bin/env python3

def build(g):

    tset=set()

    graph = {}
    nodes =[]
    location = {}
    i =0

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
                temp={}
                temp['name'] = link
                temp['group'] = 2
                tset.add(link)
                nodes.append(temp)
                location[link] = i
                i +=1


    graph['nodes'] = nodes

    edges = []
    for engine in g:
        for link in g[engine]:
            edge ={}
            edge['source'] = location[engine]
            edge['target'] = location[link]
            edge['value'] = 1
            edges.append(edge)

    graph['links'] = edges

    return graph
