from math import log

DFLT_UNIT_FAILURE_PROB = 0.01
DFLT_ANY_FAILURE_PROB = 0.5
DFLT_N_UNITS = 70


def any_failure_prob_for(n_units=DFLT_N_UNITS, unit_failure_prob=DFLT_UNIT_FAILURE_PROB):
    """ Probability of at least one failure when we have several units,
    given the probability of a single unit failing"""
    return 1 - ((1 - unit_failure_prob) ** n_units)


def n_units_for(any_failure_prob=DFLT_ANY_FAILURE_PROB, unit_failure_prob=DFLT_UNIT_FAILURE_PROB):
    """n_units for which we get a given 'any failure' probability for a given unit failure probability
    This can be useful if we want to know how many units we need to monitor if we want to be
    `any_failure_prob` sure to observe at least one failure.
    """
    return log(1 - any_failure_prob) / log(1 - unit_failure_prob)


def unit_failure_prob_for(n_units=DFLT_N_UNITS, any_failure_prob=DFLT_ANY_FAILURE_PROB):
    """ If we know the 'any failure' probability, and the number of units: What's the unit failure probability?
    This can be useful if the data we have is the proportion of times there's at least one failure in a fixed-size
    period, and we want to know what the unit failure probability is.
    """
    return 1 - (1 - any_failure_prob) ** (1 / n_units)


funcs = [any_failure_prob_for, unit_failure_prob_for, n_units_for]

if __name__ == '__main__':
    from py2dash.app_makers import dispatch_funcs

    app = dispatch_funcs(funcs)
    app.run_server(debug=True)
