import sys
import os
import copy
import json
import argparse


class Process:
    num: int = 0
    arriv_time: float = 0
    burst_time: float = 0
    memory: float = 0

    @staticmethod
    def from_json(path: str):
        procs = []

        with open(path, 'r') as f:
            for pr in json.load(f):
                p = Process()
                p.num = int(pr['proc_num'])
                p.arriv_time = float(pr['arriv_time'])
                p.burst_time = float(pr['burst_time'])
                p.memory = float(pr['memory'])

                procs.append(p)

        return procs


class Machine:
    cpus: int  # num of CPUs, a soft constraint
    memory: float  # in GB

    @staticmethod
    def from_json(path: str):
        with open(path, 'r') as f:
            json_machine = json.load(f)

            m = Machine()
            m.cpus = int(json_machine['cpus'])
            m.memory = float(json_machine['memory'])

            return m


class SimulationInput:
    prcs: [Process] = []  # array of processes
    machine: Machine = Machine()
    context_switch_time: float = 0
    time_quant: float = 0  # RR

    @staticmethod
    def build(processes_path: str, machine_path: str, cont_switch: float, time_quant: float):
        inp = SimulationInput()

        # sort processes with arrival time
        inp.prcs = sorted(Process.from_json(processes_path),
                          key=lambda x: x.arriv_time)

        inp.context_switch_time = cont_switch
        inp.time_quant = time_quant
        inp.machine = Machine.from_json(machine_path)

        return inp


class SimulationOutput:
    # for each process (1, 2, .. n)
    waiting_times: [float] = []
    turnaround_times: [float] = []
    weighted_turnaround_times: [float] = []

    def print(self):
        json_output = {'waiting_times': self.waiting_times,
                       'turnaround_times': self.turnaround_times,
                       'weighted_turnaround_times': self.weighted_turnaround_times,
                       'average_turnaround': sum(self.turnaround_times)/len(self.turnaround_times),
                       'average_weighted_turnaround': sum(self.weighted_turnaround_times)/len(self.weighted_turnaround_times)}
        print(json.dumps(json_output, indent=4))


def simulate(inp: SimulationInput) -> SimulationOutput:
    out = SimulationOutput()

    # TODO: perform simulation
    raise NotImplementedError()

    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='simulate given processes for a given machine')
    parser.add_argument('machine', help='path to machine.json file')
    parser.add_argument('processes', help='path to processes.json file')
    parser.add_argument('cont_switch', type=float,
                        help='time in seconds to make a context switch')
    parser.add_argument('time_quant', type=float,
                        help='time quantom for RR in seconds')
    args = parser.parse_args()

    # run
    inp = SimulationInput.build(args.processes, args.machine,
                                args.cont_switch, args.time_quant)

    out = simulate(inp)

    out.print()
