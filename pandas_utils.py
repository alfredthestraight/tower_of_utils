from typing import List, Dict, Optional, Union, Callable, Iterable, Any
import pandas as pd
import numpy as np
import itertools


def describe_df_using_quantiles_per_column(
        df: pd.DataFrame,
        percentiles: list[float] | None = [0.05, 0.25, 0.5, 0.75, 0.95],
        rounding: int = 2):
    """
    Percentiles per columns in a dataframe
    """
    assert isinstance(percentiles, list)
    assert all(isinstance(x, float) for x in percentiles)
    assert min(percentiles) >= 0
    assert max(percentiles) <= 1

    percentiles = np.array(percentiles)
    df_numerics = df.select_dtypes(include=np.number)
    quantiles_df = df_numerics.apply(
        lambda x: np.round(np.quantile(x, percentiles), rounding), axis=0
    )
    quantiles_df.index = percentiles.round(2).astype("str")
    return quantiles_df


def describe_aggregated_df_using_quantiles_per_column(
    df: pd.DataFrame,
    weight_col_name: str,
    values_col_names: list[str],
    percentiles: list[float] | None = [0.05, 0.25, 0.5, 0.75, 0.95],
):
    """
    Percentiles per columns in a dataframe which contained cumulative
    counts in each of its entries instead of one case per row

    """

    assert isinstance(percentiles, list)
    assert all(isinstance(x, float) for x in percentiles)
    assert min(percentiles) >= 0
    assert max(percentiles) <= 1

    output_dict = {}
    num = df[weight_col_name].sum()
    for values_col_name in values_col_names:
        output_dict[values_col_name] = [
            (df[weight_col_name].multiply(df[values_col_name], fill_value=0.0)).sum()
            / num
        ]
        df_sorted = df.sort_values(by=values_col_name)
        df_sorted["prop_cum"] = (
            df_sorted[weight_col_name].cumsum(skipna=False)
            / df_sorted[weight_col_name].sum()
        )
        for percentile in percentiles:
            output_dict[values_col_name].append(
                df_sorted[df_sorted["prop_cum"] <= percentile][values_col_name].max()
            )

    output_df = pd.DataFrame(output_dict)
    output_df.index = ["mean"] + percentiles
    return output_df
