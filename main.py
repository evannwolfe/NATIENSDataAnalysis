# These are import statements that import the necessary libraries for the script to run
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import textwrap
from matplotlib import patheffects as path_effects


# Settings.json and the data.csv files are expected to be in the same directory as the script
# This is the function that reads the csv file and returns the dataframe
def read_csv(file_path):
    try:
        # Read csv and return dataframe
        dataframe = pd.read_csv(file_path)

        # Specify the required columns, so that we can drop rows with missing values in those columns
        required_columns = ['redcap_data_access_group', 'total_detached', 'total_attached', 'total_detached_gt', 'total_attached_gt']

        # Drop rows where any of the required columns have missing values
        dataframe = dataframe.dropna(subset=required_columns)

        return dataframe
    except Exception as e:
        # Handle any errors that occur during reading of csv
        print("Error reading CSV file:", e)
        return pd.DataFrame()


# This is the function that reads the settings file and returns the settings
def read_settings(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# This is the function that calculates the error for detached, attached, and combined (total) errors and returns the updated dataframe
def calculate_error(dataframe):
    dataframe['detached_error'] = (dataframe['total_detached'].astype(float) - dataframe['total_detached_gt'].astype(float)).abs()
    dataframe['attached_error'] = (dataframe['total_attached'].astype(float) - dataframe['total_attached_gt'].astype(float)).abs()
    dataframe['total_error'] = dataframe['detached_error'] + dataframe['attached_error']

    # Calculate mean errors for each group
    composite_data = dataframe.groupby('redcap_data_access_group')[['detached_error', 'attached_error', 'total_error']].mean().reset_index()
    composite_data['redcap_data_access_group'] = 'Composite'

    # Append composite data to the DataFrame
    dataframe = pd.concat([dataframe, composite_data], ignore_index=True)
    return dataframe


# Function to calculate and overlay median value labels
def add_median_labels(ax, settings):
    show_median = settings.get("show_median", True)
    color = settings.get("color", "white")
    foreground_color = settings.get("foreground_color", "black")
    fontsize = settings.get("font_size", None)
    median_outline = settings.get("median_outline", False)

    if not show_median:
        return []

    lines = ax.get_lines()
    boxes = [c for c in ax.get_children() if type(c).__name__ == 'PathPatch']
    if not boxes:
        return []

    lines_per_box = int(len(lines) / len(boxes))
    median_list = []
    for median in lines[4:len(lines):lines_per_box]:
        x, y = (data.mean() for data in median.get_data())
        value = x if (median.get_xdata()[1] - median.get_xdata()[0]) == 0 else y
        text = ax.text(x, y, f'{value:.2f}', ha='center', va='center',
                       fontweight='bold', color=color, fontsize=fontsize)
        if median_outline:
            text.set_path_effects([
                path_effects.Stroke(linewidth=3, foreground=foreground_color),
                path_effects.Normal(),
            ])
        median_list.extend([value])
    return median_list


# This is the function that generates the box plots with the customized settings
def generate_plot(df, settings):
    # This returns the customization dictionary from the settings file
    customization_dict = settings.get('customization', {})
    # This returns the custom labels from the settings file
    custom_labels = settings.get('customLabels', {})
    # This returns the groups from the settings file
    selected_groups = settings.get('groups', [])
    # This returns the custom order from the settings file
    custom_order = settings.get('customOrder', [])
    # This returns the wrap_title from the settings file
    wrap_title = customization_dict.get('wrap_title', False)
    # This returns the x_tick_font_size and y_tick_font_size from the settings file
    x_tick_font_size = customization_dict.get('x_tick_font_size', 10)
    y_tick_font_size = customization_dict.get('y_tick_font_size', 10)
    # This returns the designated output from the settings file
    output_format = customization_dict.get('output_format', 'png')
    # This returns the settings for the median value labels
    median_label_settings = customization_dict.get('median_label', {})
    # This returns the errors to display from the settings file
    show_errors = customization_dict.get('show_errors', ['detached_error'])

    # Copy the DataFrame so we don't modify the original
    df = df.copy()

    # Apply the filtering on the dataframe
    if selected_groups:
        df = df[df['redcap_data_access_group'].isin(selected_groups)]

    # Apply custom sorting on the dataframe
    if custom_order:
        order_mapping = {name: index for index, name in enumerate(custom_order)}
        df['custom_sort'] = df['redcap_data_access_group'].map(order_mapping)
        df = df.sort_values('custom_sort').drop('custom_sort', axis=1)
    # This sets the background color of the plot. Default is whitesmoke #f5f5f5
    plot_bg_color = customization_dict.get('plot_bg_color', '#f5f5f5')
    # This sets the background color of the figure (everything outside the plot). Default is white
    fig_bg_color = customization_dict.get('fig_bg_color', '#ffffff')
    # This sets the style of the plot. Default is whitegrid. You can set it to whitegrid, darkgrid, white, and dark
    style = customization_dict.get('style', 'whitegrid')
    # This is the figure width. Default is 15
    fig_width = float(customization_dict.get('fig_width', 15))
    # This is the figure height. Default is 6
    fig_height = float(customization_dict.get('fig_height', 6))
    # This retrieves the label wrap width from the settings, defaulting to 10
    label_wrap_width = customization_dict.get('label_wrap_width', 10)
    # Use the DPI setting from the settings file, default to 300
    dpi = customization_dict.get('dpi', 300)
    # Determine which point plot type to use based on settings
    point_plot_type = customization_dict.get('point_plot_type', 'beeswarm')  # Default to beeswarm if not specified

    # Filter errors to display based on the settings
    error_types = [error for error in ['detached_error', 'attached_error', 'total_error'] if error in show_errors]

    # This is the function that sets the style based on what was designated in the settings file
    with sns.axes_style(style):
        fig, axes = plt.subplots(1, len(error_types), figsize=(fig_width, fig_height))
        fig.set_facecolor(fig_bg_color)

        if len(error_types) == 1:
            axes = [axes]

        # This is the function that sets the background color of the plot based on what was designated in the settings file and
        for i, ax in enumerate(axes):
            ax.set_facecolor(plot_bg_color)
            new_labels = []
            for label in df['redcap_data_access_group'].unique():
                custom_label = custom_labels.get(label, label)
                # Wrap each label to a max width, for example, 20 characters
                wrapped_label = "\n".join(textwrap.wrap(custom_label, width=label_wrap_width))
                new_labels.append(f"{wrapped_label} ({df[df['redcap_data_access_group'] == label].shape[0]})")

            ax.set_xticks(range(len(new_labels)))
            ax.set_xticklabels(new_labels)
            # Set x-tick and y-tick font sizes
            ax.tick_params(axis='x', labelsize=x_tick_font_size)
            ax.tick_params(axis='y', labelsize=y_tick_font_size)

        # This sets the colors for the boxes for VUMC(the baseline) and for the other sites. Default is #866D4B for VUMC and
        # #5975a4 for the other sites
        palette = {
            group: customization_dict.get('palette_vumc', '#866D4B') if group == 'vumc' else customization_dict.get('palette_other', '#5975a4')
            for group in df['redcap_data_access_group'].unique()
        }
        # Here we are setting the color, size and jitter for the points plotted on the box plot. Default is black,
        # size of 3, and jitter set to true
        plot_color = customization_dict.get('plot_color', 'black')
        plot_size = float(customization_dict.get('plot_point_size', 3))
        stripplot_jitter = customization_dict.get('stripplot_jitter', True)
        # This sets the title, x-axis label, and y-axis labels
        y_labels = {
            'detached_error': customization_dict.get('detached_y_label', 'Detached Error (%)'),
            'attached_error': customization_dict.get('attached_y_label', 'Attached Error (%)'),
            'total_error': customization_dict.get('total_y_label', 'Total Error (%)')
        }
        for i, ax in enumerate(axes):
            error_type = error_types[i]
            title = customization_dict.get(f'{error_type}_title', f'{error_type.title().replace("_", " ").capitalize()} by Site')

            # Check if wrap_title is True before applying word wrapping
            if wrap_title:
                wrap_width = customization_dict.get(f'{error_type}_title_wrap_width', 10)  # Use default wrap width if not specified
                title = "\n".join(textwrap.wrap(title, width=wrap_width))
            # We use a space as the default x-axis label so that the x-axis label is not displayed unless specified
            x_label = customization_dict.get('x_label', ' ')
            # Font size and color for the title, x-axis label, and y-axis label
            # X and Y axis share font size and color parameters while Title are separate
            font_size_title = int(customization_dict.get('font_size_title', 12))
            font_color_title = customization_dict.get('font_color_title', '#000000')
            font_size_axes = int(customization_dict.get('font_size_axes', 12))
            font_color_axes = customization_dict.get('font_color_axes', '#000000')
            # This sets the title, x-axis label, and y-axis labels with their respective font size and color
            ax.set_title(title, fontsize=font_size_title, color=font_color_title)
            if x_label:
                ax.set_xlabel(x_label, fontsize=font_size_axes, color=font_color_axes)
            ax.set_ylabel(y_labels[error_type], fontsize=font_size_axes, color=font_color_axes)

            sns.boxplot(ax=ax, x='redcap_data_access_group', y=error_type, data=df,
                        hue='redcap_data_access_group', palette=palette, dodge=False, legend=False, showfliers=False)
            # Plot points according to the specified type
            if point_plot_type == 'beeswarm':
                sns.swarmplot(ax=ax, x='redcap_data_access_group', y=error_type, data=df,
                              color=plot_color, size=plot_size)
            elif point_plot_type == 'stripplot':
                sns.stripplot(ax=ax, x='redcap_data_access_group', y=error_type, data=df,
                              color=plot_color, size=plot_size, jitter=stripplot_jitter)

            add_median_labels(ax, median_label_settings)

        # Tight layout is used to adjust the padding between and around subplots. Other options are available
        # such as: pad, w_pad, h_pad, rect and more
        plt.tight_layout()

        # This saves the plot as a png file in the same directory as the script
        plt.savefig(f'output_plot.{output_format}')
        if output_format == 'png':
            plt.savefig(f'output_plot.{output_format}', dpi=dpi)


# Main execution
dataframe = read_csv('data.csv')
# This checks to see if the dataframe is empty and if it is not empty then it will run the calculations and make plots
if not dataframe.empty:
    dataframe = calculate_error(dataframe)
    settings = read_settings('settings.json')
    generate_plot(dataframe, settings)
else:
    print("Dataframe is empty. Please check the CSV file.")
