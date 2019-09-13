import numpy as np

DFLT_UNIT_FAILURE_PROB = 0.01
DFLT_ANY_FAILURE_PROB = 0.5
DFLT_N_UNITS = 70


def any_failure_prob_for(n_units=DFLT_N_UNITS, unit_failure_prob=DFLT_UNIT_FAILURE_PROB):
    """ Probability of at least one failure when we have several units,
    given the probability of a single unit failing"""
    return 1 - ((1 - unit_failure_prob) ** n_units)


def unit_failure_prob_for(n_units=DFLT_N_UNITS, any_failure_prob=DFLT_ANY_FAILURE_PROB):
    return 1 - (1 - any_failure_prob) ** (1 / n_units)


def n_units_for(any_failure_prob=DFLT_ANY_FAILURE_PROB, unit_failure_prob=DFLT_UNIT_FAILURE_PROB):
    return np.log(1 - any_failure_prob) / np.log(1 - unit_failure_prob)


funcs = [any_failure_prob_for, unit_failure_prob_for, n_units_for]

if __name__ == '__main__':
    from py2dash.app_makers import dispatch_funcs

    app = dispatch_funcs(funcs)
    app.run_server(debug=True)
