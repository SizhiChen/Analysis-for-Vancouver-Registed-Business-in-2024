"""
Strong/Sizhi Chen
CS 5001, Fall 2024
Final Project -- drive.py

Business and Inventory Analysis

This script processes cleaned business and inventory data to initialize and update objects representing
businesses and inventories in the City of Vancouver. It combines these objects to create dataframes
for further analysis and visualization.

Key Features:
1. **Object Initialization**:
   - Creates instances of `Business` and `Inventory` classes from cleaned CSV data.
   - Updates objects with details such as type, address, employee counts, inventory counts, and registration fees.

2. **Data Filtering**:
   - Filters inventory objects based on a configurable threshold (`INVENTORY_THRESHOLD`).

3. **Dataframe Creation**:
   - Converts processed business and inventory data into pandas DataFrames for analysis.

4. **GUI Integration**:
   - Launches a graphical user interface (GUI) for data visualization using the `BusinessApp` class from `app`.

The script integrates with data cleaning tools to generate clean datasets, and then transforms them into
structured data for visualization and analysis.

Dependencies:
- `pandas`: For data manipulation.
- `tkinter`: For GUI.
- Custom modules: `app`, `business`, `inventory`.
"""


# Import the modules and classes
import pandas as pd
from app import *
from business import *
from inventory import *


# Set constants
INVENTORY_THRESHOLD = 3
BUSINESS_NAME_INDEX = 1
BUSINESS_TYPE_INDEX = 3
BUSINESS_ADDRESS_INDEX = 5
BUSINESS_CITY_INDEX = 6
BUSINESS_LOCAL_AREA_INDEX = 7
BUSINESS_EMPLOYEES = 8
BUSINESS_REGISTER_FEE = 9
INVENTORY_NAME_INDEX = 1
INVENTORY_CATEGORY_INDEX = 2
INVENTORY_ADDRESS = 4


def read_from_csv(filename: str) -> list[str]:
    """
    Reads csv file to pd.dataframe, and converts it into a list

    Parameters:
    filename : str
        The name of the file to be read. Must be a
        valid path to a readable text file.
    Returns:
    list[str]
        A list of strings where each element is a
        line from the file (excluding the header line).
        If the file cannot be found, returns None
        and prints an error message.
    Raises:
    IOError
        If the specified file is not found, an error
        message is printed.
    TypeError
        If `filename` is not a string, a generic error
        message is printed.
    """
    # Check the filename is validated
    try:
        file = pd.read_csv(filename)
    except IOError:
        print(f'FileNotFoundError: File {filename} not found.')
    except TypeError:
        print('TypeError: Please input the filename as string.')
    # For Validated filename
    else:
        # Convert dataframe to list
        business_list = file.fillna('').values.tolist()
        return business_list


# Function about business class
def initial_business_class(dataframe_list):
    """
    Initializes a dictionary of Business objects from a list of data.

    Args: dataframe_list (list):
        A list of data rows, where each row is a list
        information about a business in the following order:
        [year, name, trade_name, type, sub_type,
        address, city, local_area, numOfEmployees, fee].
    Returns: dict:
        A dictionary where the keys are business names (line[1]) and the values are
        instances of the Business class initialized with the corresponding data.
    """
    if not isinstance(dataframe_list, list):
        raise ValueError("dataframe_list must be a list of data rows.")

    business_dict = {}
    for line in dataframe_list:
        if line[1] not in business_dict.keys():
            # __init__(self, name, type, sub_type, city, local_area)
            business_dict[line[BUSINESS_NAME_INDEX]] = (
                Business(line[BUSINESS_NAME_INDEX],
                         line[BUSINESS_CITY_INDEX],
                         line[BUSINESS_LOCAL_AREA_INDEX]))
    return business_dict


def add_type_business(object_dict, dataframe_list):
    """
    Updates business objects in a dictionary with type information.

    Args: object_dict (dict):
        A dictionary of objects (e.g., Business instances),
        where keys are identifiers (e.g., business names) and values are the objects.
    dataframe_list (list):
        A list of data rows, where each row is a list or iterable containing:
            - Identifier at line[1] (corresponding to keys in `object_dict`)
            - Type information at line[3].
    Returns: dict:
        The updated `object_dict` with the `add_type` method called
        on each relevant object, using the type information from `dataframe_list`.
    """
    if not isinstance(object_dict, dict):
        raise ValueError("object_dict must be a dict of data object.")
    if not isinstance(dataframe_list, list):
        raise ValueError("dataframe_list must be a list of data rows.")

    for line in dataframe_list:
        object_dict[line[BUSINESS_NAME_INDEX]].add_type(
            line[BUSINESS_TYPE_INDEX])
    return object_dict


def add_address_business(object_dict, dataframe_list):
    """
    Updates business objects in a dictionary with address information.

    Args: object_dict (dict):
        A dictionary of objects (e.g., Business instances),
        where keys are identifiers (e.g., business names) and values are the objects.
    dataframe_list (list):
        A list of data rows, where each row is a list or iterable containing:
            - Identifier at line[1] (corresponding to keys in `object_dict`)
            - Address information at line[5].
    Returns: dict:
        The updated `object_dict` with the `add_address` method called
        on each relevant object, using the address data from `dataframe_list`.
    """
    if not isinstance(object_dict, dict):
        raise ValueError("object_dict must be a dict of data object.")
    if not isinstance(dataframe_list, list):
        raise ValueError("dataframe_list must be a list of data rows.")

    for line in dataframe_list:
        object_dict[line[BUSINESS_NAME_INDEX]].add_address(
            line[BUSINESS_ADDRESS_INDEX])
    return object_dict


def add_employees_business(object_dict, dataframe_list):
    """
    Updates objects in a dictionary with employee count information.

    Args: object_dict (dict):
        A dictionary of objects (e.g., Business instances),
        where keys are names and values are the objects.
    dataframe_list (list):
        A list of data rows, where each row is a list or iterable containing
        a names at line[1] (corresponding to the keys in `object_dict`)
        and the employee count at line[-2].

    Returns: dict:
        The updated `object_dict` with the `add_employee` method called
        on each relevant object, using the employee count from `dataframe_list`.
    """
    if not isinstance(object_dict, dict):
        raise ValueError("object_dict must be a dict of data object.")
    if not isinstance(dataframe_list, list):
        raise ValueError("dataframe_list must be a list of data rows.")

    for line in dataframe_list:
        object_dict[line[BUSINESS_NAME_INDEX]].add_employee(
            int(line[BUSINESS_EMPLOYEES]))
    return object_dict


def add_inventory_business(business: dict, inventory: dict):
    """
    Adds inventory details to the corresponding business entries.

    Args: business (dict):
        A dictionary where keys are business identifiers
        and values are business objects with an 'add_inventory' method.
    inventory (dict):
        A dictionary where keys are business identifiers
        and values contain inventory details with an 'address' attribute.
    Returns: dict:
        The updated business dictionary with inventory details added.
    """
    if not isinstance(business, dict):
        raise ValueError("business must be a dict of data object.")
    if not isinstance(inventory, dict):
        raise ValueError("inventory must be a dict of data object.")

    for key, value in inventory.items():
        if key in business.keys():
            business[key].add_inventory(value.address)
    return business


def add_register_fee_business(object_dict, dataframe_list):
    """
    Updates business objects in a dictionary with registration fee information.

    Args: object_dict (dict):
        A dictionary of objects (e.g., Business instances),
        where keys are identifiers (e.g., business names) and values are the objects.
    dataframe_list (list):
        A list of data rows, where each row is a list or iterable containing:
            - Identifier at line[1] (corresponding to keys in `object_dict`)
            - Registration fee information at line[-1].
    Returns: dict:
        The updated `object_dict` with the `add_register_fee` method called
        on each relevant object, using the registration fee data from `dataframe_list`.
    """
    if not isinstance(object_dict, dict):
        raise ValueError("object_dict must be a dict of data object.")
    if not isinstance(dataframe_list, list):
        raise ValueError("dataframe_list must be a list of data rows.")

    for line in dataframe_list:
        object_dict[line[BUSINESS_NAME_INDEX]].add_register_fee(
            line[BUSINESS_REGISTER_FEE])
    return object_dict


# Function about inventory class
def initial_inventory_class(dataframe_list):
    """
    Initializes a dictionary of Inventory objects from a list of data.

    Args: dataframe_list (list):
        A list of data rows, where each row is a list or iterable containing
        information about inventory in the following order:
        [ID, name, type, year, local_area, address].
    Returns: dict:
        A dictionary where the keys are inventory identifiers (line[1]) and the values are
        instances of the Inventory class initialized with the corresponding data.
    """
    if not isinstance(dataframe_list, list):
        raise ValueError("dataframe_list must be a list of data rows.")

    inventory_dict = {}
    for line in dataframe_list:
        if line[1] not in inventory_dict.keys():
            inventory_dict[line[INVENTORY_NAME_INDEX]] = Inventory(line[INVENTORY_NAME_INDEX])
    return inventory_dict


def add_type_inventory(object_dict, dataframe_list):
    """
    Updates inventory objects in a dictionary with type information.

    Args: object_dict (dict):
        A dictionary of objects (e.g., Inventory instances),
        where keys are identifiers (e.g., inventory IDs) and values are the objects.
    dataframe_list (list):
        A list of data rows, where each row is a list or iterable containing:
            - Identifier at line[1] (corresponding to keys in `object_dict`)
            - Type information at line[2].
    Returns: dict:
        The updated `object_dict` with the `add_type` method called
        on each relevant object, using the type information from `dataframe_list`.
    """
    if not isinstance(object_dict, dict):
        raise ValueError("object_dict must be a dict of data object.")
    if not isinstance(dataframe_list, list):
        raise ValueError("dataframe_list must be a list of data rows.")

    for line in dataframe_list:
        object_dict[line[INVENTORY_NAME_INDEX]].add_type(line[INVENTORY_CATEGORY_INDEX])
    return object_dict


def add_address_inventory(object_dict, dataframe_list):
    """
    Updates inventory objects in a dictionary with address information.

    Args: object_dict (dict):
        A dictionary of objects (e.g., Inventory instances),
        where keys are identifiers (e.g., inventory IDs) and values are the objects.
    dataframe_list (list):
        A list of data rows, where each row is a list or iterable containing:
            - Identifier at line[1] (corresponding to keys in `object_dict`)
            - Additional address-related data at line[3] and line[-1].
    Returns: dict:
        The updated `object_dict` with the `add_address` method called
        on each relevant object, using address-related data from `dataframe_list`.
    """
    if not isinstance(object_dict, dict):
        raise ValueError("object_dict must be a dict of data object.")
    if not isinstance(dataframe_list, list):
        raise ValueError("dataframe_list must be a list of data rows.")

    for line in dataframe_list:
        object_dict[line[INVENTORY_NAME_INDEX]].add_address(line[INVENTORY_ADDRESS])
    return object_dict


# Find related business name
def find_inventory(inventory_threshold: int, object_dict: dict):
    """
    Filters and retrieves inventory objects based on a minimum inventory threshold.

    Args: inventory_threshold (int):
        The minimum number of inventory items required
        for an object to be included in the result.
    object_dict (dict):
        A dictionary of objects (e.g., Inventory instances),
        where keys are identifiers (e.g., inventory IDs) and values are the objects.

    Returns: dict:
        A dictionary containing the filtered objects from `object_dict` where the
        `get_number_of_inventory` method returns a value greater than or equal to
        `inventory_threshold`.
    """
    if not isinstance(inventory_threshold, int):
        raise ValueError("inventory_threshold must be an integer.")
    if not isinstance(object_dict, dict):
        raise ValueError("object_dict must be a dict of data object.")

    result = {}
    for key, value in object_dict.items():
        if value.get_number_of_inventory() >= inventory_threshold:
            result[key] = value
    return result


def main():
    """
    Main function for processing business and inventory data, and launching the GUI for visualization.

    Workflow:
    1. **Read Data**:
       - Loads cleaned business and inventory data from CSV files into lists.

    2. **Object Initialization**:
       - Initializes `Business` objects and updates them with type, address, employees, and fees.
       - Initializes `Inventory` objects and updates them with type and address.

    3. **Combine Data**:
       - Filters inventory objects based on the `INVENTORY_THRESHOLD`.
       - Adds inventory data to the corresponding businesses.

    4. **Create DataFrames**:
       - Converts the `Business` and `Inventory` objects into pandas DataFrames.

    5. **Launch GUI**:
       - Initializes and runs the `BusinessApp` GUI for visualizing the processed data.
    """
    # Read two files
    business_list = read_from_csv('business_cleaned.csv')
    inventory_list = read_from_csv('inventory_cleaned.csv')

    # Setting for business Class
    business_dict = initial_business_class(business_list)
    business_dict = add_type_business(business_dict, business_list)
    business_dict = add_address_business(business_dict, business_list)
    business_dict = add_employees_business(business_dict, business_list)
    business_dict = add_register_fee_business(business_dict, business_list)

    # Setting for inventory Class
    inventory_dict = initial_inventory_class(inventory_list)
    inventory_dict = add_type_inventory(inventory_dict, inventory_list)
    inventory_dict = add_address_inventory(inventory_dict, inventory_list)

    # Combine two dictionary together
    inventory_threshold = find_inventory(INVENTORY_THRESHOLD, inventory_dict)
    business_dict = add_inventory_business(business_dict, inventory_threshold)

    # Convert into DataFrame
    business_df = [
        {'Business Name': value.name,
         'Business Category': value.get_main_business(),
         'Number of Store': value.get_number_store(),
         'Number of Employees': value.get_number_employees(),
         'Number of Inventory': value.get_number_of_inventory(),
         'Total Register Fee': value.register_fee,
         'City': value.city}
        for value in list(business_dict.values())
    ]
    business_df = pd.DataFrame(business_df)
    inventory_df = [
        {'Business Name': value.name,
         'Business Category': value.get_main_business(),
         'Number of inventory': value.get_number_of_inventory()}
        for value in list(inventory_dict.values())
    ]
    inventory_df = pd.DataFrame(inventory_df)

    # # GUI using Tkinter
    root = Tk()
    app = BusinessApp(root, business_df, inventory_df)
    root.mainloop()
    print(app)


if __name__ == '__main__':
    main()
