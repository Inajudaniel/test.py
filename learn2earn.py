import json
import os

borrow_records = []

DATA_FILE = "data.json"


def save_data():
    data = {
        "resources": resources,
        "borrow_records": borrow_records
    }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    global resources, borrow_records

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    resources = data.get("resources", resources)
    borrow_records = data.get("borrow_records", [])

resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
]

fellows = {
    "F001": "Ada",
    "F002": "John",
    "F003": "Grace"
}

borrow_records = []


def find_resource(resource_id):
    for resource in resources:
        if resource["id"] == resource_id:
            return resource
    return None


def find_borrow_record(fellow_id, resource_id):
    for record in borrow_records:
        if record["fellow_id"] == fellow_id and record["resource_id"] == resource_id:
            return record
    return None   

def add_resource():
    resource_id = input("Enter resource ID: ").strip()

    if find_resource(resource_id):
        print("Error: Resource ID already exists.")
        return

    name = input("Enter resource name: ").strip()
    category = input("Enter category: ").strip()

    try:
        total = int(input("Enter total units: "))

        if total <= 0:
            print("Error: Total units must be greater than 0.")
            return

    except ValueError:
        print("Error: Total units must be an integer.")
        return

    resource = {
        "id": resource_id,
        "name": name,
        "category": category,
        "total": total,
        "available": total
    }

    resources.append(resource)
    save_data()
    print("Resource added successfully.")


def list_resources():
    if not resources:
        print("No resources available.")
        return

    print("\n--- Resource Inventory ---")

    for resource in resources:
        print(
            f"ID: {resource['id']} | "
            f"Name: {resource['name']} | "
            f"Category: {resource['category']} | "
            f"Total: {resource['total']} | "
            f"Available: {resource['available']}"
        )

def borrow_resource():
    fellow_id = input("Enter fellow ID: ").strip()

    if fellow_id not in fellows:
        print("Error: Fellow ID not found.")
        return

    resource_id = input("Enter resource ID: ").strip()

    resource = find_resource(resource_id)

    if resource is None:
        print("Error: Resource ID not found.")
        return

    try:
        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("Error: Quantity must be a positive integer.")
            return

    except ValueError:
        print("Error: Quantity must be a positive integer.")
        return

    if quantity > resource["available"]:
        print("Error: Not enough units available.")
        return

    record = find_borrow_record(fellow_id, resource_id)

    if record:
        record["quantity"] += quantity
    else:
        borrow_records.append({
            "fellow_id": fellow_id,
            "resource_id": resource_id,
            "quantity": quantity
        })

    resource["available"] -= quantity
    save_data()

    print(
        f"{fellows[fellow_id]} successfully borrowed "
        f"{quantity} {resource['name']}(s)."
    )

def return_resource():
    fellow_id = input("Enter fellow ID: ").strip()

    if fellow_id not in fellows:
        print("Error: Fellow ID not found.")
        return

    resource_id = input("Enter resource ID: ").strip()

    resource = find_resource(resource_id)

    if resource is None:
        print("Error: Resource ID not found.")
        return

    try:
        quantity = int(input("Enter quantity to return: "))

        if quantity <= 0:
            print("Error: Quantity must be a positive integer.")
            return

    except ValueError:
        print("Error: Quantity must be a positive integer.")
        return

    record = find_borrow_record(fellow_id, resource_id)

    if record is None:
        print("Error: This fellow has no units of this resource on loan.")
        return

    if quantity > record["quantity"]:
        print("Error: Cannot return more than the fellow currently has.")
        return

    record["quantity"] -= quantity
    resource["available"] += quantity

    if record["quantity"] == 0:
        borrow_records.remove(record)

    print(
        f"{fellows[fellow_id]} successfully returned "
        f"{quantity} {resource['name']}(s)."
    )

def search_resources():
    search_term = input("Enter resource name to search: ").strip().lower()

    found = False

    for resource in resources:
        if search_term in resource["name"].lower():
            print(
                f"ID: {resource['id']} | "
                f"Name: {resource['name']} | "
                f"Category: {resource['category']} | "
                f"Total: {resource['total']} | "
                f"Available: {resource['available']}"
            )
            found = True

    if not found:
        print("No resources found.")

def filter_by_category():
    category = input("Enter category: ").strip().lower()

    found = False

    for resource in resources:
        if resource["category"].lower() == category:
            print(
                f"ID: {resource['id']} | "
                f"Name: {resource['name']} | "
                f"Category: {resource['category']} | "
                f"Total: {resource['total']} | "
                f"Available: {resource['available']}"
            )
            found = True

    if not found:
        print("No resources found in that category.")

def generate_report():
    total_units = sum(resource["total"] for resource in resources)
    available_units = sum(resource["available"] for resource in resources)
    borrowed_units = total_units - available_units

    print("\n===== Resource Report =====")
    print(f"Total units: {total_units}")
    print(f"Available units: {available_units}")
    print(f"Currently borrowed units: {borrowed_units}")

    print("\nResources with fewer than 3 available units:")

    low_stock = False

    for resource in resources:
        if resource["available"] < 3:
            print(
                f"- {resource['name']}: "
                f"{resource['available']} available"
            )
            low_stock = True

    if not low_stock:
        print("None")

    borrowed_amounts = []

    for resource in resources:
        borrowed = resource["total"] - resource["available"]
        borrowed_amounts.append((resource, borrowed))

    highest_borrowed = max(
        borrowed for resource, borrowed in borrowed_amounts
    )

    print("\nResource(s) with the most currently borrowed:")

    for resource, borrowed in borrowed_amounts:
        if borrowed == highest_borrowed:
            print(
                f"- {resource['name']}: "
                f"{borrowed} borrowed"
            )
    
def show_menu():
    while True:
        print("\n===== Learn2Earn Resource System =====")
        print("1. Add resource")
        print("2. List resources")
        print("3. borrow resource")
        print("4. return resources")
        print("5. search resources")
        print("6. filter by category")
        print("7. generate report")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_resource()
        elif choice == "2":
            list_resources()
        elif choice == "3":
            borrow_resource()
        elif choice == "4":
            return_resource()
        elif choice == "5":
            search_resources()
        elif choice == "6":
            filter_by_category()
        elif choice == "7": 
            generate_report()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1, 2, 3, 4, 5, 6, 7 or 8.")
load_data()
show_menu()