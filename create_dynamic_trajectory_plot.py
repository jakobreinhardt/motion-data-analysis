import panel as pn
import holoviews as hv
hv.extension('bokeh')

def dynamic_trajectory_plot(
    data,
    names_of_columns_x_and_y_tuple,
    labels=None,
    colors=None,
    start=0,
    end=None,
    step=1,
    width=800,
    height=600,
    title="Dynamic Trajectory Plot"
):
    """
    Create a dynamic 2D trajectory plot with a slider using Panel and Holoviews.

    Parameters:
        data: pandas DataFrame containing the data
        names_of_columns_x_and_y_tuple: list of (x_col, y_col) tuples (column names)
        labels: list of str, legend labels for each trajectory (optional)
        colors: list of str, colors for each trajectory (optional)
        start: int, start frame index
        end: int, end frame index (default: length of first x column)
        step: int, slider step size
        width: int, plot width
        height: int, plot height
        title: str, plot title
    """
    n = len(names_of_columns_x_and_y_tuple)
    if labels is None:
        labels = [f"Trajectory {i+1}" for i in range(n)]
    if colors is None:
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray'][:n]
    if end is None:
        end = len(data[names_of_columns_x_and_y_tuple[0][0]]) - 1

    def plot_frame(i):
        fig = None
        for (x_col, y_col), label, color in zip(names_of_columns_x_and_y_tuple, labels, colors):
            curve = hv.Curve((data[x_col][:i], data[y_col][:i]), label=label).opts(color=color)
            point = hv.Points((data[x_col][i], data[y_col][i])).opts(color='black', size=10)
            if fig is None:
                fig = curve * point
            else:
                fig *= curve * point
        return fig.opts(
            title=f"{title} - Frame {i}",
            xlabel='X Position',
            ylabel='Y Position',
            width=width,
            height=height,
            legend_position='right'
        )

    slider = pn.widgets.IntSlider(name='Frame', start=start, end=end, step=step, value=start)
    return pn.interact(plot_frame, i=slider)

# Example usage:
# dynamic_trajectory_plot(
#     data=vicon_positions_from_csv,
#     names_of_columns_x_and_y_tuple=[
#         ('Surgeon:C7_X', 'Surgeon:C7_Y'),
#         ('Instrumenter:OM_X', 'Instrumenter:OM_Y'),
#         ('DLR_Robot:HTop_X', 'DLR_Robot:HTop_Y')
#     ],
#     labels=['Surgeon C7', 'Instrumenter OM', 'DLR Robot HTop'],
#     colors=['blue', 'red', 'green'],
#     start=0,
#     end=50000,
#     step=50,
#     width=800,
#     height=600,
#     title="Dynamic Trajectory Plot Example"
# )
