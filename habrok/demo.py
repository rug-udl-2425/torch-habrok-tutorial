"""
THIS SCRIPT IS USED AS A DEMONSTRATION FOR HABROK
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
import torchvision.transforms as transforms
import argparse

# Argument paraser to showcase how we can pass command line arguments to jobs
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arg', default='defaul_arg', type=str, help='Example command line argument')
    return parser.parse_args()

def main():
    args = parse_args()
    print(f'Passed arguments: arg = {args.arg}')

    # Device agnostic code!
    # Use a GPU if we can. The code must work in both cases
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using {device}', flush=True)
    
    train_dataset = MNIST(root='data', train=True, download=True, transform=transforms.ToTensor())
    test_dataset = MNIST(root='data', train=False, download=True, transform=transforms.ToTensor())
    print('Datasets loaded', flush=True)

    train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    validation_dataloader = DataLoader(test_dataset, batch_size=64)

    mlp = nn.Sequential(
        nn.Flatten(),
        nn.Linear(28*28, 16),
        nn.ReLU(),
        nn.BatchNorm1d(16),
        nn.Linear(16, 16),
        nn.ReLU(),
        nn.BatchNorm1d(16),
        nn.Linear(16, 16),
        nn.ReLU(),
        nn.BatchNorm1d(16),
        nn.Linear(16, 10)
    ).to(device)

    loss_fn = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(params=mlp.parameters(), lr=.001)

    for epoch in range(5):

        # Train step
        mlp.train()
        train_loss, train_acc = 0, 0
        for X, y in train_dataloader:
            X, y = X.to(device), y.to(device)
            y_pred = mlp(X)
            loss = loss_fn(y_pred, y)
            acc = (y_pred.argmax(-1) == y).float().mean()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            train_acc += acc.item()
        train_loss /= len(train_dataloader)
        train_acc /= len(train_dataloader)

        # Evaluation step
        mlp.eval()
        val_loss, val_acc = 0, 0
        for  X, y in validation_dataloader:
            X, y = X.to(device), y.to(device)
            with torch.inference_mode():
                y_pred = mlp(X)
            loss = loss_fn(y_pred, y)
            acc = (y_pred.argmax(-1) == y).float().mean()
            val_loss += loss.item()
            val_acc += acc.item()
        val_loss /= len(validation_dataloader)
        val_acc /= len(validation_dataloader)

        print(
            f'Epoch: {epoch} | \
            Train Loss: {train_loss:.3f} | \
            Train accuracy: {train_acc:.3f} | \
            Validation loss: {val_loss:.3f} | \
            Validation accuracy: {val_acc:.3f}',
            flush=True
        )

    torch.save(mlp.state_dict(), 'models/mlp_demo.pt')

if __name__ == '__main__':
    main()