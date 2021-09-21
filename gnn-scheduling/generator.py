from collections import deque
from itertools import chain

import estee.common
import torch
from estee.generators import elementary
from torch_geometric.data import Data
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv


def estee_to_pyg(graph: estee.common.TaskGraph) -> Data:
    edges_from = []
    edges_to = []

    to_visit = deque(graph.source_tasks())
    visited = set()
    while to_visit:
        node = to_visit.popleft()
        if node in visited:
            continue
        visited.add(node)
        consumers = chain.from_iterable(o.consumers for o in node.outputs)
        for consumer in consumers:
            if consumer not in visited:
                edges_from.append(node.id)
                edges_to.append(consumer.id)
                to_visit.append(consumer)

    assert len(edges_from) == len(edges_to)
    edge_index = torch.tensor([edges_from, edges_to], dtype=torch.long)
    nodes = [task for (_, task) in sorted(graph.tasks.items(), key=lambda x: x[0])]
    features = [len(list(chain.from_iterable(o.consumers for o in node.outputs))) for node in
                nodes]

    x = torch.tensor([features], dtype=torch.float)

    return Data(x=x, edge_index=edge_index)


class GCN(torch.nn.Module):
    def __init__(self, num_features: int, label_size: int):
        super().__init__()
        self.conv1 = GCNConv(num_features, 16)
        self.conv2 = GCNConv(16, label_size)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)

        return F.log_softmax(x, dim=1)


g = elementary.merge_neighbours(10)
# data = estee_to_pyg(g)
#
# dataset = list(data)
dataset = Planetoid(root='/tmp/Cora', name='Cora')
loader = DataLoader(dataset, batch_size=32, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GCN(dataset.num_features, dataset.num_classes).to(device)
data = dataset[0].to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    print(epoch, loss)
    loss.backward()
    optimizer.step()


model.eval()
pred = model(data).argmax(dim=1)
correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
acc = int(correct) / int(data.test_mask.sum())
print('Accuracy: {:.4f}'.format(acc))
