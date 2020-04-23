import sys
import subprocess
import multiprocessing as mp
import argparse
import math
import os
import shutil
from collections import defaultdict

def func(task):
    # subprocess.Popen(task, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    try:
        subprocess.call(task, shell=True)
    except (KeyboardInterrupt, Exception):
        raise KeyboardInterrupt
    return

def run(work, cores_per_task):
    ncpus = mp.cpu_count()
    size = int(math.floor(ncpus / cores_per_task))

    p = mp.Pool(size)
    try:
        ret = p.map_async(func, work).get(100000)
    except (KeyboardInterrupt):
        p.terminate()
        exit(1)
    return

def make_clustering_call(fi, cores_per_task=1):
    run_line = "Rscript clustering_index.R " + fi + " " + str(cores_per_task)
    return run_line

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, type=str, help="Input BEDPE file")
    parser.add_argument("-c", "--cores-per-task", required=False, default=1, type=int, help="Number of threads per clustering task", dest="task_cores")
    parser.add_argument("-t", "--tasks", required=False, default=2, type=int, help="Number of clustering tasks to run at one time.")
    parser.add_argument("-d", "--directory", required=False, default="splits", type=str, help="Directory to use for split files.")
    return parser.parse_args()

if __name__ == "__main__":
    
    args = parse_args()

    odir = os.getcwd()
    if os.path.exists(args.directory):
        shutil.rmtree(args.directory)
    os.mkdir(args.directory)
    
    sample_d = defaultdict(list)
    with open(args.input, "r") as ifi:
        for line in ifi:
            line = line.strip()
            tokens = line.split("\t")
            name = tokens[6]
            n_splits = name.split(":")
            sample_name = n_splits[0]
            sample_d[sample_name].append(line)

    for i in sample_d:
        with open(args.directory + "/" + i + ".sv.bedpe", "w") as ofi:
            for line in sample_d[i]:
                ofi.write(line + "\n")
    
    work_lines = []
    for i in sample_d:
        samp_file = args.directory + "/" + i + ".sv.bedpe"
        run_line = make_clustering_call(samp_file, args.task_cores)
        work_lines.append(run_line)
    run(work_lines, args.tasks)

    cluster_fi = ".".join(args.input.split(".")[:-1]) + ".clustered.bedpe"
    with open(cluster_fi, "w") as ofi:
        for i in sample_d:
            samp_file = args.directory + "/" + i + ".sv.bedpe.sv_clusters_and_footprints"
            with open(samp_file, "r") as sfi:
                for line in sfi:
                    ofi.write(line)
    
    shutil.rmtree(args.directory)

