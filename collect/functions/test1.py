import numpy as np
import pandas as pd
import random

time_dict1 = {}
for n in range(2023 - 1985):
    time_dict1[str(1985 + n)] = np.arange(0, 12)
print(time_dict1)
if 2020 != 1985:
    for o in range(2020 - 1985):
        del time_dict1[str(1985 + o)]

# time_dict_len = len(
#    [item for sublist in (time_dict1[x] for x in time_dict1.keys()) for item in sublist]
# )
print(np.random.choice(time_dict1["2021"], size=1))
