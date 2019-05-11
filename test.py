#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: fabian
"""

import pandas as pd
import numpy as np
from tttsituation import TTTSituation

sit1 = TTTSituation(['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'], np.zeros(9))
sit2 = TTTSituation(['X', 'Y', 'L', 'N', 'N', 'N', 'N', 'N', 'N'], np.zeros(9))


def saveSituations(file_path, situations):
    formed = []
    for s in situations:
        dL = s.getSquares()
        dL.extend(s.getActions())
        formed.append(dL)
    dfSituations = pd.DataFrame(formed)
    dfSituations.to_csv(file_path)


def loadSituations(file_path):
    dfTest = pd.read_csv(file_path, index_col=0)
    situations = []
    for s in dfTest.get_values():
        situations.append(TTTSituation(s[:9], s[9:]))
    return situations


saveSituations('situations.csv', [sit1, sit2])

sA = loadSituations('situations.csv')
