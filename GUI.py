import tkinter as tk
from tkinter import messagebox, ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

# Import the necessary classes (your database models)
from employee_db import Employee, Customer, Device, Borrowing, Sale, Inventory

# Setup Database
engine = create_engine('sqlite:///iqos_management.db')
Session = sessionmaker(bind=engine)
session = Session()

# Setup Tkinter Window
root = tk.Tk()
root.title("IQOS Management System")

# Function to Validate Customer Input
def validate_customer_input(name, contact):
    if not name or not contact:
        messagebox.showwarning("Input Error", "Both Name and Contact are required!")
        return False
    return True

# Function to Add a Customer
def add_customer():
    name = entry_customer_name.get()
    contact = entry_customer_contact.get()

    if validate_customer_input(name, contact):
        new_customer = Customer(name=name, contact_info=contact)
        session.add(new_customer)
        session.commit()
        messagebox.showinfo("Success", f"Customer {name} added successfully!")
        display_customers()

# Function to Add a Device
def add_device():
    name = entry_device_name.get()
    model = entry_device_model.get()

    if name and model:
        new_device = Device(name=name, model=model, status="available")
        session.add(new_device)
        session.commit()
        messagebox.showinfo("Success", f"Device {name} added successfully!")
        display_devices()
    else:
        messagebox.showwarning("Input Error", "Please fill out all fields.")

# Function to Add Borrowing Record
def add_borrowing():
    customer_name = entry_borrowing_customer_name.get()
    device_name = entry_borrowing_device_name.get()

    # Find the corresponding customer and device by name
    customer = session.query(Customer).filter_by(name=customer_name).first()
    device = session.query(Device).filter_by(name=device_name, status='available').first()

    if customer and device:
        # Create a borrowing record
        new_borrowing = Borrowing(customer_id=customer.id, device_id=device.id, borrow_date=date.today())
        session.add(new_borrowing)

        # Update device status
        device.status = "borrowed"
        session.commit()
        messagebox.showinfo("Success", f"Device {device_name} borrowed by {customer_name}!")
        display_borrowings()
    else:
        messagebox.showwarning("Input Error", "Invalid customer or device.")

# Function to Update Device Status
def update_device_status(device_name, new_status):
    device = session.query(Device).filter_by(name=device_name).first()
    if device:
        device.status = new_status
        session.commit()
        messagebox.showinfo("Success", f"Device {device_name} status updated to {new_status}!")
        display_devices()
    else:
        messagebox.showwarning("Error", "Device not found!")

# Function to Record a Sale
def record_sale():
    product_name = entry_sale_product_name.get()
    amount = entry_sale_amount.get()

    # Find the device and check if it's available
    device = session.query(Device).filter_by(name=product_name, status="available").first()
    if device and amount:
        sale = Sale(employee_id=1, product_name=product_name, sale_date=date.today(), amount=float(amount))
        session.add(sale)

        # Update inventory for the sold product
        inventory_item = session.query(Inventory).filter_by(item_name=product_name).first()
        if inventory_item:
            inventory_item.quantity_out += 1
            inventory_item.current_stock -= 1
            session.commit()
            messagebox.showinfo("Success", f"Sale recorded for {product_name}!")
            display_inventory()
        else:
            messagebox.showwarning("Inventory Error", f"No inventory found for {product_name}.")
        session.commit()
    else:
        messagebox.showwarning("Input Error", "Please provide valid device and amount.")

# Function to Display Customers
def display_customers():
    customers = session.query(Customer).all()
    listbox_customers.delete(0, tk.END)  # Clear current list
    for customer in customers:
        listbox_customers.insert(tk.END, f"{customer.id} - {customer.name} ({customer.contact_info})")

# Function to Display Devices
def display_devices():
    devices = session.query(Device).all()
    listbox_devices.delete(0, tk.END)  # Clear current list
    for device in devices:
        listbox_devices.insert(tk.END, f"{device.id} - {device.name} ({device.status})")

# Function to Display Borrowings
def display_borrowings():
    borrowings = session.query(Borrowing).all()
    treeview_borrowings.delete(*treeview_borrowings.get_children())  # Clear current list

    for borrowing in borrowings:
        treeview_borrowings.insert("", "end", values=(
            borrowing.id, borrowing.customer.name, borrowing.device.name, borrowing.borrow_date))

# Function to Display Inventory
def display_inventory():
    inventory_items = session.query(Inventory).all()
    treeview_inventory.delete(*treeview_inventory.get_children())  # Clear current list

    for item in inventory_items:
        treeview_inventory.insert("", "end", values=(
            item.id, item.item_name, item.quantity_in, item.quantity_out, item.current_stock))

# Layout: Customer Data Entry
tk.Label(root, text="Customer Name").grid(row=0, column=0)
entry_customer_name = tk.Entry(root)
entry_customer_name.grid(row=0, column=1)

tk.Label(root, text="Customer Contact").grid(row=1, column=0)
entry_customer_contact = tk.Entry(root)
entry_customer_contact.grid(row=1, column=1)

tk.Button(root, text="Add Customer", command=add_customer).grid(row=2, columnspan=2)

# Layout: Device Data Entry
tk.Label(root, text="Device Name").grid(row=3, column=0)
entry_device_name = tk.Entry(root)
entry_device_name.grid(row=3, column=1)

tk.Label(root, text="Device Model").grid(row=4, column=0)
entry_device_model = tk.Entry(root)
entry_device_model.grid(row=4, column=1)

tk.Button(root, text="Add Device", command=add_device).grid(row=5, columnspan=2)

# Layout: Borrowing Data Entry
tk.Label(root, text="Customer Name (Borrowing)").grid(row=6, column=0)
entry_borrowing_customer_name = tk.Entry(root)
entry_borrowing_customer_name.grid(row=6, column=1)

tk.Label(root, text="Device Name (Borrowing)").grid(row=7, column=0)
entry_borrowing_device_name = tk.Entry(root)
entry_borrowing_device_name.grid(row=7, column=1)

tk.Button(root, text="Add Borrowing", command=add_borrowing).grid(row=8, columnspan=2)

# Layout: Sale Data Entry
tk.Label(root, text="Product Name (Sale)").grid(row=9, column=0)
entry_sale_product_name = tk.Entry(root)
entry_sale_product_name.grid(row=9, column=1)

tk.Label(root, text="Amount").grid(row=10, column=0)
entry_sale_amount = tk.Entry(root)
entry_sale_amount.grid(row=10, column=1)

tk.Button(root, text="Record Sale", command=record_sale).grid(row=11, columnspan=2)

# Layout: List of Customers
tk.Label(root, text="Customers List").grid(row=12, columnspan=2)
listbox_customers = tk.Listbox(root)
listbox_customers.grid(row=13, column=0, columnspan=2)
display_customers()

# Layout: List of Devices
tk.Label(root, text="Devices List").grid(row=14, columnspan=2)
listbox_devices = tk.Listbox(root)
listbox_devices.grid(row=15, column=0, columnspan=2)
display_devices()

# Layout: Borrowings Treeview
tk.Label(root, text="Borrowings").grid(row=16, columnspan=2)
treeview_borrowings = ttk.Treeview(root, columns=("ID", "Customer", "Device", "Borrow Date"), show="headings")
treeview_borrowings.grid(row=17, column=0, columnspan=2)
treeview_borrowings.heading("ID", text="ID")
treeview_borrowings.heading("Customer", text="Customer")
treeview_borrowings.heading("Device", text="Device")
treeview_borrowings.heading("Borrow Date", text="Borrow Date")

display_borrowings()

# Layout: Inventory Treeview
tk.Label(root, text="Inventory").grid(row=18, columnspan=2)
treeview_inventory = ttk.Treeview(root, columns=("ID", "Item Name", "In", "Out", "Current Stock"), show="headings")
treeview_inventory.grid(row=19, column=0, columnspan=2)
treeview_inventory.heading("ID", text="ID")
treeview_inventory.heading("Item Name", text="Item Name")
treeview_inventory.heading("In", text="Quantity In")
treeview_inventory.heading("Out", text="Quantity Out")
treeview_inventory.heading("Current Stock", text="Current Stock")

display_inventory()

# Run the Tkinter Event Loop
root.mainloop()
