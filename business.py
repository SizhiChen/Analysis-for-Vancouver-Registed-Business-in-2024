"""
Strong/Sizhi Chen
CS 5001, Fall 2024
Final Project -- business.py

Business Class Implementation

This script defines the `Business` class, which represents a business entity in the City of Vancouver.
The class includes methods for managing and analyzing various attributes of a business, such as its type,
addresses, employees, inventory, and registration fees.

Key Features:
1. **Attribute Management**:
   - Allows adding and tracking multiple types, addresses, employees, and inventories for a business.

2. **Data Aggregation**:
   - Provides methods to calculate the total number of employees, stores, and inventories.

3. **Business Summary**:
   - Includes a string representation method (`__str__`) for summarizing business details.

4. **Comparison**:
   - Implements an equality method (`__eq__`) to compare two business objects based on their attributes.

This class is designed to be used as part of a larger application for business and inventory analysis.
"""


class Business:
    """
    Represents a business entity in the City of Vancouver

    Including its details, operations, and associated data such
    as addresses, employees, inventory, and registration fees.

    Attributes:
        name (str): The name of the business.
        city (str): The city where the business is located.
        local_area (str): The local area within the city.
        type (list): A list of types or categories associated with the business.
        address (list): A list of store addresses for the business.
        employees (list): A list of employee counts for each store or location.
        inventory_list (list): A list of inventories associated with the business.
        register_fee (float): The total registration fee paid by the business.
    Methods:
        add_type(type): Adds a type or category to the business.
        add_address(address): Adds a unique store address to the business.
        add_employee(employee): Adds the number of employees for a specific store or location.
        add_inventory(inventory): Adds inventory details to the business.
        add_register_fee(register_fee): Adds the registration fee paid by the business.
        get_main_business(): Determines the primary type or category of the business.
        get_number_store(): Calculates the number of unique stores the business has.
        get_number_employees(): Calculates the total number of employees across all stores.
        get_number_of_inventory(): Calculates the total number of inventories associated with the business.
        __str__(): Returns a summary description of the business.
        __eq__(other): Compares two Business objects for equality based on their attributes.
    """
    def __init__(self, name, city, local_area):
        """
        Initializes a new Business object.

        Args: name (str): The name of the business.
              city (str): The city where the business is located.
              local_area (str): The local area within the city.
        """
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        if not isinstance(city, str):
            raise ValueError("City must be a string.")
        if not isinstance(local_area, str):
            raise ValueError("Local area must be a string.")
        self.name = name
        self.city = city
        self.local_area = local_area
        self.type = []
        self.address = []
        self.employees = []
        self.inventory_list = []
        self.register_fee = 0

    def add_type(self, business_type):
        """
        Adds a type or category to the business.

        Args: type (str): The type/category of the business (e.g., retail, manufacturing).
        """
        if not isinstance(business_type, str):
            raise ValueError("Type must be a string.")
        self.type.append(business_type)

    def add_address(self, address):
        """
        Adds a store address to the business if it is not already present.

        Args: address (str): The address of the store to add.
        """
        if not isinstance(address, str):
            raise ValueError("Address must be a string.")
        if address.lower() not in self.address:
            self.address.append(address.lower())

    def add_employee(self, employee):
        """
        Adds the number of employees for a specific store or location.

        Args: employee (int): The number of employees to add.
        """
        if not isinstance(employee, int) or employee <= 0:
            raise ValueError("Employee must be a positive integer.")
        self.employees.append(employee)

    def add_inventory(self, inventory):
        """
        Adds a list of inventories to the business.

        Args: inventory (list): A list of inventories associated with the business.
        """
        if not isinstance(inventory, list):
            raise ValueError("Inventory must be a list.")
        self.inventory_list += inventory

    def add_register_fee(self, register_fee):
        """
        Adds the registration fee paid by the business.

        Args: register_fee (float): The registration fee to add.
        """
        if register_fee != '':
            if not isinstance(register_fee, float) or register_fee < 0:
                raise ValueError("Registration fee must be a non-negative number.")
            self.register_fee += register_fee

    def get_main_business(self):
        """
        Determines the primary type or category of the business.

        Returns: str: The most common type/category of the business.
        """
        if not self.type:
            return "Unknown"
        return max(self.type, key=self.type.count)

    def get_number_store(self):
        """
        Calculates the number of unique stores (addresses) the business has.

        Returns: int: The number of stores.
        """
        return len(self.address)

    def get_number_employees(self):
        """
        Calculates the total number of employees across all stores.

        Returns: int: The total number of employees.
        """
        return sum(self.employees)

    def get_number_of_inventory(self):
        """
        Calculates the total number of inventories associated with the business.

        Returns: int: The total number of inventories.
        """
        return len(self.inventory_list)

    def __str__(self):
        """
        Provides a summary description of the business.

        Returns: str: A descriptive string summarizing the business details.
        """
        main_business = self.get_main_business()
        return (f"{self.name} is a {main_business} company in {self.city}.\n"
                f"It has {self.get_number_store()} store with {self.get_number_employees()} employees.\n"
                f"There are {self.get_number_of_inventory()} inventories which belong to this company.\n"
                f"The total registration fee which the company paid is {self.register_fee}.")

    def __eq__(self, other):
        """
        Compares two Business objects for equality based on their attributes.

        Args:
            other (Business): Another instance of the Business class to compare.
        Returns:
            bool: True if the two objects have the same name, city, local area, and main business type; False otherwise.
        """
        if not isinstance(other, Business):
            return False
        return (self.name == other.name and
                self.city == other.city and
                self.local_area == other.local_area and
                self.get_main_business() == other.get_main_business())
