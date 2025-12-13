import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Load the TSV file
filename = "filtered_edges.tsv"
#filename = "internal_edges_only.tsv"
df = pd.read_csv(filename, sep="\t")

# nly plot intra-chromosomal edges
df = df[df['chrom1'] == df['chrom2']]

#plotting time
fig, ax = plt.subplots(figsize=(12, 4))

#Closest general color to what they use in the slides
strand_color = {
    '++': 'blue',
    '--': 'green',
    '+-': 'red',
    '-+': 'brown'
}


#ok now its actually plotting time
def plot_arc(ax, start, end, count, color='gray'):
    """Draw a half-ellipse arc between start and end positions."""
    mid = (start + end) / 2
    width = abs(end - start)
    height = np.log(count + 1) * 1e6  #Scaled for visibility

    #Arc using parametric equation
    t = np.linspace(0, np.pi, 100)
    x = mid + (width / 2) * np.cos(t)
    y = height * np.sin(t)

    ax.plot(x, y, color=color)

#for al edges
for _, row in df.iterrows():
    if row['count'] >= 1:
        pos1 = row['pos1']
        pos2 = row['pos2']
        count = row['count']
        strand_pair = row['dir1'] + row['dir2']
        color = strand_color.get(strand_pair, 'gray')  #if all other colors fail

        plot_arc(ax, pos1, pos2, count, color=color)

#yay formatting
ax.set_xlabel(f"Chromosome {df.iloc[0]['chrom1']} position (Hundred Million bp)")
ax.set_ylabel("Number of Occurences")
ax.set_title("Sashimi Plot Colored by Strand Direction")
ax.set_ylim(0, None)
ax.grid(False)

#Legend (not of zelda)
handles = [plt.Line2D([0], [0], color=color, lw=2, label=label)
           for label, color in strand_color.items()]
ax.legend(handles=handles, title="Strand Pair", loc='upper right')

plt.tight_layout()
plt.show()
