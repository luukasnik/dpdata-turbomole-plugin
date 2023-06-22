from dpdata.format import Format
from .turbomole_data import to_system_data
import numpy as np

@Format.register("turbomole")
class TurbomoleFormat(Format):
    def from_system(self, N, **kwargs):
        return {
            "atom_numbs": [20],
            "atom_names": ['X'],
            "atom_types": [0] * 20,
            "cells": np.repeat(np.diag(np.diag(np.ones((3, 3))))[np.newaxis,...], N, axis=0) * 100.,
            "coords": np.random.rand(N, 20, 3) * 100.,
        }

    def from_labeled_system(self, file_name, md=True, **kwargs):
        return to_system_data(file_name, md = True)