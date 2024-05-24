"""
This example introduces Seaborn and is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://seaborn.pydata.org/generated/seaborn.set_theme.html#seaborn.set_theme;
- http://seaborn.pydata.org/tutorial/axis_grids.html#plotting-pairwise-relationships-with-pairgrid-and-pairplot;
- http://seaborn.pydata.org/index.html.
"""
import numpy as np
import pandas as pd
import seaborn as sns  # Relies on Matplotlib
import matplotlib.pyplot as plt

sns.set()
# instead of plt.style.use(...)
# plt.style.use('seaborn-v0_8-whitegrid')

num_points = 100
coef = 0.5
x = np.array(range(num_points))
y = np.random.randn(num_points) * 10 + x * coef
data = pd.DataFrame({'dummy x': x, 'dummy y': y})

# linear regression

sns.lmplot(
    data=data,
    x='dummy x',
    y='dummy y',
    height=4,  # in inches
    aspect=2,  # width / height
    scatter_kws={"color": "slategray"},
    line_kws={"linewidth": 2, "linestyle": "--", "color": "seagreen"},
    markers='D',  # diamonds as plot markers
    ci=68,  # confidence interval of 68%, the standard error estimate
)
plt.tight_layout()  # seaborn shares the Matplotlib global context
plt.savefig('seaborn-figures/figure-1--lmplot-with-linear-regression.svg')
plt.close()

# FacetGrids

tips = sns.load_dataset('tips')
#      total_bill   tip     sex smoker   day    time  size
# 0         16.99  1.01  Female     No   Sun  Dinner     2
# 1         10.34  1.66    Male     No   Sun  Dinner     3
# 2         21.01  3.50    Male     No   Sun  Dinner     3
# 3         23.68  3.31    Male     No   Sun  Dinner     2
# 4         24.59  3.61  Female     No   Sun  Dinner     4
# ..          ...   ...     ...    ...   ...     ...   ...
# 239       29.03  5.92    Male     No   Sat  Dinner     3
# 240       27.18  2.00  Female    Yes   Sat  Dinner     2
# 241       22.67  2.00    Male    Yes   Sat  Dinner     2
# 242       17.82  1.75    Male     No   Sat  Dinner     2
# 243       18.78  3.00  Female     No  Thur  Dinner     2
#
# [244 rows x 7 columns]

g = sns.FacetGrid(
    tips,
    col="smoker",
    height=4,
    aspect=1,
)
g.map(plt.scatter, "total_bill", "tip")
plt.savefig('seaborn-figures/figure-2--FacetGrid-1.svg')
plt.close()

g = sns.FacetGrid(
    tips,
    col="smoker",
    hue="sex",
    hue_kws={"marker": ["D", "s"]},  # D for diamond, s for square
    palette={"Female": "red", "Male": "blue"},
    height=4,
    aspect=1,
)
g.map(plt.scatter, "total_bill", "tip", alpha=.4)
g.add_legend()
plt.savefig('seaborn-figures/figure-3--FacetGrid-2.svg')
plt.close()

g = sns.FacetGrid(
    tips,
    col="smoker",
    row="time",
    hue="sex",
    hue_kws={"marker": ["D", "s"]},  # D for diamond, s for square
    palette={"Female": "red", "Male": "blue"},
    height=4,
    aspect=1,
)
g.map(sns.regplot, "total_bill", "tip")  # regplot for regression
g.add_legend()
plt.savefig('seaborn-figures/figure-4--FacetGrid--regplot.svg')
plt.close()

# Note: FacetGrid and regplot suggest more than lmplot.
# Plot the equivalent graph:
g = sns.lmplot(
    x="total_bill",
    y="tip",
    hue="sex",
    markers=["D", "s"],  # D for diamond, s for square
    col="smoker",
    row="time",
    data=tips,
    palette={"Female": "red", "Male": "blue"},
    height=4,
    aspect=1,
)
g.add_legend()
plt.savefig('seaborn-figures/figure-5--lmplot.svg')
plt.close()


# # # PairGrids for pair-wise comparison (known as a scatter-plot matrix)

iris = sns.load_dataset('iris')
#      sepal_length  sepal_width  petal_length  petal_width    species
# 0             5.1          3.5           1.4          0.2     setosa
# 1             4.9          3.0           1.4          0.2     setosa
# 2             4.7          3.2           1.3          0.2     setosa
# 3             4.6          3.1           1.5          0.2     setosa
# 4             5.0          3.6           1.4          0.2     setosa
# ..            ...          ...           ...          ...        ...
# 145           6.7          3.0           5.2          2.3  virginica
# 146           6.3          2.5           5.0          1.9  virginica
# 147           6.5          3.0           5.2          2.0  virginica
# 148           6.2          3.4           5.4          2.3  virginica
# 149           5.9          3.0           5.1          1.8  virginica
#
# [150 rows x 5 columns]

sns.set_theme(font_scale=1.5)
g = sns.PairGrid(
    iris,
    hue="species",
)
g.map_diag(plt.hist)
g.map_offdiag(plt.scatter)
g.add_legend()
plt.savefig('seaborn-figures/figure-6--PairGrid.svg')
plt.close()
