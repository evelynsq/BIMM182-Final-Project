import csv
import re #yay regex
from typing import List, Tuple

#Parameters
POSITION_TOLERANCE = 150000  #bp tolerance for clustering

#define edge
Edge = Tuple[str, int, str, str, int, str]

def parse_edge_string(edge_str: str) -> Edge:

    #Parses an edge string like '12:69386332+->12:69110024-'
    #expected edge formatting in regex form
    match = re.match(r'(\w+):(\d+)([+-])->(\w+):(\d+)([+-])', edge_str)
    #if no match, error
    if not match:
        raise ValueError(f"Invalid edge format: {edge_str}")
    #assigns values from edge to each parameter
    chrom1, pos1, dir1, chrom2, pos2, dir2 = match.groups()
    return (chrom1, int(pos1), dir1, chrom2, int(pos2), dir2)

#loads the edges from file into an array
def load_edges(filename: str) -> List[Edge]:
    edges = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)  #skip header (do not parse)
        for row in reader:
            edge_str = row[1]
            try:
                #attempts to parse file line by line for edges
                edge = parse_edge_string(edge_str)
                edges.append(edge)
            except ValueError as e:
                #if failure, thrown error
                print(f"Skipping line due to error: {e}")
    return edges


#helper funciton to cluster edges if their chromosomes match and their locations are within tolerance
def edges_within_window(e1: Edge, e2: Edge) -> bool:
    return (e1[0] == e2[0] and abs(e1[1] - e2[1]) <= POSITION_TOLERANCE and
            e1[2] == e2[2] and e1[3] == e2[3] and
            abs(e1[4] - e2[4]) <= POSITION_TOLERANCE and
            e1[5] == e2[5])


#clusters all edges into groups
def cluster_edges(edges: List[Edge]) -> List[Tuple[Edge, int]]:
    clustered = []
    used = [False] * len(edges)

    for i, edge_i in enumerate(edges):
        if used[i]:
            continue
        count = 1  # this edge counts as 1
        for j in range(i + 1, len(edges)):
            if not used[j]:
                edge_j = edges[j]
                if edges_within_window(edge_i, edge_j):
                    used[j] = True
                    count += 1
        used[i] = True
        clustered.append((edge_i, count))
    return clustered


#writes edges from clusters
def write_clusters(clusters: List[Tuple[Edge, int]], output_file: str):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['chrom1', 'pos1', 'dir1', 'chrom2', 'pos2', 'dir2', 'count'])
        for (edge, count) in clusters:
            writer.writerow(list(edge) + [count])

if __name__ == '__main__':
    #no argument parser, we only have two arguments, its fine
    input_file = 'all_edges.txt' #input file, change if necessary
    output_file = 'clustered_edges.tsv' #output file
    edges = load_edges(input_file)
    clusters = cluster_edges(edges)
    write_clusters(clusters, output_file)
    print(f"Clustered {len(edges)} edges into {len(clusters)} clusters.")
