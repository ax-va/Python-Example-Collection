import pandas as pd

# These settings allow us to print the whole dataframe without splitting rows:

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
