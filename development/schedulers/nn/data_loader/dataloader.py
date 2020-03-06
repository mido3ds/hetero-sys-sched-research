from torch.utils.data import Dataset 
import torchvision.transforms as transform
import torch
import pandas as pd
import numpy as np  
import os

class SchedDataset(Dataset):
    """
        Implementation of the custom dataset for scheduling data.
    """
    def __init__(self, machines_path, jobs_dir, results_dir):
        """
            initialization method

            Parameters:
            machines_path(string): path to the csv file that contains machines information.
            jobs_dir(string): directory of jobs lists.
            results_dir(string): directory of scheduling results.
        """
        self.jobs_list = os.listdir(jobs_dir)
        self.results_list = os.listdir(results_dir)

        self.machines_list = pd.read_csv(machines_path)
        del self.machines_list["machine_id"]

        self.machines_list = torch.from_numpy(self.machines_list.to_numpy())

    def __getitem__(self, idx):
        """
            returns a single dataset item

            Parameters:
            idx(int): index of required dataset item.

            Returns:
            machines_list(Tensor): machines information tensor.
            job_list(Tensor): job information tesnor.
            out_machines(Tensor): machines running each job in the list.
            out_time(Tensor): start and finish time of each job in the list.
        """
        job_list = pd.read_csv(self.jobs_list[idx])
        del job_list["job_id"]

        job_list = torch.from_numpy(job_list.to_numpy())

        out_list = pd.read_csv(self.results_list[idx])
        del out_list["job_id"]

        out_list = torch.from_numpy(out_list.to_numpy())

        out_machines = out_list[:,0]

        out_time = out_list[:,1:]

        return self.machines_list, job_list, out_machines, out_time

    def __len__(self):
        """
            returns the length of the dataset

            Returns:
            length(int): length of dataset items.
        """
        return len(self.jobs_list)
