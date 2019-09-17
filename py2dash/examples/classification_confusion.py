import re
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
from functools import lru_cache

from warnings import warn
warn("This app doesn't fully work yet.")

LRU_CACHE_SIZE = 10
dropbox_dl_pattern = re.compile('(?<=[&\?])dl=\d+')


# example url to use: https://www.dropbox.com/s/qjar1syi9l15juz/Thor.csv?dl=0

def is_dropbox_url(url):
    return 'www.dropbox.com' in url


def url_from_dropbox_url(url):
    return dropbox_dl_pattern.sub('dl=1', url)


@lru_cache(maxsize=LRU_CACHE_SIZE)
def get_csv_data(source, **read_csv_kwargs):
    if isinstance(source, str):
        if source.startswith('http'):
            url = source
            if is_dropbox_url(url):
                source = url_from_dropbox_url(url)
    else:
        raise TypeError("Un recognized source type")

    return pd.read_csv(source, **read_csv_kwargs)


def true_and_pred(source, truth_thresh=0.2, truth_value=1, score_field='scores', truth_field='truth'):
    df = get_csv_data(source)
    y_true = np.array(df[truth_field])
    y_pred = np.zeros(len(y_true))
    y_pred[df[score_field] >= truth_thresh] = truth_value
    return y_true, y_pred


def classification_scores(source, truth_thresh=0.2, truth_value=1, score_field='scores', truth_field='truth'):
    """ Computes the classification scores for truth/prediction data """
    y_true, y_pred = true_and_pred(source, truth_thresh, truth_value, score_field, truth_field)
    print(source)
    return classification_report(y_true, y_pred, output_dict=False)


def complex_classification_scores(source, truth_thresh=0.2, truth_value=1, score_field='scores', truth_field='truth',
                                  labels=None, target_names=None, sample_weight=None, digits=2, output_dict=False
                                  ):
    """ Computes the classification scores for truth/prediction data (with more options) """
    y_true, y_pred = true_and_pred(source, truth_thresh, truth_value, score_field, truth_field)

    return classification_report(y_true, y_pred, labels=labels,
                                 target_names=target_names, sample_weight=sample_weight, digits=digits,
                                 output_dict=output_dict)


if __name__ == '__main__':
    from py2misc.dispatch_anything import dispatch_funcs

    # from functools import wraps
    # _classification_scores = classification_scores
    # @wraps(_classification_scores)
    # def classification_scores(*args, **kwargs):
    #     d = _classification_scores(*args, **kwargs)
    #     d = pd.DataFrame(d)[['0', '1']]
    #     return d.to_html()

    funcs = [classification_scores, get_csv_data, complex_classification_scores, true_and_pred]

    dispatch_funcs(funcs, interface='dash')
