import random
from typing import List

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import torchmetrics
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, global_add_pool, global_max_pool, global_mean_pool
import pytorch_lightning as pl

from conversion import estee_to_pyg
from generator import generate_dataset_1


def df_to_geometric_data(df: pd.DataFrame) -> List[Data]:
    dataset = []
    for row in range(len(df)):
        graph = df["graph"].iloc[row]
        makespan = df["makespan"].iloc[row]
        (node_features, edge_index) = estee_to_pyg(graph)

        max_duration = max(t.duration for t in graph.tasks.values())
        node_features = node_features / max_duration
        makespan = makespan / max_duration

        data = Data(x=node_features, edge_index=edge_index,
                    y=torch.tensor([makespan], dtype=torch.float32))
        dataset.append(data)
    return dataset


class GCN(torch.nn.Module):
    def __init__(self, num_features: int):
        super().__init__()
        self.conv1 = GCNConv(num_features, 16)
        self.conv2 = GCNConv(16, 32)
        self.node_head = torch.nn.Linear(32, 1)
        self.graph_head = torch.nn.Linear(3, 1)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        x = self.node_head(x)

        sum = global_add_pool(x, data.batch)
        mean = global_mean_pool(x, data.batch)
        max = global_max_pool(x, data.batch)

        result = torch.cat([sum, mean, max], axis=1)

        return self.graph_head(result)


class MakespanPredictor(pl.LightningModule):
    def __init__(self, num_features: int):
        super().__init__()
        self.module = GCN(num_features)

    def forward(self, x):
        return self.module(x)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.01, weight_decay=5e-4)

    def training_step(self, train_batch, batch_idx):
        return self.step(train_batch, "loss")

    def validation_step(self, val_batch, batch_idx):
        return self.step(val_batch, "val_loss")

    def step(self, batch: Data, loss_name: str):
        pred = self.module(batch)
        gt = batch.y.unsqueeze(1)
        loss = F.mse_loss(pred, gt)
        self.log(loss_name, loss)
        return loss


if __name__ == "__main__":
    torch.manual_seed(0)
    np.random.seed(0)
    random.seed(0)

    dataset = generate_dataset_1(1000)
    # print(dataset["graph"][0])
    dataset = df_to_geometric_data(dataset)
    batch_size = 32
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = MakespanPredictor(dataset[0].num_features)

    trainer = pl.Trainer(max_epochs=100, log_every_n_steps=batch_size)
    trainer.fit(model, loader)

    mse = torchmetrics.MeanSquaredError()
    model.eval()
    batch = list(loader)[0]
    pred = model(batch)
    accuracy = mse(pred, batch.y.unsqueeze(1)).detach().numpy()
    print(accuracy)


# 1000 graphs, 100 epochs, LR 0.001: 0.33750963
# 1000 graphs, 100 epochs, LR 0.01: 0.21409684
