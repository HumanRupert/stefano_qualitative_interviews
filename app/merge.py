import time
import typing as T

import pandas as pd


def merge(regions: T.List[str]):
    df = pd.DataFrame()

    for region in regions:
        reg_df = pd.read_csv(f"out/{region}.csv")
        df = pd.concat([reg_df, df], ignore_index=True)

    df.to_csv(f"out/all_{int(time.time() * 1000)}.csv")
