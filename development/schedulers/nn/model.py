from __future__ import print_function
import torch 
import torch.nn as nn
import torch.nn.functional as F

class JobEncoder(nn.Module):
    """
        Implementation of the encoder network for jobs.
    """
    def __init__(self, input_dim, enc_hid_dim, dec_dim):
        """
            initialization method

            Parameters:
            input_dim(int): number of input features to the RNN cell.
            enc_hid_dim(int): number of hidden units for the RNN cell.
            dec_dim(int): number of units in the decoder network, usually equal to the maximum number of jobs.
        """
        super(JobEncoder, self).__init__()
        
        self.rnn = nn.GRU(input_dim, enc_hid_dim, bidirectional = True)
        
        self.fc = nn.Linear(enc_hid_dim * 2, dec_dim)
        
    def forward(self, input):
        """
            forward propagation method

            Parameters:
            input(Tensor): input to the RNN layers.

            Returns:
            outputs(Tensor): outputs of the RNN layers.
            hidden(Tensor): hidden units of the last two layers.
        """
        outputs, hidden = self.rnn(input)

        hidden = torch.tanh(self.fc(torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim = 1)))

        return outputs, hidden

class MachineEncoder(nn.Module):
    """
        Implementation of the encoder network for machines.
    """
    def __init__(self, input_dim, input_features, dec_dim):
        """
            initialization method

            Parameters:
            input_dim(int): number of inputs for the encoder, equal to the number of machines.
            input_features(int): number of features for each input.
            dec_dim(int): number of units in the decoder network, usually equal to the maximum number of jobs.
        """
        super(MachineEncoder, self).__init__()
        
        self.conv1d = nn.Conv1d(input_features, 1, kernel_size=1, stride=1, padding=0)

        self.fc = nn.Linear(input_dim, dec_dim)
        
    def forward(self, input):
        """
            forward propagation method

            Parameters:
            input(Tensor): input to the conv1d layer

            Returns:
            outputs(Tensor): outputs of the fully connected layer
        """
        outputs =  self.conv1d(input)

        outputs =  torch.tanh(self.fc(outputs.view(-1, outputs.shape[-1])))

        return outputs     
           

class SchedNN(nn.Module):
    """
        Implementation of the proposed network for scheduling.
    """
    def __init__(self, max_jobs, num_machines, rnn_hid_dim, machine_dim=3, job_dim=4):
        """
            initialization method

            Parameters:
            num_machines(int): number of machines.
            max_jobs(int): maximum number of jobs.
            rnn_hid_dim(int): number of hidden units in the RNN layers.
            machine_dim(int): number of data features for each machine [num_cores, core_freq, mem_cap].
            job_dim(int): number of data features for each job [arrival_time, avg_burst_time, mem_util, priority].
        """
        super(SchedNN, self).__init__()

        self.job_enc = JobEncoder(job_dim, rnn_hid_dim, max_jobs)

        self.machine_enc = MachineEncoder(num_machines, machine_dim, max_jobs)

        self.conv1d_1 = nn.Conv1d(2, 2, kernel_size=1, stride=1, padding=0)

        self.conv1d_2 = nn.Conv1d(2, num_machines, kernel_size=1, stride=1, padding=0)

    def forward(self, machine_input, job_input):
        """
            forward propagation method

            Parameters:
            machine_input(Tensor): batch of machines to be utilized, dim=(batch_size,num_machines,machine_dim)
            job_input(Tensor): batch of the list of jobs to be scheduled, dim=(batch_size,num_jobs,job_dim)

            Returns:
            Tensor: n timesteps with scheduled jobs for each machine.
        """    
        job_input = torch.transpose(job_input, 1, 0)

        machine_features = self.machine_enc(machine_input)

        _, job_features = self.job_enc(job_input)

        feature_fusion = torch.stack([machine_features, job_features], dim=1)

        time_output = self.conv1d_1(feature_fusion)

        machine_output = self.conv1d_2(feature_fusion)

        return machine_output, time_output