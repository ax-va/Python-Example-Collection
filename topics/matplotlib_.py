"""
This example introduces Matplotlib and is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://ipython.readthedocs.io/en/stable/;
- https://matplotlib.org/1.2.1/api/matplotlib_configuration_api.html;
- https://matplotlib.org/1.4.0/users/customizing.html#the-matplotlibrc-file;
- https://matplotlib.org/1.4.0/users/customizing.html#a-sample-matplotlibrc-file;
- https://matplotlib.org/stable/users/explain/figure/backends.html;
- https://ipython.readthedocs.io/en/stable/overview.html#decoupled-two-process-model;
- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html;
- https://matplotlib.org/stable/users/explain/colors/colormaps.html.
"""
# How to run Jupyter QtConsole:
# 1) Install PySide6 and qtconsole
# 2) Run in the terminal: jupyter qtconsole
import numpy as np
import pandas as pd
import cycler
import matplotlib.pyplot as plt
from datetime import datetime

# # # pyplot’s global state

# Create a pandas datetime index with 200 day (d) elements, starting from the current time
x = pd.period_range(datetime(year=2023, month=12, day=31), periods=200, freq='d')
# Convert datetime index to Python datetimes
x = x.to_timestamp().to_pydatetime()
# Create three 200-element random arrays summed along the 0 axis
rng = np.random.default_rng(seed=42)
y = np.random.standard_normal(size=(200, 3)).cumsum(0)
plt.plot(x, y)
plt.savefig('matplotlib-figures/example-01--global-state.svg')
plt.close()

# # # Configure Matplotlib

plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.prop_cycle'] = cycler.cycler(color=['k', 'y', 'm'])
plt.plot(x, y)
plt.savefig('matplotlib-figures/example-02--rcParams.svg')
plt.close()

# # # Set the figure’s size

# Two ways to set the figure size to 8 by 4 inches
plt.rcParams['figure.figsize'] = (8, 4)
plt.gcf().set_size_inches(8, 4)
plt.plot(x, y)
plt.savefig('matplotlib-figures/example-03--figure-size.svg')
plt.close()

# solid (-), dashed (--), and dash-dotted (-.) lines

# plots = plt.plot(x,y)
plots = plt.plot(x, y[:,0], '-', x, y[:,1], '--', x, y[:,2], '-.')
plt.savefig('matplotlib-figures/example-04--styled-lines.svg')
plt.close()

# legend
plots = plt.plot(x, y)
plt.legend(
    plots,
    ('foo', 'bar', 'baz'),  # labels
    loc='best',  # the best location avoiding obscuring lines
    framealpha=0.5,  # transparency.
    prop={'size': 'small', 'family': 'monospace'},  # font properties
)
plt.savefig('matplotlib-figures/example-05--legend.svg')
plt.close()

# title and axes labels
plots = plt.plot(x, y)
plt.title('Random trends')
plt.xlabel('Date')
plt.ylabel('Cum. sum')
# text
plt.figtext(
    x=0.995, y=0.01,  # proportional coordinates
    s='SOME TEXT',
    ha='right', va='bottom',  # horizontal (ha) and vertical (va) alignment
)
# grid
plt.grid(True)
# plt.tight_layout()  # All the plot elements are within the figure box
plt.gcf().set_tight_layout(True)  # All the plot elements are within the figure box
plt.savefig('matplotlib-figures/example-06--title--axes-labels--more.svg')
plt.close()

# # # object-oriented Matplotlib

fig = plt.figure(
    figsize=(8, 4),  # figure size in inches
    dpi=200,  # dots per inch
    # tight_layout=True,  # Fit axes, labels, etc. to canvas
    linewidth=1,  # 1 point wide,
    edgecolor='r',  # red border
)

ax1 = fig.add_axes((0.1, 0.1, 0.9, 0.9))  # (left in %, bottom in %, width in %, height in %)
ax1.set_title('Main Axes with Insert Child Axes')
ax1.plot(x, y[:, 0])
ax1.set_xlabel('Date')
ax1.set_ylabel('Cum. sum')

ax2 = fig.add_axes((0.5, 0.2, 0.4, 0.4))  # (left in %, bottom in %, width in %, height in %)
ax2.plot(x, y[:, 1], color='g')  # 'g' for green
ax2.set_xticks([])  # Remove the x ticks and labels from our embedded plot
# ax2.set_yticks([])
fig.savefig('matplotlib-figures/example-07--object-oriented.svg')
plt.close()

# subplots

# single axis
fig, ax = plt.subplots()
plots = ax.plot(x, y, label='')
fig.set_size_inches(8, 4)
ax.legend(
    plots,
    ('foo', 'bar', 'baz'),
    loc='best',
    framealpha=0.25,
    prop={'size': 'small', 'family': 'monospace'}
)
ax.set_title('Random trends')
ax.set_xlabel('Date')
ax.set_ylabel('Cum. sum')
ax.grid(True)
fig.text(0.995, 0.01, 'SOME TEXT', ha='right', va='bottom')
fig.tight_layout()
fig.savefig('matplotlib-figures/example-08--subplots-1.svg')
plt.close()

# three axes
fig, axes = plt.subplots(
    nrows=3, ncols=1,
    sharex=True, sharey=True,
    figsize=(8, 8),
)
labelled_data = zip(y.transpose(), ('foo', 'bar', 'baz'), ('b', 'g', 'r'))
fig.suptitle('Three Random Trends', fontsize=16)
for ind, ld in enumerate(labelled_data):
    ax = axes[ind]
    ax.plot(x, ld[0], label=ld[1], color=ld[2])
    ax.set_ylabel('Cum. sum')
    ax.legend(loc='upper left', framealpha=0.5, prop={'size': 'small'})
axes[-1].set_xlabel('Date')
fig.savefig('matplotlib-figures/example-09--subplots-2.svg')
plt.close()

# # # bar charts

labels = ["Physics", "Chemistry", "Literature", "Peace"]
foo_data = [3, 6, 10, 4]

bar_width = 0.5
xlocations = np.array(range(len(foo_data))) + bar_width
# array([0.5, 1.5, 2.5, 3.5])
plt.bar(xlocations, foo_data, width=bar_width)
plt.yticks(range(0, 12))
plt.xticks(xlocations, labels)
plt.title("Prizes won by Fooland")
plt.gca().get_xaxis().tick_bottom()
plt.gca().get_yaxis().tick_left()
plt.gcf().set_size_inches((8, 4))
plt.savefig('matplotlib-figures/example-10--bar-chart.svg')
plt.close()

bar_data = [8, 3, 6, 1]
fig, ax = plt.subplots(figsize=(8, 4))
bar_width = 0.4
xlocs = np.arange(len(foo_data))
ax.bar(xlocs - bar_width, foo_data, bar_width, color='#fde0bc', label='Fooland')
ax.bar(xlocs, bar_data, bar_width, color='peru', label='Barland')
ax.set_yticks(range(12))
ax.set_xticks(ticks=range(len(foo_data)))
ax.set_xticklabels(labels)
ax.yaxis.grid(True)
ax.legend(loc='best')
ax.set_ylabel('Number of prizes')
fig.suptitle('Prizes by country')
fig.tight_layout(pad=2)  # specify padding around the figure as a fraction of the font size
fig.savefig('matplotlib-figures/example-11--subplots-bar-charts.png', dpi=500)
plt.close()

bar_data = [8, 3, 6, 1]
fig, ax = plt.subplots(figsize=(8, 4))
bar_width = 0.4
ylocs = np.arange(len(foo_data))
ax.barh(ylocs - bar_width, foo_data, bar_width, color='#fde0bc', label='Fooland')
ax.barh(ylocs, bar_data, bar_width, color='peru', label='Barland')
ax.set_xticks(range(12))
ax.set_yticks(ticks=ylocs-bar_width/2)
ax.set_yticklabels(labels)
ax.xaxis.grid(True)
ax.legend(loc='best')
ax.set_xlabel('Number of prizes')
fig.savefig('matplotlib-figures/example-12--horizontal-bar-charts.svg')
plt.close()

fig, ax = plt.subplots(figsize=(8, 4))
bar_width = 0.8
xlocs = np.arange(len(foo_data))
ax.bar(xlocs, foo_data, bar_width, color='#fde0bc', label='Fooland')
ax.bar(xlocs, bar_data, bar_width, color='peru', label='Barland', bottom=foo_data)
ax.set_yticks(range(18))
ax.set_xticks(ticks=xlocs)
ax.set_xticklabels(labels)
ax.yaxis.grid(True)
ax.legend(loc='best')
ax.set_ylabel('Number of prizes')
fig.suptitle('Prizes by country')
fig.tight_layout(pad=2)  # specify padding around the figure as a fraction of the font size
fig.savefig('matplotlib-figures/example-13--stacked-bar-charts.svg',)
plt.close()

# # # scatter plots

num_points = 100
coef = 0.5
x = np.array(range(num_points))
y = np.random.randn(num_points) * 10 + x * coef
fig, ax = plt.subplots(figsize=(8, 4))
colors = np.random.rand(num_points)
size = np.pi * (2 + np.random.rand(num_points) * 8) ** 2
ax.scatter(x, y, s=size, c=colors, alpha=0.5)
fig.suptitle('Scatterplot with Color and Size Specified')
fig.savefig('matplotlib-figures/example-14--scatter.svg',)
plt.close()

# linear regression
num_points = 100
coef = 0.5
x = np.array(range(num_points))
y = np.random.randn(num_points) * 10 + x * coef
fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(x, y)
m, c = np.polyfit(x, y, deg=1)
ax.plot(x, m * x + c, c="r")
fig.suptitle('Scatterplot with Linear Regression')
fig.savefig('matplotlib-figures/example-15--scatter-with-linear-regression.svg',)
plt.close()
