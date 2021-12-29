"""
Created by SungMin Yoon on 2021-02-22..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import numpy as np


# target 값과 가장 유사한 값의 인덱스
def min_diff_pos(array_like, target):
    return np.abs(np.array(array_like) - target).argmin()