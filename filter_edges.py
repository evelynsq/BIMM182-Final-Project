

#filters edges such that an edge has to start or end (or both) in the MDM2 region 
#of chromosome 12. 
def filter_edges_in_region(input_file, output_file, start=69000000, end=69240000):
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        header = fin.readline()
        #start with header
        fout.write(header)

        for line in fin:
            fields = line.strip().split()
            if len(fields) < 7:
                #if lines are malformed (not necessary)
                continue  
            
            try:
                pos1 = int(fields[1])
                pos2 = int(fields[4])
            except ValueError:
                #if invalid value for some reason
                continue 

            if start <= pos1 <= end or start <= pos2 <= end:
                fout.write(line)

#call
filter_edges_in_region("clustered_edges.tsv", "filtered_edges.tsv")

