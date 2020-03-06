from data_loader.dataloader import SchedDataset
from model import SchedNN
import torch.nn as nn
from torch.utils.data import DataLoader
import argparse
import torch
import math

def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('--machines_path', help='Path to the machines csv.', type=str, default="data/machines/machines.csv")
    parser.add_argument('--jobs_dir', help='Path to the jobs csvs.', type=str, default="data/jobs/")
    parser.add_argument('--results_dir', help='Path to the results csvs.', type=str, default="data/schedules/")
    parser.add_argument('--batch_size', help='Batch size.', type=int, default=8)
    parser.add_argument('--num_epochs', help='Number of epochs.', type=int, default=100)

    args = parser.parse_args(args)
    
    device = "cuda:0" if torch.cuda.is_available else "cpu"

    dataset = SchedDataset(args.machines_path, args.jobs_dir, args.results_dir)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, num_workers=4)
    data_iterator = iter(dataloader)

    model = SchedNN().to(device)

    print("The model contains: {} parameters.".format(sum(p.numel() for p in model.parameters())))

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=15, gamma=0.5)

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
            loss = criterion_1(out_machine, Y_machine) + criterion_2(out_time, Y_time)
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
