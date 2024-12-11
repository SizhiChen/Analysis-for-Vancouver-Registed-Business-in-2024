# README: Business and Inventory Analysis Project

## Overview

This project provides a comprehensive solution for analyzing business and inventory data for the City of Vancouver. By integrating data cleaning, analysis, and visualization functionalities, the project empowers users to explore business trends and relationships through an intuitive GUI interface.

## Key Features

1. **Data Cleaning and Preprocessing:**
   - Cleans raw business license and inventory data to ensure consistency and accuracy.
   - Standardizes business and inventory names for reliable cross-referencing.

2. **Object-Oriented Representation:**
   - Implements `Business` and `Inventory` classes for structured data representation.
   - Each class provides methods for managing, summarizing, and comparing data.

3. **Data Visualization:**
   - Generates bar plots, scatter plots, and heatmaps for insightful analysis.
   - Customizable themes enhance the visualization aesthetics.
![image](https://github.com/user-attachments/assets/2664577a-b053-4046-93c2-01a20ace1ffc)
![image](https://github.com/user-attachments/assets/c8d3d56a-4ba2-4482-8fc1-e801e35d7f3e)
![image](https://github.com/user-attachments/assets/78cf9b44-23e1-40c1-915e-9156c29fb5e3)
![image](https://github.com/user-attachments/assets/32f556ba-4ec0-491b-ab1c-ae087dbcd46a)

4. **Interactive GUI:**
   - A Tkinter-based application for exploring business and inventory data.
   - Provides user-friendly widgets for selecting data, customizing plots, and saving visualizations.

5. **Modular Design:**
   - Separates data cleaning, class definitions, and GUI logic into modular components.
   - Ensures maintainability and scalability.

## File Descriptions

### Python Scripts

1. **`data_clean.py`**
   - Processes raw business and inventory data.
   - Handles tasks like duplicate removal, outlier elimination, and standardization of names.

2. **`business.py`**
   - Defines the `Business` class to manage business attributes, including type, address, employees, and registration fees.
   - Provides methods for aggregating and summarizing business data.

3. **`inventory.py`**
   - Defines the `Inventory` class to manage inventory attributes, including location and category.
   - Offers methods for summarizing inventory data.

4. **`plot.py`**
   - Contains utility functions for creating visualizations (bar plots, scatter plots, and heatmaps).
   - Uses Matplotlib and Seaborn for high-quality plots.

5. **`app.py`**
   - Implements the GUI using Tkinter.
   - Integrates visualization functions for interactive data exploration.

6. **`data_dashboard.py`**
   - Acts as the driver script, initializing the application and data objects.
   - Combines cleaned data and launches the GUI.

### Data Files

- **`business_cleaned.csv`**: Cleaned dataset containing business information.
- **`inventory_cleaned.csv`**: Cleaned dataset containing inventory information.

### Additional Resources

- **`CityOfVancouverLogo.png`**: Logo used in the GUI header.

## Usage

1. Ensure all required Python packages are installed:
   ```bash
   pip install pandas matplotlib seaborn
   ```

2. Run the driver script to launch the application:
   ```bash
   python data_dashboard.py
   ```

3. Use the GUI to:
   - Explore data summaries.
   - Visualize relationships between business metrics.
   - Customize themes and save plots for reporting.

## Project Achievements

This project successfully achieves the following:

1. **Streamlined Data Analysis:**
   - Cleans and preprocesses data for error-free analysis.
   - Provides object-oriented structures for managing business and inventory data.

2. **User-Friendly Interaction:**
   - Offers an intuitive GUI for non-technical users.
   - Enables easy customization and visualization of complex datasets.

3. **Advanced Visualizations:**
   - Delivers high-quality plots to uncover insights and trends.
   - Supports customizable themes to cater to diverse presentation needs.

## Future Enhancements

- Integrate additional datasets for a more comprehensive analysis.
- Implement machine learning models for predictive analysis.
- Enhance GUI usability with more advanced interactive features.

## Author

**Strong/Sizhi Chen**

