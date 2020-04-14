import argparse
import intervaltree
import sys
from collections import namedtuple, defaultdict

"""
A script that implements the SV clustering rules of 
Tracing Oncogene Rearrangements in the Mutational History of Lung Adenocarcinoma, Lee et al 2019.
Clusters balanced events
Clusters nearby breakpoints into events that are then labeled simple/complex
"""


MAX_INTER_DEFAULT = 5000000
SLOP = 1

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input SV file for clustering", type=str, required = True, dest="input")
    parser.add_argument("-m", "--max-distance", help="The max interbreakpoint distance. SVs closer than this are clustered.",
            required=False, type=int, default=MAX_INTER_DEFAULT)
    parser.add_argument("-b", "--balanaced-dist", help="Max distance for two SVs to be considered balanced.", default=500, required=False)
    return parser.parse_args()

def balance(vtree, bal_slop):
    for chrom in vtree:
        for v in vtree[chrom]:
            if vtree.overlaps(v.POS1 - bal_slop, v.POS2 + bal_slop) is not None:
                pass
    return

def cluster(variants, vtree, inter_dist, bal_dist):
    cluster_d = defaultdict(list)
    pass
    #for i in variants:

def slow_clust(vlist, bal_d):
    clust_d = defaultdict(list)
    for samp in vlist:
        b_list = vlist[samp]
        clust_count = 0
        for v in vlist[samp]:
            for b in b_list:
                pass
                

def slow_bal(vlist):
    bal_d = defaultdict(bool)
    for samp in vlist:
        b_list = vlist[samp]
        for v in vlist[samp]:
            for b in b_list:
                if v.NAME != b.NAME and \
                        abs(int(v.POS1) - int(b.POS1)) <= 500 and \
                        abs(int(v.POS2) - int(b.POS2)) <= 500 and \
                        v.STRAND1 == b.STRAND2 and \
                        v.SVTYPE == b.SVTYPE:
                    bal_d[v] = True
    return bal_d
    

if __name__ == "__main__":
    
    args = parse_args()

    Variant = namedtuple('Variant', 'CHROM1 POS1 STRAND1 CHROM2 POS2 STRAND2 SVTYPE SAMPLE NAME BALANCED LINE')
    header_d = defaultdict(int)
    
    vlist = defaultdict(list)
    chrom_intervals = defaultdict(lambda : intervaltree.IntervalTree)
    inter_head_intervals = defaultdict(intervaltree.IntervalTree)
    inter_tail_intervals = defaultdict(intervaltree.IntervalTree)
    vcount = 0
    with open(args.input, "r") as ifi:
        for line in ifi:
            if not line.startswith("#") and not line.startswith("individual"):
                line = line.strip()
                tokens = line.strip().split("\t")
                name = "_".join([tokens[header_d["chr1"]], tokens[header_d["pos1"]], tokens[header_d["str1"]],
                        tokens[header_d["chr2"]], tokens[header_d["pos2"]], tokens[header_d["str2"]], tokens[header_d["class"]], tokens[header_d["individual"]]])
                v = Variant(tokens[header_d["chr1"]], tokens[header_d["pos1"]], tokens[header_d["str1"]],
                        tokens[header_d["chr2"]], tokens[header_d["pos2"]], tokens[header_d["str2"]], tokens[header_d["class"]], tokens[header_d["individual"]], name, False, line)
                vlist[v.SAMPLE].append(v)
                chrom_intervals[v.SAMPLE][v.CHROM1].addi(v.POS1, v.POS2, v)
                vcount += 1
            else:
                tokens = line.strip().strip("#").split("\t")
                for i in range(0, len(tokens)):
                    header_d[tokens[i]] = i

    print("Read", vcount, "variants.", file=sys.stderr)
    bal_d = slow_bal(vlist)
    for s in vlist:
        for v in vlist[s]:
            print(v.NAME, bal_d[v])
    #cluster_list = cluster()

