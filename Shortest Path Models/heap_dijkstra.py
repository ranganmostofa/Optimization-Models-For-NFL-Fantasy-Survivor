import heapq


def val(pair): return pair[0]


def id(pair): return pair[1]


def dijkstra(G,v):
    heap = [ [0, v] ]
    dist_so_far = {v:[0, v]}
    final_dist = {}
    prev = {}
    while len(final_dist) < len(G):
        # find the closest un-explored node
        while True:
            w = heapq.heappop(heap)
            # grab the relevant parts of w
            node = id(w)
            dist = val(w)
            if node != 'REMOVED':
                del dist_so_far[node]
                break

        # lock it down!
        final_dist[node] = dist
        # look at its neighbors
        for x in G[node]:
            # but only those that haven't been locked down
            if x not in final_dist:
                new_dist = dist + G[node][x]
                new_entry = [new_dist, x]
                if x not in dist_so_far:
                    # we haven't see this yet
                    # so add to the heap and the dictionary
                    dist_so_far[x] = new_entry
                    prev[x] = node
                    heapq.heappush(heap, new_entry)
                elif new_dist < val(dist_so_far[x]):
                    # the new distance is less then the
                    # best known
                    # Instead of removing it from the heap
                    # which could be expensive, mark it
                    dist_so_far[x][1] = "REMOVED"
                    # and then add a new entry
                    # for this node
                    prev[x] = node
                    dist_so_far[x] = new_entry
                    heapq.heappush(heap, new_entry)
    return final_dist, prev