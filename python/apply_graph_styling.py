import matplotlib.pyplot as plt

def apply_graph_styling(ax=None,
                        text_color="#221F20",
                        grid_color="#C5C5C4",
                        grid_on_x=False,
                        grid_on_y=False,
                        data_colors=None,
                        column_color_map=None,
                        single_data_color=None):
    """
    Applies a consistent styling to a Matplotlib Axes, in a way that 
    is usable for different plot types (line, bar, scatter, etc.).

    Parameters:
      ax (matplotlib.axes.Axes): The axis to style. If None, uses plt.gca().
      text_color (str): HEX color for text elements (ticks, labels, title, legend).
      grid_color (str): HEX color for grid lines.
      grid_on_x (bool): Whether to show grid lines (x axis).
      grid_on_y (bool): Whether to show grid lines (y axis).
      data_colors (list): If provided, sets the color cycle for *future* plots 
                          (lines, bars, etc.) in the given order.
      column_color_map (dict): A mapping from column/legend label -> HEX color.
                               If provided, recolors existing bar containers 
                               (e.g., grouped bar charts) based on their label.
      single_data_color (str): A HEX color to apply uniformly to all data elements
                               (bars, lines, etc.). Overrides column_color_map 
                               and data_colors if provided.
                               Example: "#CF4C48" for all bars in a bar chart.
    """
    if ax is None:
        ax = plt.gca()

    # 1) Set a color cycle for future plots, if specified
    if data_colors is not None:
        ax.set_prop_cycle(color=data_colors)

    # 2) Style the spines, tick labels, axis labels, title
    for spine in ax.spines.values():
        spine.set_color(text_color)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    ax.title.set_color(text_color)

    # 3a) Optionally enable grid with the specified color
    if grid_on_x:
        ax.grid(True, axis='x', color=grid_color)
    else:
        ax.grid(False, axis='x')

    # 3b) Optionally enable grid with the specified color
    if grid_on_y:
        ax.grid(True, axis='y', linestyle='--', alpha=0.7, zorder = 10, color=grid_color)
    else:
        ax.grid(False, axis='y')

    # 4) Legend text color
    legend = ax.get_legend()
    if legend is not None:
        for txt in legend.get_texts():
            txt.set_color(text_color)

    # 5) Apply single data color if specified
    if single_data_color:
        for container in ax.containers:
            for bar in container:
                bar.set_facecolor(single_data_color)
        
        # Update legend with single color
        if legend is not None:
            for handle in legend.legend_handles:
                handle.set_facecolor(single_data_color)
                handle.set_edgecolor(single_data_color)

    # 6) If we have a column->color mapping and no single_data_color, recolor any bar containers
    if column_color_map and not single_data_color:
        for container in ax.containers:
            label = container.get_label()
            if label in column_color_map:
                color = column_color_map[label]
                for bar in container:
                    bar.set_facecolor(color)
        
        # Update legend colors to match container colors
        if legend is not None:
            for handle, text in zip(legend.legend_handles, legend.get_texts()):
                label = text.get_text()
                if label in column_color_map:
                    color = column_color_map[label]
                    handle.set_facecolor(color)
                    handle.set_edgecolor(color)
