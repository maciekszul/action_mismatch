import numpy as np


def oddball_sequence(trial_no, prop_dev):
    """
    trial_no - amount of trials 
    prop_dev - proportion of deviants
    """
    dev_no = int(np.round(trial_no * prop_dev, decimals=0))
    reg_no = trial_no - dev_no
    seq = np.hstack([np.tile(1, reg_no), np.tile(-1,dev_no)])
    np.random.shuffle(seq)
    return seq

