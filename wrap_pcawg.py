import sys
from collections import defaultdict

if __name__ == "__main__":
    
    sample_d = defaultdict(list)
    with open(sys.argv[1], "r") as ifi:
        for line in ifi:
            line = line.strip()
            tokens = line.split("\t")
            name = tokens[6]
            n_splits = name.split(":")
            sample_name = n_splits[0]
            sample_d[sample_name].append(line)

    for i in sample_d:
        with open(i + ".sv.bedpe", "w") as ofi:
            for line in sample_d[i]:
                ofi.write(line + "\n")

