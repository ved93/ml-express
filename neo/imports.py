

import pandas as pd
import numpy as np


from datetime import datetime, date


# def measure_time(func):
#     def _measure_time(*args, **kwargs):
#         t0 = datetime.now()
#         # print(args,kwarg)
#         ret = func(*args, **kwargs)
#         print(str(datetime.now() - t0))
#         return ret
#     return _measure_time