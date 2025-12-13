### BIMM 182 Final Project - Problem 3
### Identify SV type of every discordant edge

import os

os.chdir("/Users/evelynquan/Downloads/classes/BIMM 182/final-project/all_discordant_edges")

# Set up SV frequencies file
with open("../sv_frequencies.tsv", "w") as sv_frequencies:
    sv_frequencies.write("ID\tStart_Position\tEnd_Position\tSV_Type\tFrequency\n")

    sv_id = 0
    with open("filtered_edges_1.tsv", "r") as file:
        for line in file:
            if (line.startswith("chrom1")):
                continue
            edge_info = line.split("\t")
            start = edge_info[1]
            end = edge_info[4]

            sv_id += 1
            # check if it's a translocation first (diff chromosomes for start and end)
            if (edge_info[0] != edge_info[3]):
                sv_frequencies.write(str(sv_id) + "\t" + edge_info[0] + ":" + start + edge_info[2] + "\t" + edge_info[3] + ":" + end + edge_info[5] + 
                                     "\t" + "Translocation" + "\t" + edge_info[6])
        
            # deletion (+/-, and it's not a translocation)
            elif (edge_info[2] == "+" and edge_info[5] == "-"):
                sv_frequencies.write(str(sv_id) + "\t" + edge_info[0] + ":" + start + edge_info[2] + "\t" + edge_info[3] + ":" + end + edge_info[5] + 
                                     "\t" + "Deletion" + "\t" + edge_info[6])
            
            # inversion (right foldback +/+ or left foldback -/-)
            elif (edge_info[2] == edge_info[5]):
                sv_frequencies.write(str(sv_id) + "\t" + edge_info[0] + ":" + start + edge_info[2] + "\t" + edge_info[3] + ":" + end + edge_info[5] + 
                                     "\t" + "Inversion" + "\t" + edge_info[6])

            # circularization (-/+)
            elif (edge_info[2] == "-" and edge_info[5] == "+"):
                sv_frequencies.write(str(sv_id) + "\t" + edge_info[0] + ":" + start + edge_info[2] + "\t" + edge_info[3] + ":" + end + edge_info[5] + 
                                     "\t" + "Circularization" + "\t" + edge_info[6])