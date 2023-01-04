import sys
from pathlib import Path

module_path = Path(__file__).parents[1]
if module_path not in sys.path:
    sys.path.append(str(module_path))

from multiprocessing import Pool
import pickle

from src.tsp_problem import TSPProblem
from src.algorithms.methods import Method

problem = TSPProblem(no_runs=100)

items = items = [
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
    (("TSPC",), [Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM]),
]

with Pool() as pool:
    grades_tmp = pool.starmap(problem.run, items)

pickle.dump(grades_tmp, open("grades_tmp.pkl", "wb"))

print("Done!")
