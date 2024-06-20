import sorobn as hh
import pandas as pd

bn = hh.BayesNet(
    ('C', ['S', 'R']),
    ('S', 'W'),
    ('R', 'W'))

bn.P['C'] = pd.Series({True: 0.5, False: 0.5})
bn.P['S'] = pd.Series({
    (True, True): 0.1, (True, False): 0.9,
    (False, True): 0.5, (False, False): 0.5})
bn.P['R'] = pd.Series({
    (True, True): 0.8, (True, False): 0.2,
    (False, True): 0.2, (False, False): 0.8})
bn.P['W'] = pd.Series({
    (True, True, True): 0.99, (True, True, False): 0.01,
    (True, False, True): 0.9, (True, False, False): 0.1,
    (False, True, True): 0.95, (False, True, False): 0.05,
    (False, False, True): 0.05, (False, False, False): 0.95})

bn.prepare()
bn.query('C', event = {'S': False, 'W': True})
