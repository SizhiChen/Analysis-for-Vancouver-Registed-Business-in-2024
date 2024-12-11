"""
Strong/Sizhi Chen
CS 5001, Fall 2024
Final Project -- plot.py

This script provides a collection of utility functions for data visualization using Matplotlib and Seaborn.
The functions are designed to generate commonly used visualizations such as bar plots, scatter plots, and heatmaps,
with additional customization options for themes and color schemes.

Key Features:
1. **Bar Plot**:
   - Creates a horizontal bar plot for the top `n` entries based on aggregated values of a specified column.
   - Includes customizable themes and bar colors.

2. **Scatter Plot**:
   - Visualizes the relationship between two variables using a scatter plot.
   - Optionally includes a linear regression line for trend analysis.

3. **Heatmaps**:
   - Generates a correlation heatmap to show relationships between dataset features.
   - Includes options for a full-feature heatmap or a single-column correlation heatmap.

Customization Options:
- Users can specify background colors and colormaps for plots to match themes or improve visualization aesthetics.

Functions:
- `bar_plot(x_axis, y_axis, top_n, data, theme_color, bar_color)`: Creates a horizontal bar plot.
- `scatter_plot(x_axis, y_axis, data, theme_color, bar_color)`: Creates a scatter plot with an optional regression line.
- `heatmap(data, background_color, cell_color)`: Generates a correlation heatmap for all features.
- `single_column_heatmap(data, column, background_color, cell_color)`: Creates a heatmap showing correlations with a single column.

This script is useful for quick exploratory data analysis (EDA) and creating polished visualizations for reports or presentations.
"""


# Import modules
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.colors import is_color_like
import numpy as np
import seaborn as sns
import pandas as pd


# Validate input function
def validate_dataframe_column(data, column, func_name):
    """Validates that the specified column exists in the DataFrame."""
    if column not in data.columns:
        raise ValueError(f"[{func_name}] Error: Column '{column}' not found in the dataset.")


def validate_positive_integer(value, name, func_name):
    """Validates that a given value is a positive integer."""
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"[{func_name}] Error: {name} must be a positive integer.")


def validate_color_cmap(color, func_name):
    """Validates the color input by trying to convert it using Matplotlib."""
    try:
        colormaps.get_cmap(color)
    except ValueError:
        raise ValueError(f"[{func_name}] Error: '{color}' is not a valid Matplotlib colormap name.")


def validate_color_normal(color, param_name, func_name):
    """Validates that the given color is a valid Matplotlib color."""
    if not is_color_like(color):
        raise ValueError(f"[{func_name}] Error: '{color}' is not a valid color for '{param_name}'.")


# Plotting
def bar_plot(x_axis, y_axis, top_n, data, theme_color, bar_color):
    """
    Creates a horizontal bar plot showing the top `n` entries of a dataset based on the sum of values for a specified column, with a customizable theme and bar colors.

    Parameters:
        x_axis (str): The column name for the x-axis (categories).
        y_axis (str): The column name for the y-axis (values to aggregate and display).
        top_n (int): The number of top entries to include in the plot.
        data (DataFrame): The dataset containing the data for the plot.
        theme_color (str): Background color for the plot (e.g., "white", "#f0f0f0").
        bar_color (str): Matplotlib colormap name for bar colors (e.g., "viridis", "plasma").
    Returns:
        matplotlib.figure.Figure: The generated bar plot as a Matplotlib figure object.
    """
    # Validating inputs
    if not isinstance(data, pd.DataFrame):
        raise ValueError("[bar_plot] Error: bar_plot.data must be a pandas DataFrame.")
    validate_dataframe_column(data, x_axis, "bar_plot")
    validate_dataframe_column(data, y_axis, "bar_plot")
    validate_positive_integer(top_n, "top_n", "bar_plot")
    validate_color_cmap(bar_color, "bar_plot")
    validate_color_normal(theme_color, "theme_color", "bar_plot")

    # Selecting top_n entries and reversing the order
    top_data = data.groupby(x_axis)[y_axis].sum().sort_values(ascending=False).head(top_n)[::-1]

    # Create a colormap
    cmap = colormaps.get_cmap(bar_color).resampled(top_n)  # Create a colormap with `top_n` discrete colors
    colors = [cmap(i) for i in range(top_n)]  # Generate color for each bar

    # Set the font size
    font_size = 10

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(6.5, 4), facecolor=theme_color)
    bars = ax.barh(top_data.index, top_data.values, color=colors)
    ax.set_title(f"Top {top_n} {x_axis} by {y_axis}", fontsize=12)
    ax.set_xlabel(y_axis)
    ax.set_ylabel(x_axis)
    ax.tick_params(axis='both', labelsize=font_size)
    plt.tight_layout()

    # Add text labels on the bars with opposite color
    for bar, color, value in zip(bars, colors, top_data.values):
        # Choose text color: white for dark bars, black for light bars
        r, g, b, _ = color
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = 'white' if luminance < 0.5 else 'black'

        # Get the text width (approximation using value length)
        text_str = f'{value:,.0f}'
        text_width = (len(text_str)+6) * font_size * 0.6 * fig.dpi / 72
        bar_width = (value / ax.get_xlim()[1]) * fig.get_size_inches()[0] * fig.dpi

        # Determine placement: inside if text fits, outside otherwise
        if text_width< bar_width:
            text_x = bar.get_width() - (0.01 * max(top_data.values))  # Slightly inside the bar
            ha = 'right'  # Align text to the right
        else:
            text_x = bar.get_width() + (0.01 * max(top_data.values))  # Slightly outside the bar
            ha = 'left'  # Align text to the left
            text_color = 'black' # if Outside the bar, always black

        # Add the text
        ax.text(
            text_x,  # Position inside the bar
            bar.get_y() + bar.get_height() / 2,  # Centered vertically
            text_str,  # Formatted value
            va='center',
            ha=ha,
            color=text_color,  # Opposite text color
            fontsize=font_size,
        )
    return fig


def scatter_plot(x_axis, y_axis, data, theme_color, bar_color):
    """
    Creates a scatter plot visualizing the relationship between two variables with an optional linear regression line.

    Parameters:
        x_axis (str): The column name for the x-axis variable.
        y_axis (str): The column name for the y-axis variable.
        data (DataFrame): The dataset containing the data for the plot.
        theme_color (str): Background color for the plot (e.g., "white", "#f0f0f0").
        bar_color (str): Color for the scatter plot points.
    Returns:
        matplotlib.figure.Figure: The generated scatter plot as a Matplotlib figure object.
    """
    # Validating inputs
    if not isinstance(data, pd.DataFrame):
        raise ValueError("[scatter_plot] Error: scatter_plot.data must be a pandas DataFrame.")
    validate_dataframe_column(data, x_axis, "scatter_plot")
    validate_dataframe_column(data, y_axis, "scatter_plot")
    validate_color_normal(theme_color, "theme_color", "scatter_plot")
    validate_color_normal(bar_color, "bar_color", "scatter_plot")

    # Create a new figure
    fig, ax = plt.subplots(figsize=(6.5, 4), facecolor=theme_color)

    # Get x-axis and y-axis data for the graph
    x = data[x_axis]
    y = data[y_axis]

    # Create the scatter plot
    ax.scatter(x, y, label='Data points', color=bar_color)

    # Get the Linear Regression
    slope, intercept = np.polyfit(x, y, 1)
    regression_line = slope * x + intercept
    ax.plot(x, regression_line, color='#6C2666',
            label=f'Regression line: {slope:.2f}x + {intercept:.2f}')

    # Add labels, title, and legend
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f'Relationship between {x_axis} and {y_axis}')
    ax.legend()

    # Adjust the spacing to minimize white space
    plt.tight_layout(pad=1)
    return fig


def heatmap(data, background_color, cell_color):
    """
    Generates a heatmap displaying the absolute correlation between features in a dataset.

    Parameters:
        data (DataFrame): The dataset whose correlations are to be visualized.
        background_color (str): Background color of the figure (e.g., "white", "#f0f0f0").
        cell_color (str): Colormap for the heatmap cells (e.g. "viridis").
    Returns:
        matplotlib.figure.Figure: The generated heatmap as a Matplotlib figure object.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("[heatmap] Error: heatmap.data must be a pandas DataFrame.")
    validate_color_cmap(cell_color, "heatmap")
    validate_color_normal(background_color, "background_color", "heatmap")

    # Create the heatmap
    fig, ax = plt.subplots(figsize=(4, 2.5), facecolor=background_color)
    sns.heatmap(data.corr().abs(), vmin=0, vmax=1, annot=True, cmap=cell_color, ax=ax,
                fmt=".2f")

    # Set x and y labels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

    # Add title
    ax.set_title('Correlation Heatmap', fontdict={'fontsize': 10}, pad=5)

    # Adjust heatmap
    plt.tight_layout()
    return fig


def single_column_heatmap(data, column, background_color, cell_color):
    """
    Generates a heatmap showing the absolute correlation between a specific column and all other columns in a dataset.

    Parameters:
        data (DataFrame): The dataset whose correlations are to be visualized.
        column (str): The column name for which correlations with other columns are computed.
        background_color (str): Background color of the figure (e.g., "white", "#f0f0f0").
        cell_color (str): Colormap for the heatmap cells (e.g. "viridis").
    Returns:
        matplotlib.figure.Figure: The generated heatmap as a Matplotlib figure object.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("[single_column_heatmap] Error: single_column_heatmap.data must be a pandas DataFrame.")
    validate_dataframe_column(data, column, "single_column_heatmap")
    validate_color_cmap(cell_color, "single_column_heatmap")
    validate_color_normal(background_color, "background_color", "single_column_heatmap")

    # Keep it in 2D
    corr_column = data.corr().abs()[[column]].sort_values(by=column, ascending=False)

    # Create the single column heatmap
    fig, ax = plt.subplots(figsize=(2.5, 2.5), facecolor=background_color)
    sns.heatmap(corr_column, vmin=0, vmax=1, annot=True,
                cmap=cell_color, ax=ax, fmt=".2f")

    # Set x and y labels
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)

    # Add title
    ax.set_title(f'Correlation with {column}', fontdict={'fontsize': 10}, pad=10)

    # Adjust heatmap
    plt.tight_layout()
    return fig
