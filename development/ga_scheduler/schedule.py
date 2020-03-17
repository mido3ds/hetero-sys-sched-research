import argparse
import json

import genetic_algorithm

def main():
    """
        genetic scheduling driver function
    """
    # Get arguments
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--data_path', type=str, default='data/jobs.json',
                            help='path to data json')
    args = argparser.parse_args()                        

    # Get data
    with open(args.data_path) as f:
        data = json.load(f)

    raw_tasks = data['tasks']
    tasks = []
    for task in raw_tasks:
        dependencies = task['depend']
        if dependencies:
            dependencies = [dependencies]

        t = genetic_algorithm.Job(task['id'], task['length'], task['priority'], dependencies)
        tasks.append(t)

    # Setup dependencies
    for task in tasks:
        dependencies = []
        for depend_id in task.dependencies:
            for t2 in tasks:
                if t2.id == depend_id:
                    dependencies.append(t2)
                    break
            else:
                raise Exception('Invalid dependency')
        task.dependencies = dependencies

    constraints = data['constraints']

    processors = constraints['processors']
    generations = constraints['generations']
    total_time = constraints['total_time']

    gen_alg = genetic_algorithm.GeneticTaskScheduler(tasks)
    schedule = gen_alg.schedule_tasks(processors, generations, total_time)

    # Display the schedule
    for i, processor in enumerate(schedule):
        print(f"Processor #{i} ...")
        for j, task in enumerate(processor):
            if task:
                print(task)


if __name__ == "__main__":
    main()