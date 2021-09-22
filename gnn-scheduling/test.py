import json
import random
from typing import List

import numpy as np
import pandas as pd
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
import torchmetrics
from estee.serialization.dask_json import deserialize_graph, serialize_graph
from kitt.data import train_test_split
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, global_add_pool, global_max_pool, global_mean_pool
from torchmetrics import MeanAbsoluteError

from conversion import estee_to_pyg
from generator import generate_dataset_1
from utils import timer

MAX_DURATION = 50


class Normalizer:
    def normalize(self, value):
        return value / MAX_DURATION

    def denormalize(self, value):
        return value * MAX_DURATION


def df_to_geometric_data(df: pd.DataFrame) -> List[Data]:
    dataset = []
    for row in range(len(df)):
        graph = df["graph"].iloc[row]
        makespan = df["makespan"].iloc[row]
        (node_features, edge_index) = estee_to_pyg(graph)

        max_duration = MAX_DURATION  # max(t.duration for t in graph.tasks.values())
        node_features = node_features / max_duration
        makespan = makespan / max_duration

        data = Data(x=node_features, edge_index=edge_index,
                    y=torch.tensor([makespan], dtype=torch.float32))
        dataset.append(data)
    return dataset


class GCN(torch.nn.Module):
    def __init__(self, num_features: int):
        super().__init__()
        self.conv1 = GCNConv(num_features, 32)
        self.conv2 = GCNConv(32, 32)
        self.node_head1 = torch.nn.Linear(32, 32)
        self.node_head2 = torch.nn.Linear(32, 32)
        self.graph_head = torch.nn.Linear(96, 1)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        # x = F.dropout(x, p=0.2, training=self.training)
        # x = self.conv2(x, edge_index)
        # x = self.node_head1(x)

        sum = global_add_pool(x, data.batch)
        mean = global_mean_pool(x, data.batch)
        max = global_max_pool(x, data.batch)

        x = torch.cat([sum, mean, max], axis=1)
        x = self.graph_head(x)
        return x


class MakespanPredictor(pl.LightningModule):
    def __init__(self, num_features: int, normalizer: Normalizer):
        super().__init__()
        self.module = GCN(num_features)
        self.normalizer = normalizer
        self.mae = MeanAbsoluteError()

    def forward(self, x):
        return self.module(x)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.01, weight_decay=5e-4)

    def training_step(self, train_batch, batch_idx):
        return self.step(train_batch, "loss")[2]

    def validation_step(self, val_batch, batch_idx):
        pred, gt, loss = self.step(val_batch, "val_loss")
        pred_dn = self.normalizer.denormalize(pred)
        gt_dn = self.normalizer.denormalize(gt)
        acc = self.mae(pred_dn, gt_dn)
        self.log("val_mae", acc, prog_bar=True)

    def step(self, batch: Data, loss_name: str):
        pred = self.module(batch)
        gt = batch.y.unsqueeze(1)
        loss = F.mse_loss(pred, gt)
        prog_bar = "val" in loss_name
        self.log(loss_name, loss, prog_bar=prog_bar)
        return pred, gt, loss


def save_dataset(path: str, dataset: pd.DataFrame):
    graphs = [serialize_graph(g) for g in dataset["graph"]]
    makespans = list(dataset["makespan"])
    data = {
        "graphs": graphs,
        "makespans": makespans
    }

    with open(path, "w") as f:
        f.write(json.dumps(data))


def load_dataset(path: str):
    with open(path) as f:
        data = json.load(f)
        return pd.DataFrame({
            "graph": [deserialize_graph(g) for g in data["graphs"]],
            "makespan": data["makespans"]
        })


if __name__ == "__main__":
    torch.manual_seed(0)
    np.random.seed(0)
    random.seed(0)

    with timer("generate"):
        dataset = generate_dataset_1(3)
        save_dataset("dataset1.json", dataset)
        # dataset = load_dataset("dataset1.json")

    with timer("convert"):
        dataset = df_to_geometric_data(dataset)

    train_dataset, val_dataset = train_test_split(dataset, 0.2)

    batch_size = 32
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    if val_dataset:
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    else:
        val_loader = None

    model = MakespanPredictor(dataset[0].num_features, Normalizer())

    max_epochs = 1000
    trainer = pl.Trainer(max_epochs=max_epochs, log_every_n_steps=batch_size)
    trainer.fit(model, train_loader, val_loader)

    mae = torchmetrics.MeanAbsoluteError()
    model.eval()


    def eval_dataset(dataset):
        batch = list(dataset)[0]
        pred = model(batch)
        error = mae(pred, batch.y.unsqueeze(1)).detach().numpy()
        print(error, pred, batch.y)


    print("Train")
    eval_dataset(train_loader)
    if val_loader:
        print("Val")
        eval_dataset(val_loader)

# 1000 graphs, 100 epochs, LR 0.001: 0.33750963
# 1000 graphs, 100 epochs, LR 0.01: 0.21409684
