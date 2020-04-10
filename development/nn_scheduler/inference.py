from data_loader.dataloader import SchedDataset
from model import SchedNN
import torch.nn as nn
from torch.utils.data import DataLoader
from timeit import default_timer
import numpy as np
import argparse
import torch
import math
import os

def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('--machines_path', help='Path to the machines csv.', type=str, default="data/machines/machines.csv")
    parser.add_argument('--jobs_dir', help='Path to the jobs csvs.', type=str, default="data/jobs/")
    parser.add_argument('--results_dir', help='Path to the results csvs.', type=str, default="data/schedules/")
    parser.add_argument('--model_path', help='Path to the trained model file.', type=str, default="checkpoints/final_model_100.pt")
    parser.add_argument('--batch_size', help='Batch size.', type=int, default=8)

    args = parser.parse_args(args)

    if (os.path.isdir("data/outputs/")):
        os.mkdir("data/outputs/")
    
    device = "cuda:0" if torch.cuda.is_available else "cpu"

    dataset = SchedDataset(args.machines_path, args.jobs_dir, args.results_dir)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, num_workers=4)
    data_iterator = iter(dataloader)

    model = torch.load(args.model_path)

    model.eval()

    steps_num = int(math.ceil(len(dataset)/ args.batch_size))

    print("The model contains: {} parameters".format(sum(p.numel() for p in model.parameters())))
    print("Inference on {} samples".format(len(dataset)))

    start_time = default_timer()

    for step in range(steps_num):
        X_machine, X_job, Y_machine, Y_time = next(data_iterator)
        X_machine = X_machine.to(device)
        X_job = X_job.to(device)
        out_machine, out_time = model(X_machine, X_job)
        print("Saving output #{} ...".format(step))
        np.save("data/outputs/{}_machines.npy".format(step), out_machine.cpu().detach().numpy())
        np.save("data/outputs/{}_times.npy".format(step), out_time.cpu().detach().numpy())
    
    print("Inference finished in {}".format(default_timer()-start_time))    

if __name__ == '__main__':
    main()
