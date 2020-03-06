import numpy as np
from numpy.random import normal, poisson
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('configuration')
args = parser.parse_args()


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


with open(args.configuration, 'r') as f:
    inp = json.load(f)

    n = int(inp['num_processes'])
    μ_arr, σ_arr = inp['arrival']['mean'], inp['arrival']['spread']
    μ_burst, σ_burst = inp['burst']['mean'], inp['burst']['spread']
    λ = inp['memory_poisson_lambda']

    ariv_times = normal(μ_arr, σ_arr, n)
    burst_times = normal(μ_burst, σ_burst, n)
    memory = poisson(λ, n)

    proc = []
    for i in range(1, n+1):
        proc.append({
            'proc_num': i,
            'arriv_time': ariv_times[i-1],
            'burst_time': burst_times[i-1],
            'memory': memory[i-1]
        })
    print(json.dumps(proc, cls=NpEncoder, indent=4))
