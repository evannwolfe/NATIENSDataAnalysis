This application is designed to simplify and streamline the process of analyzing NATIENS training data by generating insightful box plots. The tool is useful for comparing lesion estimation error across different sites.

**Key Features:**
- **CSV Data Reading**: Loads data from CSV file, handling potential errors gracefully.
- **Error Calculation**: Calculates absolute error for 'detached' and 'attached' data categories.
- **Dynamic Plot Customization**: Generates box plots with customizable settings, controlled via a 'settings.json' file. This includes plot background colors, figure dimensions, color palettes, and more.
- **Group-Based Data Filtering**: Supports filtering and sorting data based on predefined groups.
- **User-Friendly Visualization**: Produces clear and informative visualizations, saving them as PNG files for easy access and distribution.

**Installation and Usage:**
1. Download the executable file (`GeneratePlots.exe`).
2. Place the executable in a directory with 'data.csv' and 'settings.json' files. 
3. Run the executable. The program will read the data, calculate errors, and generate plots based on the provided settings.
4. Check the output PNG file for your visualizations. It will output the PNG file in the same directory as the executable.

**Note:** This tool expects the CSV file to be named 'data.csv'. You can modify the settings by opening settings.json with a text editor. 

**Settings Guide**
1. plot_bg_color: Background color of the plot area.
2. fig_bg_color: Background color of the entire figure or canvas.
3. style: The overall aesthetic style of the plots, e.g., "whitegrid" for grid background.
4. fig_width, fig_height: Width and height of the figure in inches.
5. palette_vumc, palette_other: Color codes for the VUMC group and other groups in the plots.
6. plot_color: Color for the points plotted on the boxplot.
7. plot_point_size: Size of the points plotted on the boxplot.
8. detached_error_title, attached_error_title: Titles for the plots of detached and attached errors.
9. x_label: Label for the x-axis (common for both plots).
10. detached_y_label, attached_y_label: Labels for the y-axis for detached and attached error plots.
11. font_size_title: Font size for the plot titles.
12. font_color_title: Color for the plot titles.
13. font_size_axes: Font size for the axes' labels.
14. font_color_axes: Color for the axes' labels.
15. wrap_title: A boolean(true/false) to determine if the title should be wrapped. Use lowercase and no quotations.
16. detached_error_title_wrap_width, attached_error_title_wrap_width: Wrap width for the titles if wrap_title is true.
17. x_tick_font_size, y_tick_font_size: Font sizes for the ticks on the x-axis and y-axis.
18. output_format: Desired output format for the plot file, e.g., "pdf" or "png"
19. dpi: Dots per inch for the output image, affecting its resolution.
20. label_wrap_width: Width to wrap the labels on the x-axis. 
21. point_plot_type: Type of point plot, e.g., "beeswarm" or "stripplot".
22. stripplot_jitter: Boolean(true/false) which allows you to apply jitter in stripplot
23. median_label: Settings for displaying median values on the boxplot:
24. show_median: Whether to show median value labels on the plots.
25. color: Text color of the median labels.
26. foreground_color: Color of the median label outline for readability.
27. font_size: Font size of the median labels.
28. median_outline: Whether to draw an outline around the median label text.
29. Custom Labels: This section maps internal group identifiers to custom labels, allowing you to easily rename groups directly from the JSON file without altering your data.
30. groups: Specifies which groups to include in the plot. This allows for filtering the dataset before plotting.
31. customOrder: Defines the order in which the groups should appear on the x-axis of the plots. This is useful for sorting the groups in a specific sequence.
