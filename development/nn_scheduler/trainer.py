from data_loader.dataloader import SchedDataset
from model import SchedNN
import torch.nn as nn
from torch.utils.data import DataLoader
import argparse
import torch
import math
import os

def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('--machines_path', help='Path to the machines csv.', type=str, default="data/machines/machines.csv")
    parser.add_argument('--jobs_dir', help='Path to the jobs csvs.', type=str, default="data/jobs/")
    parser.add_argument('--results_dir', help='Path to the results csvs.', type=str, default="data/schedules/")
    parser.add_argument('--batch_size', help='Batch size.', type=int, default=8)
    parser.add_argument('--learning_rate', help='Learning rate.', type=float, default=1e-5)
    parser.add_argument('--num_epochs', help='Number of epochs.', type=int, default=100)
    parser.add_argument('--max_jobs', help='Maximum number of jobs.', type=int, default=485)
    parser.add_argument('--num_machines', help='Number of machines to be used.', type=int, default=123)
    parser.add_argument('--rnn_hid_dim', help='Number of hidden units in encoder RNN.', type=int, default=16)
    parser.add_argument('--machine_dim', help='Number of features per machine.', type=int, default=3)
    parser.add_argument('--job_dim', help='Number of features per job.', type=int, default=4)

    args = parser.parse_args(args)

    if (os.path.isdir("checkpoints/")):
        os.mkdir("checkpoints/")
    
    device = "cuda:0" if torch.cuda.is_available else "cpu"

    dataset = SchedDataset(args.machines_path, args.jobs_dir, args.results_dir, args.max_jobs)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, num_workers=4)
    data_iterator = iter(dataloader)

    model = SchedNN(max_jobs=args.max_jobs, num_machines=args.num_machines, rnn_hid_dim=args.rnn_hid_dim, \
                    machine_dim=args.machine_dim, job_dim=args.job_dim).to(device)

    print("The model contains: {} parameters.".format(sum(p.numel() for p in model.parameters())))

    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)

    criterion_1 = nn.MSELoss()
    criterion_2 = nn.CrossEntropyLoss()

    steps_per_epoch = int(math.ceil(len(dataset)/ args.batch_size))

    for epoch in range(1,args.num_epochs+1):
        loss_per_epoch = 0
        for step in range(steps_per_epoch):
            X_machine, X_job, Y_machine, Y_time = next(data_iterator)
            X_machine = X_machine.to(device)
            X_job = X_job.to(device)
            Y_machine = Y_machine.to(device)
            Y_time = Y_time.to(device)
            optimizer.zero_grad()
            out_machine, out_time = model(X_machine, X_job)
            Y_machine = Y_machine.view(-1).to(torch.long)
            out_machine = torch.transpose(out_machine, 2, 1).reshape(-1,args.num_machines)
            loss = criterion_1(out_time, Y_time) + criterion_2(out_machine, Y_machine)
            loss.backward()
            optimizer.step()
            loss_per_epoch += loss.item()
            print("EPOCH [{}/{}], ITER [{}/{}]: Overall Loss : {:.4f}".format(epoch, args.num_epochs, step, steps_per_epoch, loss_per_epoch/(step+1)))    
        if (epoch % 5 == 0):    
            torch.save(model, "checkpoints/final_model_{}.pt".format(epoch))    
        scheduler.step()     
        data_iterator = iter(dataloader)
        print("EPOCH [{}/{}]: Overall Loss : {:.4f}".format(epoch, args.num_epochs, loss_per_epoch/steps_per_epoch))
        

if __name__ == '__main__':
    main()
