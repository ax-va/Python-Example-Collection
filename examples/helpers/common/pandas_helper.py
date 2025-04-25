import functools

import pandas as pd


def df_to_str(df: pd.DataFrame) -> str:
    """
    Converts a dataframe into a human-friendly string.

    Args:
        df: pd.DataFrame

    Returns:
        dataframe as a human-friendly string
    """
    # Set Pandas configuration
    pd.set_option("display.max_rows", len(df))
    pd.set_option("display.max_columns", len(df.columns))
    pd.set_option("expand_frame_repr", False)

    # Make string
    df_str = df.to_string()
    num_chars = len(df_str.split("\n")[0])

    # Separate dataframe with "-"
    df_str = "\n" + "-" * num_chars + "\n" + df_str + "\n" + "-" * num_chars

    # Set to defaults
    pd.set_option("display.max_rows", 60)
    pd.set_option("display.max_columns", 0)
    pd.set_option("expand_frame_repr", True)
    return df_str


def print_df(df: pd.DataFrame) -> None:
    """
    Prints a dataframe as a human-friendly string.
    Args:
        df: pd.DataFrame
    """
    print(df_to_str(df))


def print_full_df_content(func):
    """Use this decorator to print the full content of dataframe."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Save current settings
        original_settings = {
            "display.max_columns": pd.get_option("display.max_columns"),
            "display.max_rows": pd.get_option("display.max_rows"),
            "display.width": pd.get_option("display.width"),
            "display.colheader_justify": pd.get_option("display.colheader_justify"),
            "display.max_colwidth": pd.get_option("display.max_colwidth"),
        }

        # Show all columns
        pd.set_option("display.max_columns", None)
        # Show all rows
        pd.set_option("display.max_rows", None)
        # Don't split the rows to the next lines
        pd.set_option("display.width", None)
        # Align column headers to the left
        pd.set_option("display.colheader_justify", "left")
        # Set the option to display full column width
        pd.set_option("display.max_colwidth", None)

        result = func(*args, **kwargs)

        # Restore original settings
        for option, value in original_settings.items():
            pd.set_option(option, value)

        return result

    return wrapper
