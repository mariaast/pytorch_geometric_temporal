import torch
import numpy as np
from torch_geometric.data import Data
from typing import List, Union

Edge_Index = Union[np.ndarray, None] 
Edge_Weight = Union[np.ndarray, None]

class StaticGraphDiscreteSignal(object):
    r""" A data iterator object to contain a static graph with a dynamically 
    changing discrete temporal feature set (multiple signals). The node labels
    (target) are also temporal. The iterator returns a single discrete temporal
    snapshot for a time period (e.g. day or week). The iterator returns a single
    snapshot as a Pytorch Geometric Data object.
 
    Args:
        edge_index (Numpy array): Index tensor of edges.
        edge_weight (Numpy array): Edge weight tensor.
        features (): Node feature tensor.
        targets (): Node label (target) tensor.
    """
    def __init__(self, edge_index: Edge_Index, edge_weight: Edge_Weight, features, targets):
        self.edge_index = edge_index
        self.edge_weight = edge_weight
        self.features = features
        self.targets = targets

    def _get_edge_index(self):
        if self.edge_index is None:
            return self.edge_index
        else:
            return torch.LongTensor(self.edge_index)

    def _get_edge_weight(self):
        if self.edge_weight is None:
            return self.edge_weight
        else:
            return torch.FloatTensor(self.edge_weight)

    def _get_features(self): 
        if self.features[self.t] is None:
            return self.features[self.t]
        else:       
            return torch.FloatTensor(self.features[self.t])

    def _get_target(self):
        if self.targets[self.t] is None:
            return self.targets[self.t]
        else:
            if self.targets[self.t].dtype.kind == 'i':
                return torch.LongTensor(self.targets[self.t])
            elif self.targets[self.t].dtype.kind == 'f':
                return torch.FloatTensor(self.targets[self.t])
         

    def _get_snapshot(self):
        x = self._get_features()
        edge_index = self._get_edge_index()
        edge_weight = self._get_edge_weight()
        y = self._get_target()

        snapshot = Data(x = x,
                        edge_index = edge_index,
                        edge_attr = edge_weight,
                        y = y)
        return snapshot

    def __next__(self):
        if self.t < len(self.features):
            snapshot = self._get_snapshot()
            self.t = self.t + 1
            return snapshot
        else:
            self.t = 0
            raise StopIteration

    def __iter__(self):
        self.t = 0
        return self
