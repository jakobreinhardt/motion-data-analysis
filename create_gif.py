import matplotlib.pyplot as plt
import imageio
import os

def create_animated_trajectory_gif(
    xys,
    labels,
    colors,
    start=0,
    end=50000,
    step=50,
    figsize=(8, 6),
    gif_name='animated_plot.gif',
    duration=0.1,
    cleanup=True
):
    """
    Create an animated GIF of 2D trajectories with current position markers.

    Parameters:
        xys: list of (x, y) tuples, each containing arrays/lists of x and y positions
        labels: list of str, legend labels for each trajectory
        colors: list of str, line colors for each trajectory
        start: int, start frame index
        end: int, end frame index (exclusive)
        step: int, frame step size
        figsize: tuple, figure size
        gif_name: str, output GIF filename
        duration: float, duration per frame in seconds
        cleanup: bool, whether to delete PNG frames after GIF creation
    """
    filenames = []
    for i in range(start + step, end, step):
        fig, ax = plt.subplots(figsize=figsize)
        # Plot trajectories
        for (x, y), label, color in zip(xys, labels, colors):
            ax.plot(x[start:i], y[start:i], color+'-', label=label)
        # Plot current position markers
        for (x, y) in xys:
            ax.plot(x[i], y[i], 'ko', markersize=8)
        ax.legend()
        ax.set_title(f'Frame {i}')
        ax.grid(True)
        filename = f"frame_{i}.png"
        plt.savefig(filename)
        filenames.append(filename)
        plt.close()
    # Create GIF
    with imageio.get_writer(gif_name, mode='I', duration=duration) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    # Cleanup
    if cleanup:
        for filename in filenames:
            os.remove(filename)

# Example usage:
# create_animated_trajectory_gif(
#     xys=[
#         (vicon_positions_from_csv['Surgeon:C7_X'], vicon_positions_from_csv['Surgeon:C7_Y']),
#         (vicon_positions_from_csv['Instrumenter:OM_X'], vicon_positions_from_csv['Instrumenter:OM_Y']),
#         (vicon_positions_from_csv['DLR_Robot:HTop_X'], vicon_positions_from_csv['DLR_Robot:HTop_Y'])
#     ],
#     labels=['Vicon C7 X', 'Vicon OM X', 'DLR Robot HTop X'],
#     colors=['b', 'r', 'g'],
#     start=0,
#     end=50000,
#     step=50,
#     gif_name='animated_plot.gif',
#     duration=0.1
# )