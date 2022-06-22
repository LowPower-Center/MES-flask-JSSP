# import pstats
# from pstats import SortKey
#
# p = pstats.Stats('./restats')
# p.strip_dirs().sort_stats('cumtime').print_stats()

#read and show .npy
import numpy as np
context = np.load('./my_generatedData10_10.npy',encoding="latin1")
print(context)
