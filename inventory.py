"""
Strong/Sizhi Chen
CS 5001, Fall 2024
Final Project -- inventory.py

Inventory Class Implementation

This script defines the `Inventory` class, which represents inventory data associated with a business in the City of Vancouver.
The class includes methods for managing and analyzing attributes such as inventory locations and business types.

Key Features:
1. **Attribute Management**:
   - Allows adding and tracking multiple types and addresses for inventory locations.

2. **Data Aggregation**:
   - Provides methods to calculate the total number of unique inventory locations.

3. **Inventory Summary**:
   - Includes a string representation method (`__str__`) for summarizing inventory details.

4. **Comparison**:
   - Implements an equality method (`__eq__`) to compare two inventory objects based on their attributes.

This class is designed to complement the `Business` class as part of a larger application for business and inventory analysis.
"""


class Inventory:
    """
    Represents inventory data for a business, including its type and locations.

    The `Inventory` class is designed to store and manage information related to a business's inventory,
    such as its type, address locations, and associated business name. It also provides methods to analyze
    and summarize this data.
    Attributes:
        name (str): The name of the business associated with this inventory.
        type (list): A list of business types or categories related to the inventory.
        address (list): A list of unique inventory locations (addresses).
    Methods:
        add_type(type): Adds a business type/category to the inventory.
        add_address(address): Adds a unique inventory location (address).
        get_number_of_inventory(): Returns the total number of unique inventory locations.
        get_main_business(): Returns the most frequent business type/category.
        __str__(): Provides a summary description of the inventory.
        __eq__(other): Compares two Inventory objects for equality based on their attributes.
    """
    def __init__(self, name):
        """
        Initializes a new Inventory object.

        Args: name (str): The name of the business associated with this inventory.
        """
        if not isinstance(name, str):
            raise ValueError("Business name must be a string.")
        self.name = name
        self.type = []
        self.address = []

    def add_type(self, category):
        """
        Adds a business type/category associated with the inventory.

        Args: type (str): The business type (e.g., retail, wholesale).
        """
        if not isinstance(category, str):
            raise ValueError("Business type must be a string.")
        self.type.append(category)

    def add_address(self, address):
        """
        Adds an inventory location (address) if it is not already present.

        Args: address (str): The inventory address to add.
        """
        if not isinstance(address, str):
            raise ValueError("Address must be a string.")
        if address not in self.address:
            self.address.append(address)

    def get_number_of_inventory(self):
        """
        Calculates the total number of unique inventory locations.

        Returns: int: The total number of inventory locations.
        """
        return len(self.address)

    def get_main_business(self):
        """
        Determines the primary business type associated with the inventory.

        Returns: str: The most common business type/category.
        """
        if not self.type:
            return "Unknown"
        return max(self.type, key=self.type.count)

    def __str__(self):
        """
        Provides a summary description of the inventory.

        Returns: str: A descriptive string summarizing the inventory details.
        """
        number_of_inventory = self.get_number_of_inventory()
        main_business = self.get_main_business()
        return f'{self.name} is a {main_business} company, which has {number_of_inventory} inventory.'

    def __eq__(self, other):
        """
        Compares two Inventory objects for equality based on their attributes.

        Args:
            other (Inventory): Another instance of the Inventory class to compare.
        Returns:
            bool: True if the two objects have the same name, primary business type, and inventory addresses; False otherwise.
        """
        if not isinstance(other, Inventory):
            return False
        return (self.name == other.name and
                self.get_main_business() == other.get_main_business())
