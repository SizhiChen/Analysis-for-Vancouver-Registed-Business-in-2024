"""
Strong/Sizhi Chen
CS 5001, Fall 2024
Final Project -- data_clean.py

This script is designed to process and clean business license and storefront
inventory data from the City of Vancouver's open data portal.

It performs the following tasks:

1. Downloads business license and storefront inventory data in CSV format from specified URLs.
2. Cleans and filters the business license dataset to retain relevant information for businesses in British Columbia with valid licenses.
3. Cleans and filters the storefront inventory dataset to remove vacant or under-construction entries.
4. Maps inconsistent business names to standardized names for consistency across datasets.
5. Combines relevant address fields into a single "Address" column for easier processing.
6. Removes duplicates and outliers based on employee counts and other specified conditions.
7. Saves the cleaned and processed data into new CSV files.

The script includes a range of utility functions for handling data manipulations, such as filtering, column combination, and value standardization.
"""


# Import module
import requests
import pandas as pd
import numpy as np


# Set constants
BUSINESS_YEAR_ANALYSIS = 24
INVENTORY_YEAR_ANALYSIS = 2023
MIN_EMPLOYEES = 1
LOWER_THRESHOLD = 0.1
UPPER_THRESHOLD = 99.9
TRADE_NAME_MAPPINGS = [
    ('Subway', 'Subway'), ('Starbucks', 'Starbucks'), ('Tim Horton', 'Tim Hortons'),
    ('TD Canada Trust', 'TD Canada Trust'), ('Shoppers', 'Shoppers Drug Mart'),
    ('McDonald\'s', 'McDonald\'s'), ('McDonalds', 'McDonald\'s'), ('UPS Store', 'The UPS Store'),
    ('Blenz', 'Blenz'), ('Vancity', 'Vancity'), ('Pharmasave', 'Pharmasave'),
    ('A&W', 'A&W Restaurant'), ('Freshslice', 'Freshslice Pizza'), ('London Drugs', 'London Drugs'),
    ('Money Mart', 'Money Mart'), ('Panago', 'Panago'), ('JJ Bean', 'JJ Bean'),
    ('Domino', 'Domino\'s Pizza'), ('Dairy Queen', 'Dairy Queen'), ('Chevron', 'Chevron'),
    ('Safeway', 'Safeway'), ('LifeLabs', 'Life Labs'), ('Telus', 'Telus'), ('Freshii', 'Freshii'),
    ('Donair Dude', 'Donair Dude'), ('Caffe Artigiano', 'Caffe Artigiano'),
    ('Petro Canada', 'Petro Canada'), ('Fido', 'Fido'), ('Pizza Hut', 'Pizza Hut'),
    ('Circle K', 'Circle K'), ('Trees Organic', 'Trees Organic Coffee'),  ('Shell', 'Shell'),
    ('Freedom Mobile', 'Freedom Mobile'), ('Cobs Bread', 'Cobs Bread'),  ('Gong Cha', 'Gong Cha'),
    ('Home Hardware', 'Home Hardware'), ('Dollarama', 'Dollarama'), ('Pizza Pizza', 'Pizza Pizza'),
    ('Save-On-Foods', 'Save-On-Foods'), ('Purdys Chocolatier', 'Purdys Chocolatier'),
    ('Pure Integrative Pharmacy', 'Pure Integrative Pharmacy'), ('Dutch Love Cannabis', 'Dutch Love Cannabis'),
    ('The Co-operators', 'The Co-operators'), ('Uncle Fatih\'s', 'Uncle Fatih\'s Pizza'),
    ('Obanhmi', 'Obanh mi'), ('Nook', 'Nook'), ('ShareTea', 'Share Tea'), ('Specsavers', 'Specsavers'),
    ('Bosley\'s', 'Bosley\'s'), ('Banana Leaf', 'Banana Leaf'), ('Orangetheory Fitness', 'Orangetheory Fitness'),
    ('Big Feet', 'Big Feet'), ('Inspired Cannabis', 'Inspired Cannabis'), ('Pure Nail Bar', 'Pure Nail Bar'),
    ('Benjamin Moore', 'Benjamin Moore'), ('Liberty Tax Service', 'Liberty Tax Service'),
    ('Bean Around the World', 'Bean Around the World'), ('IGA #', 'IGA'), ('City Cannabis Co', 'City Cannabis Co.'),
    ('Kentucky Fried Chicken', 'KFC')]
BUSINESS_NAME_MAPPING = [
    ('H & R Block', 'H&R Block'),
    ('Breka Bakery & Cafe', 'Breka Bakery & Café'),
    ('Sleep Country', 'Sleep Country'),
    ('Dollar Tree', 'Dollar Tree'),
    ('Buntain Insurance', 'Buntain Insurance'),
    ('Exposure', 'Exposure'),
    ('Edward D', 'Edward Jones Investments'),
    ('Matchstick Coffee', 'Matchstick Coffee'),
    ('Ollie Quinn', 'Ollie Quinn'),
    ('Easy Financial', 'Easy Financial'),
    ('BCAA', 'BCAA'),
    ('The Bloom Group', 'The Bloom Group'),
    ('FW Fitness', 'Fitness World'),]
DIRECT_NAMES = [
    'Royal Bank of Canada','Bank of Nova Scotia', 'HSBC',
    'Oxygen Yoga and Fitness', 'Chicko Chicken', 'Body Energy Club', 'Turnabout',
    'F45 Training', 'Waves Coffee House', 'Tacofino', 'Expedia Cruises',
    'Kin\'s Farm Market', 'Kumon', 'White Spot', 'Myodetox', 'AARM Dental Group',
    'Yummy Slice Pizza', 'No Frills', 'Choices Markets', 'urban fare', 'Vancity',
    'Earl\'s', 'Earls', 'T & T Supermarket', 'InsureBC', 'Thai Basil', 'Jenjudan',
    'Lagree West', 'Pine House Bakery', 'Legendary Noodle', 'Care Point Medical & Wellness',
    'Aroom Cafe', 'Westland Insurance', 'Genesis Nutrition', 'Winners', 'Rexall'
    'Your Dollar Store With More', 'Pet Pantry', 'Nuba', 'Beyond Nourished',
    'Artemisia Clothing', 'KFC', 'Maruhachi Ra-men', '49th Parallel Coffee Roasters',
    'Chatime', 'Tisol', 'CoCo Fresh Tea & Juice', 'Nesters Market', 'Fighter Chicken',
    'Papa John\'s Pizza', 'Denny\'s', 'Burger King', 'Fatburger', 'Straight Outta Brooklyn',
    'Tokyo Beauty', 'The Latest Scoop', 'Highroads Medical Clinic', 'FYI Doctor',
    'La Canapa', 'Good Co', 'Minuteman Press', 'Persia Foods', 'Rib & Chicken',
    'Pulpfiction Books', 'De Dutch Pannekoek', 'Suki\'s', 'Urban Fare', 'Burgoo',
    'Pallet Coffee Roasters', 'Muse Cannabis', 'Aesop', 'Lions MMA', 'Whole Foods Market',
    'The Basic', 'Sherwin-Williams', 'Glory Juice Co', 'Honolulu Coffee', 'Vera\'s Burger Shack',
    'Coast Capital Savings', 'BlueShore Financial', 'Instant Imprints', 'Wellness Pharmacy',
    'Roots Canada', 'Cactus Club', 'Quesada', 'Bailey Nelson']
INVENTORY_NAME_MAPPING = [('CIBC', 'Canadian Imperial Bank of Commerce'), ('Scotiabank', 'Bank of Nova Scotia'),
                          ('Uncle Fatih\'s Pizza', 'Uncle Fatih\'s Pizza'), ('Suki’s', 'Suki\'s')]


def download_and_save_csv(csv_url, output_file):
    """
    Fetches a CSV file from the given URL and saves it to the specified file.

    Parameters:
        csv_url (str): The URL of the CSV file to download.
        output_file (str): The name of the file to save the downloaded content.
    Raises:
        requests.exceptions.RequestException: If there is an error fetching the dataset.
        IOError: If there is an error saving the dataset to the file.
    """
    try:
        response = requests.get(csv_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Error: Unable to fetch the dataset. Reason: {e}")

    try:
        with open(output_file, "wb") as f:
            f.write(response.content)
    except IOError as e:
        raise IOError(f"Error: Failed to save the dataset to {output_file}. Reason: {e}")


def read_csv_to_dataframe(filename, sep=','):
    """
    Reads a CSV file into a pandas DataFrame.

    Parameters:
        filename (str): The name of the CSV file to read.
        sep (str): The delimiter used in the CSV file (default is ',').
    Returns:
        DataFrame: The loaded pandas DataFrame.
    Raises:
        FileNotFoundError: If the file is not found.
        Exception: If there is any other error while reading the file.
    """
    try:
        df = pd.read_csv(filename, sep=sep)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: File {filename} not found. Reason: {e}")
    except Exception as e:
        raise Exception(f"Error: Failed to read the file. Reason: {e}")


def drop_na_columns(df, required_columns):
    """
    Drops rows with NaN values in the specified columns.

    Parameters:
        df (DataFrame): The pandas DataFrame to process.
        required_columns (list): A list of column names where NaN values should be dropped.
    Returns:
        DataFrame: A new DataFrame with rows containing NaN values in the specified columns removed.
    Raises:
        TypeError: If required_columns is not a list.
        KeyError: If any of the specified columns do not exist in the DataFrame.
    """
    if not isinstance(required_columns, list):
        raise TypeError("Error: required_columns must be a list of column names.")
    try:
        df_cleaned = df.dropna(subset=required_columns)
        return df_cleaned
    except KeyError as e:
        raise KeyError(f"Error: One or more columns specified do not exist in the DataFrame. Reason: {e}")


def filter_dataframe_by_str(df, column, value, contain=True):
    """
    Filters a DataFrame based on an exact match of a value in a specified column.

    Parameters:
        df (DataFrame): The pandas DataFrame to filter.
        value (str): The value to filter on.
        column (str): The column to apply the filter to.
        contain (bool): If True, includes rows with the matching value; otherwise, excludes them.
    Returns:
        DataFrame: A new DataFrame with rows filtered by the specified value.
    Raises:
        TypeError: If the value is not a string.
        KeyError: If the specified column does not exist in the DataFrame.
    """
    try:
        if not isinstance(value, str):
            raise TypeError("Error: value must be a String.")
        if contain:
            df = df[df[column] == value]
        else:
            df = df[df[column] != value]
        return df
    except KeyError as e:
        raise KeyError(f"Error: One or more columns specified do not exist in the DataFrame. Reason: {e}")


def filter_dataframe_by_list(df, column:str, value:list):
    """
    Filters a DataFrame to include only rows where the column value is in a specified list.

    Parameters:
        df (DataFrame): The pandas DataFrame to filter.
        value (list): A list of values to filter by.
        column (str): The column to apply the filter to.
    Returns:
        DataFrame: A new DataFrame with rows filtered by the specified values.
    Raises:
        TypeError: If values is not a list.
        KeyError: If the specified column does not exist in the DataFrame.
    """
    try:
        if not isinstance(value, list):
            raise TypeError("Error: Value must be a List.")
        df = df[df[column].isin(value)]
        return df
    except KeyError as e:
        raise KeyError(f"Error: One or more columns specified do not exist in the DataFrame. Reason: {e}")


def filter_dataframe_by_int(df, column, value, condition='min'):
    """
    Filters the DataFrame based on an integer value and a specified condition.

    Parameters:
        df (DataFrame): The pandas DataFrame to filter.
        value (int): The integer value to compare against.
        column (str): The column name to filter on.
        condition (str): The condition for filtering. Options are 'higher', 'lower', or 'equal'.
    Returns:
        DataFrame: A new DataFrame with rows matching the specified condition.
    Raises:
        KeyError: If the condition column does not exist in the DataFrame.
    """
    try:
        if not isinstance(value, int):
            raise TypeError("Error: Value must be a Integer.")
        if condition == 'min':
            return df[df[column] >= value]
        elif condition == 'max':
            return df[df[column] <= value]
        else:
            return df[df[column] == value]
    except KeyError as e:
        raise KeyError(f"Error: One or more columns specified do not exist in the DataFrame. Reason: {e}")


def strip_column_values(df, column, string_to_strip):
    """
    Strips a specific string from all values in a specified column.

    Parameters:
        df (DataFrame): The pandas DataFrame to modify.
        column (str): The name of the column to process.
        string_to_strip (str): The string to remove from each value in the column.
    Returns:
        DataFrame: The modified DataFrame with the string stripped from the column values.
    Raises:
        KeyError: If the specified column does not exist in the DataFrame.
    """
    try:
        df[column] = df[column].str.replace(string_to_strip, '', regex=True)
        return df
    except KeyError as e:
        raise KeyError(f"Error: The specified column does not exist in the DataFrame. Reason: {e}")


def combine_columns_to_new_column(df, list_columns, new_column):
    """
    Combines multiple columns into a new column by concatenating their values.

    Parameters:
        df (DataFrame): The pandas DataFrame to modify.
        list_columns (list): A list of column names to combine.
        new_column (str): The name of the new column to be created.
    Returns:
        DataFrame: The modified DataFrame with the new column added.
    Raises:
        KeyError: If any of the specified columns do not exist in the DataFrame.
    """
    try:
        address = ''
        for column in list_columns:
            address += df[column].fillna('').astype('str')
            address += ' '
        address = address.str.strip()
        df[new_column] = address
        return df
    except KeyError as e:
            raise KeyError(f"Error: One or more columns specified do not exist in the DataFrame. Reason: {e}")


def select_columns(df, columns):
    """
    Selects specific columns from a DataFrame.

    Parameters:
        df (DataFrame): The pandas DataFrame to process.
        columns (list): A list of column names to retain in the DataFrame.
    Returns:
        DataFrame: A new DataFrame containing only the specified columns.
    Raises:
        KeyError: If any of the specified columns do not exist in the DataFrame.
    """
    try:
        return df[columns]
    except KeyError as e:
        raise KeyError(f"Error: One or more columns specified do not exist in the DataFrame. Reason: {e}")


def save_dataframe_to_csv(df, output_file):
    """
    Saves the given DataFrame to a CSV file.

    Parameters:
        df (DataFrame): The pandas DataFrame to save.
        output_file (str): The name of the file to save the DataFrame to.
    Returns:
        None
    Raises:
        IOError: If there is an error saving the DataFrame to the file.
    """
    try:
        df.to_csv(output_file, index=False)
        print(f"DataFrame successfully saved to {output_file}.")
    except IOError as e:
        raise IOError(f"Error: Failed to save the DataFrame to {output_file}. Reason: {e}")


def remove_outliers_by_column(df, column, lower_percentile=5, upper_percentile=95):
    """
    Removes outliers from a DataFrame based on the values in a specified column.

    Parameters:
        df (DataFrame): The pandas DataFrame to process.
        column (str): The name of the column to use for outlier detection.
        lower_percentile (float): The lower percentile cutoff for outlier removal (default is 1).
        upper_percentile (float): The upper percentile cutoff for outlier removal (default is 99).
    Returns:
        DataFrame: A new DataFrame with outliers removed based on the specified column.
    Raises:
        KeyError: If the specified column does not exist in the DataFrame.
    """
    try:
        lower_bound = np.percentile(df[column], lower_percentile)
        upper_bound = np.percentile(df[column], upper_percentile)
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    except KeyError as e:
        raise KeyError(f"Error: The specified column does not exist in the DataFrame. Reason: {e}")


def update_values_based_on_mapping(df, search_column, change_column, mapping_list):
    """
    Updates values in one column based on matches in another column using a list of mapping rules.

    Parameters:
        df (DataFrame): The pandas DataFrame to modify.
        search_column (str): The column to search for matching strings.
        change_column (str): The column where values will be updated.
        mapping_list (list of tuples): A list of tuples where each tuple contains (old_value, new_value).
    Returns:
        DataFrame: The updated DataFrame with mapped values.
    Raises:
        TypeError: If mapping_list is not a list of tuples.
        KeyError: If search_column or change_column does not exist in the DataFrame.
    """
    try:
        if not isinstance(mapping_list, list) or not all(isinstance(item, tuple) and len(item) == 2 for item in mapping_list):
            raise TypeError("Error: mapping_list must be a list of tuples with two elements each.")

        for old_name, new_name in mapping_list:
            if not isinstance(old_name, str) or not isinstance(new_name, str):
                raise TypeError("Error: Both old_name and new_name must be strings.")
            df.loc[df[search_column].str.contains(old_name, case=False, na=False), change_column] = new_name

        return df
    except KeyError as e:
        raise KeyError(f"Error: One or more specified columns do not exist in the DataFrame. Reason: {e}")


def update_column_with_direct_names(df, column_list, names_list):
    """
    Updates a specified column with direct names if they match partially or fully in another column.

    Parameters:
        df (DataFrame): The pandas DataFrame to modify.
        list_column (list): A list of column names to update.
        names_list (list): A list of direct names to check and apply updates.
    Returns:
        DataFrame: The modified DataFrame with updated values.
    Raises:
        KeyError: If the specified columns do not exist in the DataFrame.
        TypeError: If direct_names is not a list.
    """
    try:
        if not isinstance(names_list, list):
            raise TypeError("Error: names_list must be a list.")

        for name in names_list:
            for column in column_list:
                df.loc[df[column].str.contains(name, case=False, na=False), column] = name

        return df
    except KeyError as e:
        raise KeyError(f"Error: One or more specified columns do not exist in the DataFrame. Reason: {e}")


def main():
    """
    Main function to clean and standardize business license and storefront inventory datasets.

    Workflow:
    1. Download Data:
       - Business license data for the years 2013 to 2024.
       - Storefront inventory data for retail businesses.

    2. Process Business License Data:
       - Read the CSV file into a DataFrame.
       - Drop rows with missing business names.
       - Filter data for businesses located in British Columbia and with valid licenses issued in 2024.
       - Remove historic markers from business type and subtype.
       - Combine address components into a single column.
       - Select relevant columns and remove duplicates.
       - Remove outliers based on the number of employees.

    3. Process Storefront Inventory Data:
       - Read the CSV file into a DataFrame.
       - Combine address components into a single column.
       - Filter out vacant or under-construction businesses.
       - Select relevant columns.

    4. Standardize Business Names:
       - Apply predefined mappings to align business names across datasets.
       - Update columns with direct matches based on a list of known names.

    5. Save Cleaned Data:
       - Export the cleaned business license data to `business_cleaned.csv`.
       - Export the cleaned storefront inventory data to `inventory_cleaned.csv`.

    Note:
    - The script uses URLs to fetch the data but can process local files for testing purposes by uncommenting the download lines.
    - Additional mappings for business names can be defined in the `TRADE_NAME_MAPPINGS`, `BUSINESS_NAME_MAPPING`, and `INVENTORY_NAME_MAPPING` lists.
    """
    # business_url = ('https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences-2013-to-2024/'
    #                 'exports/csv?lang=en&timezone=America%2FLos_Angeles&use_labels=true&delimiter=%3B')
    # inventory_url = ('https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/storefronts-inventory/exports/csv'
    #                  '?lang=en&timezone=America%2FLos_Angeles&use_labels=true&delimiter=%3B')
    # Download the csv file for internet
    # download_and_save_csv(business_url, 'business_licenses_2013_to_2024.csv')
    # download_and_save_csv(inventory_url, 'storefronts_inventory.csv')

    # Clean the business file
    business_df = read_csv_to_dataframe('business_licenses_2013_to_2024.csv', sep=';')
    business_df = drop_na_columns(business_df, ['BusinessName'])
    business_df = filter_dataframe_by_list(business_df, 'Province', ['BC', 'British Columbia'])
    business_df = filter_dataframe_by_str(business_df, 'Status', 'Issued', contain=True)
    business_df = filter_dataframe_by_int(business_df, 'NumberofEmployees', MIN_EMPLOYEES, condition='min')
    business_df = filter_dataframe_by_int(business_df, 'FOLDERYEAR', BUSINESS_YEAR_ANALYSIS, condition='equal')
    business_df = strip_column_values(business_df, 'BusinessType', ' *Historic*')
    business_df = strip_column_values(business_df, 'BusinessSubType', ' *Historic*')
    business_df = combine_columns_to_new_column(business_df, ['Unit', 'UnitType', 'House', 'Street'], 'Address')
    business_df = select_columns(business_df, ['FOLDERYEAR', 'BusinessName', 'BusinessTradeName',
                                               'BusinessType', 'BusinessSubType', 'Address', 'City',
                                               'LocalArea', 'NumberofEmployees', 'FeePaid'])
    business_df = business_df.fillna('')
    business_df = business_df.drop_duplicates()
    business_df = remove_outliers_by_column(business_df, 'NumberofEmployees',
                                            lower_percentile=LOWER_THRESHOLD,
                                            upper_percentile=UPPER_THRESHOLD)

    # Clean the inventory file
    inventory_df = read_csv_to_dataframe('storefronts_inventory.csv', sep=';')
    inventory_df = combine_columns_to_new_column(inventory_df,
                                                 ['Unit', 'Civic number - Parcel', 'Street name - Parcel'],
                                                 'Address')
    inventory_df = filter_dataframe_by_str(inventory_df, 'Business name', 'Vacant', contain=False)
    inventory_df = filter_dataframe_by_str(inventory_df, 'Business name', 'Vacant UC', contain=False)
    inventory_df = filter_dataframe_by_int(inventory_df, 'Year recorded', INVENTORY_YEAR_ANALYSIS, 'equal')
    inventory_df = select_columns(inventory_df, ['ID', 'Business name', 'Retail category',
                                                 'Geo Local Area', 'Address'])

    # Change names on data frame
    # business data frame
    business_df = update_values_based_on_mapping(business_df, 'BusinessTradeName',
                                                 'BusinessName', TRADE_NAME_MAPPINGS)
    business_df = update_values_based_on_mapping(business_df, 'BusinessName',
                                                 'BusinessName', TRADE_NAME_MAPPINGS)
    business_df = update_column_with_direct_names(business_df, ['BusinessTradeName', 'BusinessName'], DIRECT_NAMES)
    # inventory data frame
    inventory_df = update_values_based_on_mapping(inventory_df, 'Business name',
                                                  'Business name', INVENTORY_NAME_MAPPING)

    # Save it to csv
    business_df.to_csv('business_cleaned.csv', index=False)
    inventory_df.to_csv('inventory_cleaned.csv', index=False)


if __name__ == '__main__':
    main()
