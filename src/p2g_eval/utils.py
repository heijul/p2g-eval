import functools

import pandas as pd


SPECIAL_CHARS = "\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF"


def normalize_series(raw_series: pd.Series) -> pd.Series:
    """ Normalize the series and remove symbols. """

    def _normalize(series: pd.Series) -> pd.Series:
        """ Lower and casefold the series. """
        return series.str.lower().str.casefold()

    def _remove_forbidden_chars(series: pd.Series) -> pd.Series:
        """ Remove parentheses and their content and special chars. """

        # Match parentheses and all text enclosed by them.
        parentheses_re = r"(\(.*\))"
        # Match all chars other than the allowed ones.
        char_re = fr"([^a-zA-Z\d\|{SPECIAL_CHARS} ])"
        regex = "|".join([parentheses_re, char_re])
        return series.str.replace(regex, " ", regex=True)

    return raw_series.pipe(_normalize).pipe(_remove_forbidden_chars)


@functools.cache
def normalize_name(name: str) -> str:
    """ Normalize the given name. Simple wrapper function for a single str. """
    return normalize_series(pd.Series([name])).iloc[0]
