import pandas as pd
import numpy as np


def split_into_train_df_and_test_df(df: pd.DataFrame, test_prop: float):
    test_indices = np.random.choice(range(0, df.shape[0]-1),
                                    size=int(df.shape[0]*test_prop),
                                    replace=False)
    df_train = df[~df.index.isin(test_indices.tolist())]
    df_test = df[df.index.isin(test_indices.tolist())]
    return df_train, df_test