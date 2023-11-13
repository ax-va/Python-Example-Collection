import pandas as pd
from pandas import option_context


def dataframe_to_str(df: pd.DataFrame) -> str:
    """
    Create a user-friendly str from a pd.DataFrame.
    """
    with option_context(
            "display.max_rows", len(df),
            "display.max_columns", len(df.columns),
            "expand_frame_repr", False,
    ):
        df_str = df.to_string()
        char_num = len(df_str.split("\n")[0])
        df_str = "\n" + "-" * char_num + "\n" + df_str + "\n" + "-" * char_num
    return df_str
