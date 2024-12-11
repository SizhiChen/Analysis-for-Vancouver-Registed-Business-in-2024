"""
Strong/Sizhi Chen
CS 5001, Fall 2024
Final Project -- app.py

Business Analysis GUI Application

This script implements a graphical user interface (GUI) application using `Tkinter` for analyzing
business and inventory data for the City of Vancouver. The application provides various data visualizations
including bar plots, scatter plots, and heatmaps, with options for customizing themes and viewing relationships
between different business metrics.

Key Features:
1. **Data Visualization**:
   - Horizontal bar plots for top businesses or categories based on selected metrics.
   - Scatter plots showing relationships between business metrics with linear regression lines.
   - Heatmaps displaying correlation matrices of selected numerical columns.

2. **Theme Customization**:
   - Four distinct themes: Blue, Green, Orange, and Grey.
   - Theme changes affect both the GUI appearance and visualizations.

3. **Dynamic Plotting**:
   - Interactive controls to modify plot parameters, such as selecting axes, top N entries, and specific columns.
   - Ability to save plots to a file.

4. **Modular Design**:
   - Separate frames for different analysis sections: Information, Business, Inventory, and Relationships.
   - Seamless navigation between different sections.

5. **Interactive Widgets**:
   - Combo boxes for selecting plot parameters.
   - Spin boxes for adjusting the number of displayed entries.
   - Buttons for saving plots and switching between sections.

The application integrates `Matplotlib` for plotting and `Seaborn` for enhanced heatmaps. It also uses the
`ttk` module from `Tkinter` for styled GUI elements.

Classes:
- `BusinessApp`: The main application class containing all the logic for GUI layout, interactions, and data visualizations.

Usage:
- Provide business and inventory datasets as pandas DataFrames when initializing the `BusinessApp` class.
- Run the application to interact with the data through the GUI.
"""


# Import the modules and classes
from tkinter import *
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plot import *


class BusinessApp:
    """
    A graphical user interface (GUI) application for analyzing business data
    in the City of Vancouver. The application provides multiple visualizations
    such as bar plots, scatter plots, and heatmaps, along with theme customization.

    Attributes:
        master (Tk): The root window for the application.
        business_df (DataFrame): DataFrame containing business data.
        inventory_df (DataFrame): DataFrame containing inventory data.
        style (Style): The style configuration for the GUI elements.
        current_fig (Figure): The currently displayed Matplotlib figure.
        corr_matrix (DataFrame): Correlation matrix for selected columns of business data.

    Methods:
        single_column_heatmap_change(event): Updates the heatmap when a single column is selected.
        business_x_axis_change(event): Updates the business plot based on the x-axis selection.
        business_y_axis_change(event): Updates the business plot based on the y-axis selection.
        business_n_companies_spinbox_change(event): Updates the business plot based on the top N selection.
        inventory_x_axis_change(event): Updates the inventory plot based on the x-axis selection.
        inventory_n_companies_spinbox_change(event): Updates the inventory plot based on the top N selection.
        relationship_draw_button(): Draws a scatter plot based on selected x-axis and y-axis variables.
        change_theme(event): Updates the GUI and visualizations based on the selected theme.
        display_plot(frame, fig): Displays a given Matplotlib figure in a specified frame.
        click_infor(event): Displays the "Information" screen.
        click_business(event): Displays the "Business" screen.
        click_inventory(event): Displays the "Inventory" screen.
        click_relationship(event): Displays the "Relationship" screen.
        save_plot(): Saves the currently displayed plot to a file.
    """
    def __init__(self, master, business_df, inventory_df):
        # Initialize the Dataframe
        self.master = master
        self.business_df = business_df
        self.inventory_df = inventory_df
        self.inven_bigger_0 = business_df[business_df['Number of Inventory'] > 0]
        self.corr_matrix = business_df[['Number of Store', 'Number of Employees',
                                        'Number of Inventory', 'Total Register Fee']]
        self.corr_matrix = self.corr_matrix.rename(columns={'Number of Store': 'Store',
                                                            'Number of Employees': 'Employees',
                                                            'Number of Inventory': 'Inventory',
                                                            'Total Register Fee': 'Register Fee'})
        self.current_fig = None

        # Initialize the Window
        self.master.title('Business Analysis App')
        self.master.resizable(False, False)

        # Style
        self.style = ttk.Style()
        # Style for Header Frame
        self.style.configure('Header.TFrame', background='#0279B1')
        self.style.configure('Header.TLabel', background='#0279B1',
                             font = ('Times New Roman', 12), foreground='white')
        self.style.configure('Header.TButton', background='#0279B1', relief='sunken')
        self.style.configure('HeaderH1.TLabel', background='#0279B1',
                             font = ('Times New Roman', 18, 'bold'), foreground='white')
        # Style for Other Frame
        self.style.configure('Other.TFrame', background='#F4FAFD')
        self.style.configure('Infor.TLabel', background='#F4FAFD',
                             font = ('Times New Roman', 12))
        self.style.configure('Other.TLabel', background='#F4FAFD',
                             font = ('Times New Roman', 12))
        self.style.configure('Other.TButton', background='#F4FAFD', relief='sunken')

        # Header Frame
        self.frame_header = ttk.Frame(self.master, style='Header.TFrame')
        self.frame_header.pack(fill='x')
        # Header Widgets
        self.logo = PhotoImage(file='CityOfVancouverLogo.png')
        self.title = 'Business Analysis for City of Vancouver'
        self.infor = ('This is Business Analysis for companies '
                            'which register in 2024 in Great Vancouver Area')
        ttk.Label(self.frame_header, image=self.logo, anchor='e', style='Header.TLabel'
                  ).grid(column=0, row=0, rowspan=2, sticky='nsew')
        ttk.Label(self.frame_header, text=self.title, anchor='center', style='HeaderH1.TLabel'
                  ).grid(column=1, row=0, columnspan=2, sticky='nsew')
        ttk.Label(self.frame_header, text=self.infor, anchor='center', justify='center', wraplength=300,
                  style='Header.TLabel').grid(column=1, row=1, columnspan=2, sticky='nsew')
        # Select Theme
        self.color = ttk.Combobox(self.frame_header, state='readonly', width=8)
        self.color['values'] = ['Blue', 'Green', 'Orange', 'Grey']
        self.color.current(0)
        self.color.grid(column=3, row=1, sticky='ne')
        self.color.bind('<<ComboboxSelected>>', self.change_theme)
        ttk.Label(self.frame_header, text='Select Theme:', anchor='center', style='Header.TLabel', font=('Times New Roman', 10)
                  ).grid(column=3, row=0, sticky='se')
        # Screen Change button
        self.infor_button = ttk.Button(self.frame_header, text='Information', width=30, style='Header.TButton')
        self.infor_button.grid(column=0, row=2, sticky='nsew')
        self.infor_button.bind('<Button-1>', self.click_infor)
        self.business_button = ttk.Button(self.frame_header, text='Business', width=30, style='Header.TButton')
        self.business_button.grid(column=1, row=2, sticky='nsew')
        self.business_button.bind('<Button-1>', self.click_business)
        self.inventory_button = ttk.Button(self.frame_header, text='Inventory', width=30, style='Header.TButton')
        self.inventory_button.grid(column=2, row=2, sticky='nsew')
        self.inventory_button.bind('<Button-1>', self.click_inventory)
        self.relationship_button = ttk.Button(self.frame_header, text='Relationship', width=30, style='Header.TButton')
        self.relationship_button.grid(column=3, row=2, sticky='nsew')
        self.relationship_button.bind('<Button-1>', self.click_relationship)

        # Information Frame
        self.information_frame = ttk.Frame(self.master, style='Other.TFrame')
        self.information_frame.pack(fill='both', expand=True)
        self.max_store_row = business_df.loc[business_df['Number of Store'].idxmax()]
        self.max_employees_row = business_df.loc[business_df['Number of Employees'].idxmax()]
        self.max_inventory_row = inventory_df.loc[inventory_df['Number of inventory'].idxmax()]
        self.max_register_fee = business_df.loc[business_df['Total Register Fee'].idxmax()]
        self.basic_infor = (f'There are total {len(self.business_df):,.0f} business in Vancouver.\n'
                            f'There are total {len(self.inventory_df):,.0f} business which has inventory in Vancouver.\n'
                            f'There are total {len(self.inven_bigger_0)} business which has inventory higher than 2 in Vancouver.\n\n'
                            f'{self.max_employees_row['Business Name']} has the highest number of employees which is {self.max_employees_row['Number of Employees']:,.0f}.\n'
                            f'{self.max_inventory_row['Business Name']} has the highest number of inventory which is {self.max_inventory_row['Number of inventory']}.\n'
                            f'{self.max_store_row['Business Name']} has the highest number of store which is {self.max_store_row['Number of Store']}.\n'
                            f'{self.max_register_fee['Business Name']} has the highest register fee which is {int(self.max_register_fee['Total Register Fee']):,.0f}.')
        ttk.Label(self.information_frame, text=self.basic_infor, anchor='nw', style='Infor.TLabel'
                  ).grid(column=0, row=0, sticky='nsew', padx=20, pady=10)
        # Canvas Frame for entire heatmap
        self.heatmap_canvas_frame = ttk.Frame(self.information_frame)
        self.heatmap_canvas_frame.grid(column=0, row=1, padx=20, pady=10)
        self.heatmap = heatmap(self.corr_matrix, '#F4FAFD', self.color.get() + 's')
        self.display_plot(self.heatmap_canvas_frame, self.heatmap)
        # Combobox for single column heatmap
        ttk.Label(self.information_frame, text='Select Column:', style='Other.TLabel'
                  ).grid(column=1, row=0, sticky='se', padx=5, pady=10)
        self.single_column_combobox = ttk.Combobox(self.information_frame, state='readonly')
        self.single_column_combobox['value'] = self.corr_matrix.columns.tolist()
        self.single_column_combobox.current(0)
        self.single_column_combobox.grid(column=2, row=0, padx=5, pady=10, sticky='sw')
        self.single_column_combobox.bind('<<ComboboxSelected>>', self.single_column_heatmap_change)
        # Canvas Frame for single column heatmap
        self.single_heatmap_canvas_frame = ttk.Frame(self.information_frame)
        self.single_heatmap_canvas_frame.grid(column=1, row=1, padx=20, pady=10, columnspan=2)
        self.single_heatmap = single_column_heatmap(self.corr_matrix, self.single_column_combobox.get(),
                                                    '#F4FAFD', self.color.get() + 's')
        self.display_plot(self.single_heatmap_canvas_frame, self.single_heatmap)


        # Business Frame
        self.business_frame = ttk.Frame(self.master, style='Other.TFrame')
        # self.business_frame.pack(fill='both', expand=True)
        # Sidebar for Business Frame
        self.business_sidebar = ttk.Frame(self.business_frame, style='Other.TFrame')
        self.business_sidebar.grid(column=0, row=0, sticky='nsew', pady = 20)
        # Combobox inside Sidebar for Business Frame
        # x-axis Combobox
        ttk.Label(self.business_sidebar, text='Select x-axis: ', style='Other.TLabel'
                  ).pack(fill='x', padx=20)
        self.business_x_axis_combobox = ttk.Combobox(self.business_sidebar, state='readonly')
        self.business_x_axis_combobox['values'] = ['Business Name', 'Business Category']
        self.business_x_axis_combobox.current(0)
        self.business_x_axis_combobox.pack(fill='x', padx=20, pady=3)
        self.business_x_axis_combobox.bind('<<ComboboxSelected>>', self.business_x_axis_change)
        # y-axis Combobox
        ttk.Label(self.business_sidebar, text='Select y-axis: ', style='Other.TLabel'
                  ).pack(fill='x', padx=20)
        self.business_y_axis_combobox = ttk.Combobox(self.business_sidebar, state='readonly')
        self.business_y_axis_combobox['values'] = ['Number of Store', 'Number of Employees',
                                                   'Total Register Fee']
        self.business_y_axis_combobox.current(0)
        self.business_y_axis_combobox.pack(fill='x', padx=20, pady=3)
        self.business_y_axis_combobox.bind('<<ComboboxSelected>>', self.business_y_axis_change)
        # Spinbox inside Sidebar for Business Frame
        self.business_spinbox_default = StringVar(value='10')  # Set the default Value
        ttk.Label(self.business_sidebar, text='\nTop N Companies: ', style='Other.TLabel'
                  ).pack(fill='x', padx=20)
        self.business_n_companies_spinbox = ttk.Spinbox(self.business_sidebar, from_=5, to=15,
                                                        textvariable=self.business_spinbox_default)
        self.business_n_companies_spinbox.pack(fill='x', padx=20, pady=3)
        self.business_n_companies_spinbox.bind('<ButtonRelease>', self.business_n_companies_spinbox_change)
        # Default Canvas for Business Frame
        self.business_canvas_frame = ttk.Frame(self.business_frame)
        self.business_canvas_frame.grid(column=1, row=0, sticky='nsew', pady = 20)
        self.business_fig = bar_plot(self.business_x_axis_combobox.get(),
                                     self.business_y_axis_combobox.get(),
                                     int(self.business_n_companies_spinbox.get()), self.business_df,
                                     self.style.lookup('Other.TFrame', 'background'),
                                     self.color.get() + 's')
        self.display_plot(self.business_canvas_frame, self.business_fig)
        # Save Button
        self.business_save= ttk.Button(self.business_sidebar, text="Save Plot",
                                       style='Other.TButton', command=self.save_plot)
        self.business_save.pack(fill='x', padx=20, pady=20)

        # Inventory Frame
        self.inventory_frame = ttk.Frame(self.master, style='Other.TFrame')
        # self.inventory_frame.pack(fill='both', expand=True)
        # Sidebar for Inventory Frame
        self.inventory_sidebar = ttk.Frame(self.inventory_frame, style='Other.TFrame')
        self.inventory_sidebar.grid(column=0, row=0, sticky='nsew', pady = 20)
        # Combobox inside Sidebar for Inventory Frame
        # x-axis Combobox
        ttk.Label(self.inventory_sidebar, text='Select x-axis: ', style='Other.TLabel'
                  ).pack(fill='x', padx=20)
        self.inventory_x_axis_combobox = ttk.Combobox(self.inventory_sidebar, state='readonly')
        self.inventory_x_axis_combobox['values'] = ['Business Name', 'Business Category']
        self.inventory_x_axis_combobox.current(0)
        self.inventory_x_axis_combobox.pack(fill='x', padx=20, pady=3)
        self.inventory_x_axis_combobox.bind('<<ComboboxSelected>>', self.inventory_x_axis_change)
        # Spinbox inside Sidebar for Inventory Frame
        self.inventory_spinbox_default = StringVar(value='10')
        self.inventory_spinbox_label = ttk.Label(self.inventory_sidebar, text='\nTop N Brand: ', style='Other.TLabel')
        self.inventory_spinbox_label.pack(fill='x', padx=20)
        self.inventory_n_companies_spinbox = ttk.Spinbox(self.inventory_sidebar, from_=5, to=15,
                                                         textvariable=self.inventory_spinbox_default)
        self.inventory_n_companies_spinbox.pack(fill='x', padx=20, pady=3)
        self.inventory_n_companies_spinbox.bind('<ButtonRelease>', self.inventory_n_companies_spinbox_change)
        # Default Canvas for Inventory Frame
        self.inventory_canvas_frame = ttk.Frame(self.inventory_frame)
        self.inventory_canvas_frame.grid(column=1, row=0, sticky='nsew', pady = 20)
        self.inventory_fig = bar_plot(self.inventory_x_axis_combobox.get(),
                                      'Number of inventory',
                                      int(self.inventory_n_companies_spinbox.get()), self.inventory_df,
                                      self.style.lookup('Other.TFrame', 'background'),
                                      self.color.get() + 's')
        self.display_plot(self.inventory_canvas_frame, self.inventory_fig)
        # Save Button
        self.inventory_save = ttk.Button(self.inventory_sidebar, text="Save Plot",
                                         style='Other.TButton', command=self.save_plot)
        self.inventory_save.pack(fill='x', padx=20, pady=20)

        # Relationship Frame
        self.relationship_frame = ttk.Frame(self.master, style='Other.TFrame')
        # self.relationship_frame.pack(fill='both', expand=True)
        # Sidebar for Relationship Frame
        self.relationship_sidebar = ttk.Frame(self.relationship_frame, style='Other.TFrame')
        self.relationship_sidebar.grid(column=0, row=0, sticky='nsew', pady = 20)
        # Combobox inside Sidebar for Relationship Frame
        # x-axis Combobox
        ttk.Label(self.relationship_sidebar, text='Select x-axis: ', style='Other.TLabel'
                  ).pack(fill='x', padx=20)
        self.relationship_x_axis_combobox = ttk.Combobox(self.relationship_sidebar, state='readonly')
        self.relationship_x_axis_combobox['values'] = ['Number of Store', 'Number of Employees',
                                                       'Number of Inventory', 'Total Register Fee']
        self.relationship_x_axis_combobox.current(2)
        self.relationship_x_axis_combobox.pack(fill='x', padx=20, pady=3)
        # y-axis Combobox
        ttk.Label(self.relationship_sidebar, text='Select y-axis: ', style='Other.TLabel'
                  ).pack(fill='x', padx=20)
        self.relationship_y_axis_combobox = ttk.Combobox(self.relationship_sidebar, state='readonly')
        self.relationship_y_axis_combobox['values'] = ['Number of Store', 'Number of Employees',
                                                       'Number of Inventory', 'Total Register Fee']
        self.relationship_y_axis_combobox.current(0)
        self.relationship_y_axis_combobox.pack(fill='x', padx=20, pady=3)
        # Draw Button
        self.relationship_draw_button = ttk.Button(self.relationship_sidebar, text='Plot Relationship',
                                                   style='Other.TButton', command=self.relationship_draw_button)
        self.relationship_draw_button.pack(fill='x', padx=20, pady=3)

        # Default Canvas for Relationship Frame
        self.relationship_canvas_frame = ttk.Frame(self.relationship_frame)
        self.relationship_canvas_frame.grid(column=1, row=0, sticky='nsew', pady = 20)
        self.relationship_fig = scatter_plot(self.relationship_x_axis_combobox.get(),
                                             self.relationship_y_axis_combobox.get(), self.business_df,
                                             self.style.lookup('Other.TFrame', 'background'),
                                             self.style.lookup('Header.TFrame', 'background'))
        self.display_plot(self.relationship_canvas_frame, self.relationship_fig)
        # Save Button
        self.relationship_save = ttk.Button(self.relationship_sidebar, text="Save Plot",
                                            style='Other.TButton', command=self.save_plot)
        self.relationship_save.pack(fill='x', padx=20, pady=20)

    def single_column_heatmap_change(self, event):
        # Get the single column
        single_column = self.single_column_combobox.get()

        # Update the plot with the selected columns
        background_color = self.style.lookup('Other.TFrame', 'background')
        theme = self.color.get()
        self.single_heatmap = single_column_heatmap(self.corr_matrix, single_column,
                                                    background_color, theme + 's')
        self.display_plot(self.single_heatmap_canvas_frame, self.single_heatmap)


    def business_x_axis_change(self, event):
        # Get the x-axis and y-axis and top n companies request
        x_axis = self.business_x_axis_combobox.get()
        y_axis = self.business_y_axis_combobox.get()
        top_n = self.business_n_companies_spinbox.get()

        # Update the plot with the selected column
        background_color = self.style.lookup('Other.TFrame', 'background')
        bar_color = self.color.get() + 's'
        self.business_fig = bar_plot(x_axis, y_axis, int(top_n), self.business_df,
                                     background_color, bar_color)
        self.current_fig = self.business_fig
        self.display_plot(self.business_canvas_frame, self.business_fig)

    def business_y_axis_change(self,event):
        # Get the x-axis and y-axis and top n companies request
        x_axis = self.business_x_axis_combobox.get()
        y_axis = self.business_y_axis_combobox.get()
        top_n = self.business_n_companies_spinbox.get()

        # Update the plot with the selected column
        background_color = self.style.lookup('Other.TFrame', 'background')
        bar_color = self.color.get() + 's'
        self.business_fig = bar_plot(x_axis, y_axis, int(top_n), self.business_df,
                                     background_color, bar_color)
        self.current_fig = self.business_fig
        self.display_plot(self.business_canvas_frame, self.business_fig)

    def business_n_companies_spinbox_change(self,event):
        # Get the x-axis and y-axis and top n companies request
        x_axis = self.business_x_axis_combobox.get()
        y_axis = self.business_y_axis_combobox.get()
        top_n = self.business_n_companies_spinbox.get()

        # Update the plot with the changed spinbox
        background_color = self.style.lookup('Other.TFrame', 'background')
        bar_color = self.color.get() + 's'
        self.business_fig = bar_plot(x_axis, y_axis, int(top_n), self.business_df,
                                     background_color, bar_color)
        self.current_fig = self.business_fig
        self.display_plot(self.business_canvas_frame, self.business_fig)

    def inventory_x_axis_change(self, event):
        # Get the x-axis and y-axis and top n companies request
        x_axis = self.inventory_x_axis_combobox.get()
        y_axis = 'Number of inventory'
        top_n = self.inventory_n_companies_spinbox.get()

        # Update the plot with the changed spinbox
        background_color = self.style.lookup('Other.TFrame', 'background')
        bar_color = self.color.get() + 's'
        self.inventory_fig = bar_plot(x_axis, y_axis, int(top_n), self.inventory_df,
                                      background_color, bar_color)
        self.current_fig = self.inventory_fig
        self.display_plot(self.inventory_canvas_frame, self.inventory_fig)

        # Display or Hide the spinbox
        if x_axis == 'Business Category':
            self.inventory_spinbox_label.pack_forget()
            self.inventory_n_companies_spinbox.pack_forget()
        else:
            reference_widget = self.inventory_save
            self.inventory_spinbox_label.pack(before=reference_widget,fill='x', padx=20)
            self.inventory_n_companies_spinbox.pack(before=reference_widget, fill='x', padx=20, pady=3)

    def inventory_n_companies_spinbox_change(self, event):
        # Get the x-axis and y-axis and top n companies request
        x_axis = self.inventory_x_axis_combobox.get()
        y_axis = 'Number of inventory'
        top_n = self.inventory_n_companies_spinbox.get()

        # Update the plot with the changed spinbox
        background_color = self.style.lookup('Other.TFrame', 'background')
        bar_color = self.color.get() + 's'
        self.inventory_fig = bar_plot (x_axis, y_axis, int(top_n), self.inventory_df,
                                       background_color, bar_color)
        self.current_fig = self.inventory_fig
        self.display_plot(self.inventory_canvas_frame, self.inventory_fig)

    def relationship_draw_button(self):
        # Get the x-axis and y-axis of the relationship
        x_axis = self.relationship_x_axis_combobox.get()
        y_axis = self.relationship_y_axis_combobox.get()

        # Update the plot with the changed spinbox
        background_color = self.style.lookup('Other.TFrame', 'background')
        bar_color = self.style.lookup('Header.TFrame', 'background')
        if x_axis != y_axis:
            self.relationship_fig = scatter_plot(self.relationship_x_axis_combobox.get(),
                                                 self.relationship_y_axis_combobox.get(),
                                                 self.business_df, background_color, bar_color)
            self.current_fig = self.relationship_fig
            self.display_plot(self.relationship_canvas_frame, self.relationship_fig)

    def change_theme(self, event):
        # Get theme
        theme = self.color.get()

        # Change theme
        if theme == 'Green':
            # Style for Header Frame
            self.style.configure('Header.TFrame', background='#2F9F23')
            self.style.configure('Header.TLabel', background='#2F9F23',
                                 font=('Times New Roman', 12), foreground='white')
            self.style.configure('Header.TButton', background='#2F9F23', relief='sunken')
            self.style.configure('HeaderH1.TLabel', background='#2F9F23',
                                 font=('Times New Roman', 18, 'bold'), foreground='white')
            # Style for Other Frame
            self.style.configure('Other.TFrame', background='#E5F5E4')
            self.style.configure('Infor.TLabel', background='#E5F5E4',
                                 font=('Times New Roman', 12))
            self.style.configure('Other.TLabel', background='#E5F5E4',
                                 font=('Times New Roman', 12))
            self.style.configure('Other.TButton', background='#E5F5E4', relief='sunken')
        elif theme == 'Blue':
            # Style for Header Frame
            self.style.configure('Header.TFrame', background='#0279B1')
            self.style.configure('Header.TLabel', background='#0279B1',
                                 font=('Times New Roman', 12), foreground='white')
            self.style.configure('Header.TButton', background='#0279B1', relief='sunken')
            self.style.configure('HeaderH1.TLabel', background='#0279B1',
                                 font=('Times New Roman', 18, 'bold'), foreground='white')
            # Style for Other Frame
            self.style.configure('Other.TFrame', background='#F4FAFD')
            self.style.configure('Infor.TLabel', background='#F4FAFD',
                                 font=('Times New Roman', 12))
            self.style.configure('Other.TLabel', background='#F4FAFD',
                                 font=('Times New Roman', 12))
            self.style.configure('Other.TButton', background='#F4FAFD', relief='sunken')
        elif theme == 'Orange':
            # Style for Header Frame
            self.style.configure('Header.TFrame', background='#D85109')
            self.style.configure('Header.TLabel', background='#D85109',
                                 font=('Times New Roman', 12), foreground='white')
            self.style.configure('Header.TButton', background='#D85109', relief='sunken')
            self.style.configure('HeaderH1.TLabel', background='#D85109',
                                 font=('Times New Roman', 18, 'bold'), foreground='white')
            # Style for Other Frame
            self.style.configure('Other.TFrame', background='#FAECE0')
            self.style.configure('Infor.TLabel', background='#FAECE0',
                                 font=('Times New Roman', 12))
            self.style.configure('Other.TLabel', background='#FAECE0',
                                 font=('Times New Roman', 12))
            self.style.configure('Other.TButton', background='#FAECE0', relief='sunken')
        else:
            # Style for Header Frame
            self.style.configure('Header.TFrame', background='#131316')
            self.style.configure('Header.TLabel', background='#131316',
                                 font=('Times New Roman', 12), foreground='white')
            self.style.configure('Header.TButton', background='#131316', relief='sunken')
            self.style.configure('HeaderH1.TLabel', background='#131316',
                                 font=('Times New Roman', 18, 'bold'), foreground='white')
            # Style for Other Frame
            self.style.configure('Other.TFrame', background='#dee2e6')
            self.style.configure('Infor.TLabel', background='#dee2e6',
                                 font=('Times New Roman', 12))
            self.style.configure('Other.TLabel', background='#dee2e6',
                                 font=('Times New Roman', 12))
            self.style.configure('Other.TButton', background='#dee2e6', relief='sunken')

        # Re-display the Business fig
        background_color = self.style.lookup('Other.TFrame', 'background')
        bar_color = self.color.get() + 's'
        dot_color = self.style.lookup('Header.TFrame', 'background')
        # Get the x-axis and y-axis and top n companies request
        business_x_axis = self.business_x_axis_combobox.get()
        business_y_axis = self.business_y_axis_combobox.get()
        top_n = self.business_n_companies_spinbox.get()

        # Update the plot with the changed spinbox
        self.business_fig = bar_plot(business_x_axis, business_y_axis, int(top_n),
                                     self.business_df, background_color, bar_color)
        self.current_fig = self.business_fig
        self.display_plot(self.business_canvas_frame, self.business_fig)

        # Re-display the Inventory fig
        # Get the x-axis and y-axis and top n companies request
        inventory_x_axis = self.inventory_x_axis_combobox.get()
        inventory_y_axis = 'Number of inventory'
        top_n = self.inventory_n_companies_spinbox.get()

        # Update the plot with the changed spinbox
        self.inventory_fig = bar_plot(inventory_x_axis, inventory_y_axis, int(top_n),
                                      self.inventory_df, background_color, bar_color)
        self.current_fig = self.inventory_fig
        self.display_plot(self.inventory_canvas_frame, self.inventory_fig)

        # Re-display the Relationship fig
        # Get the x-axis and y-axis of the relationship
        relationship_x_axis = self.relationship_x_axis_combobox.get()
        relationship_y_axis = self.relationship_y_axis_combobox.get()

        # Update the plot with the changed spinbox
        if relationship_x_axis != relationship_y_axis:
            self.relationship_fig = scatter_plot(relationship_x_axis, relationship_y_axis,
                                                 self.business_df, background_color, dot_color)
            self.current_fig = self.relationship_fig
            self.display_plot(self.relationship_canvas_frame, self.relationship_fig)

        # Re-display the Heatmap fig
        self.heatmap = heatmap(self.corr_matrix, background_color, theme + 's')
        self.display_plot(self.heatmap_canvas_frame, self.heatmap)
        # Re-display the single column Heatmap fig
        # Get the single column
        single_column = self.single_column_combobox.get()
        self.single_heatmap = single_column_heatmap(self.corr_matrix, single_column,
                                                    background_color, theme + 's')
        self.display_plot(self.single_heatmap_canvas_frame, self.single_heatmap)

    def display_plot(self, frame, fig):
        # Clear the frame before displaying the new plot
        for widget in frame.winfo_children():
            widget.destroy()

        # Display the new plot
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def click_infor(self, event):
        # Remove all the Frame
        self.business_frame.pack_forget()
        self.inventory_frame.pack_forget()
        self.relationship_frame.pack_forget()
        # Display the Frame we want
        self.information_frame.pack(fill='both', expand=True)

    def click_business(self, event):
        # Remove all the Frame
        self.information_frame.pack_forget()
        self.inventory_frame.pack_forget()
        self.relationship_frame.pack_forget()
        # Display the Frame we want
        self.business_frame.pack(fill='both', expand=True)
        # Current Fig
        self.current_fig = bar_plot(self.business_x_axis_combobox.get(),
                                    self.business_y_axis_combobox.get(),
                                    int(self.business_n_companies_spinbox.get()),
                                    self.business_df, 'white', self.color.get() + 's')

    def click_inventory(self, event):
        # Remove all the Frame
        self.information_frame.pack_forget()
        self.business_frame.pack_forget()
        self.relationship_frame.pack_forget()
        # Display the Frame we want
        self.inventory_frame.pack(fill='both', expand=True)
        # Current Fig
        self.current_fig = bar_plot(self.inventory_x_axis_combobox.get(),
                                    'Number of inventory',
                                    int(self.inventory_n_companies_spinbox.get()),
                                    self.inventory_df, 'white', self.color.get() + 's')

    def click_relationship(self, event):
        # Remove all the Frame
        self.information_frame.pack_forget()
        self.business_frame.pack_forget()
        self.inventory_frame.pack_forget()
        # Display the Frame we want
        self.relationship_frame.pack(fill='both', expand=True)
        # Current Fig
        self.current_fig = scatter_plot(self.relationship_x_axis_combobox.get(),
                                        self.relationship_y_axis_combobox.get(),
                                        self.business_df, 'white', 'skyblue')

    def save_plot(self):
        if self.current_fig:
            # Get the title of the plot from the current figure
            default_filename = self.current_fig.axes[0].get_title()
            # Open the "Save As" dialog with the default filename
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile = default_filename
            )
            if file_path:
                self.current_fig.savefig(file_path)
