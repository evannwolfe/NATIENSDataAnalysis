This release is designed to simplify and streamline the process of analyzing NATIENS training data by generating insightful box plots. The tool is useful for comparing lesion estimation error across different sites.

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
