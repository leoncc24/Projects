from config.settings import TRAIN_TEST_SPLIT
from analysis.var_model import train_var_model
from itertools import combinations

TRAIN_TEST_SPLIT = 0.8

def find_best_target_vars(data, sp500_col, candidate_vars, features, top_n=4, combo_size=4):
    """
    Finds the best combinations of features (of length combo_size) that minimize RMSE.
    """
    results = []
    for combo in combinations(features, combo_size):
        try:
            res = train_var_model(data, sp500_col, list(combo))
            results.append({
                'features': combo,
                'rmse': res['rmse'],
                'nrmse': res['nrmse']
            })
        except Exception as e:
            print(f"Error with combination {combo}: {e}")
            continue
    best = sorted(results, key=lambda x: x['rmse'])[:top_n]
    return best


