from datetime import datetime
from typing import Dict, List, Optional, Tuple

class Product:
    def __init__(self, product_id: int, name: str, price: float, description: str = ""):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.product_id}) - ${self.price:.2f}"

class Inventory:
    def __init__(self):
        self.products: Dict[int, int] = {}  # product_id -> quantity

    def add_product(self, product_id: int, quantity: int) -> None:
        self.products[product_id] = self.products.get(product_id, 0) + quantity

    def remove_product(self, product_id: int, quantity: int) -> bool:
        if product_id not in self.products or self.products[product_id] < quantity:
            return False
        self.products[product_id] -= quantity
        return True

    def get_quantity(self, product_id: int) -> int:
        return self.products.get(product_id, 0)

    def transfer_to(self, other_inventory: 'Inventory', product_id: int, quantity: int) -> bool:
        if not self.remove_product(product_id, quantity):
            return False
        other_inventory.add_product(product_id, quantity)
        return True

class Branch:
    def __init__(self, branch_id: int, name: str, location: str):
        self.branch_id = branch_id
        self.name = name
        self.location = location
        self.inventory = Inventory()
        self.sales: List[Sale] = []

    def get_inventory_status(self, products: Dict[int, Product]) -> Dict[int, Dict]:
        status = {}
        for product_id, quantity in self.inventory.products.items():
            if product_id in products:
                product = products[product_id]
                status[product_id] = {
                    "name": product.name,
                    "quantity": quantity,
                    "price": product.price
                }
        return status

class Sale:
    def __init__(self, sale_id: int, date: datetime, branch_id: int):
        self.sale_id = sale_id
        self.date = date
        self.branch_id = branch_id
        self.items: Dict[int, int] = {}  # product_id -> quantity
        self.total_amount: float = 0.0

    def add_item(self, product_id: int, quantity: int, price: float) -> None:
        self.items[product_id] = self.items.get(product_id, 0) + quantity
        self.total_amount += price * quantity

class Shop:
    def __init__(self, name: str):
        self.name = name
        self.branches: Dict[int, Branch] = {}
        self.products: Dict[int, Product] = {}
        self.next_product_id = 1
        self.next_sale_id = 1
        self.next_branch_id = 1

    def add_branch(self, name: str, location: str) -> int:
        branch_id = self.next_branch_id
        self.next_branch_id += 1
        self.branches[branch_id] = Branch(branch_id, name, location)
        return branch_id

    def add_product(self, name: str, price: float, description: str = "") -> int:
        product_id = self.next_product_id
        self.next_product_id += 1
        self.products[product_id] = Product(product_id, name, price, description)
        return product_id

    def add_inventory_to_branch(self, branch_id: int, product_id: int, quantity: int) -> bool:
        if branch_id not in self.branches or product_id not in self.products:
            return False
        self.branches[branch_id].inventory.add_product(product_id, quantity)
        return True

    def transfer_inventory(self, from_branch_id: int, to_branch_id: int, product_id: int, quantity: int) -> bool:
        if (from_branch_id not in self.branches or 
            to_branch_id not in self.branches or 
            product_id not in self.products):
            return False
        
        from_branch = self.branches[from_branch_id]
        to_branch = self.branches[to_branch_id]
        
        return from_branch.inventory.transfer_to(to_branch.inventory, product_id, quantity)

    def process_sale(self, branch_id: int, items: Dict[int, int]) -> Optional[Sale]:
        if branch_id not in self.branches:
            return None

        branch = self.branches[branch_id]
        
        # Verify inventory availability
        for product_id, quantity in items.items():
            if product_id not in self.products:
                return None
            if branch.inventory.get_quantity(product_id) < quantity:
                return None

        # Create sale
        sale = Sale(self.next_sale_id, datetime.now(), branch_id)
        self.next_sale_id += 1

        # Process items
        for product_id, quantity in items.items():
            product = self.products[product_id]
            branch.inventory.remove_product(product_id, quantity)
            sale.add_item(product_id, quantity, product.price)

        branch.sales.append(sale)
        return sale

    def get_branch_inventory_status(self, branch_id: int) -> Optional[Dict[int, Dict]]:
        if branch_id not in self.branches:
            return None
        return self.branches[branch_id].get_inventory_status(self.products)

    def get_branch_sales_report(self, branch_id: int) -> Optional[List[Dict]]:
        if branch_id not in self.branches:
            return None
            
        report = []
        for sale in self.branches[branch_id].sales:
            sale_info = {
                "sale_id": sale.sale_id,
                "date": sale.date,
                "total_amount": sale.total_amount,
                "items": {}
            }
            for product_id, quantity in sale.items.items():
                if product_id in self.products:
                    product = self.products[product_id]
                    sale_info["items"][product.name] = {
                        "quantity": quantity,
                        "price": product.price
                    }
            report.append(sale_info)
        return report

# Example usage
if __name__ == "__main__":
    # Create a shop
    shop = Shop("My Shop")

    # Add branches
    branch1_id = shop.add_branch("Downtown Branch", "123 Main St")
    branch2_id = shop.add_branch("Uptown Branch", "456 Oak Ave")

    # Add products
    apple_id = shop.add_product("Apple", 1.50, "Fresh red apples")
    banana_id = shop.add_product("Banana", 0.75, "Yellow bananas")
    orange_id = shop.add_product("Orange", 1.25, "Sweet oranges")

    # Add inventory to branches
    shop.add_inventory_to_branch(branch1_id, apple_id, 100)
    shop.add_inventory_to_branch(branch1_id, banana_id, 150)
    shop.add_inventory_to_branch(branch1_id, orange_id, 80)

    shop.add_inventory_to_branch(branch2_id, apple_id, 50)
    shop.add_inventory_to_branch(branch2_id, banana_id, 75)
    shop.add_inventory_to_branch(branch2_id, orange_id, 40)

    # Transfer inventory between branches
    shop.transfer_inventory(branch1_id, branch2_id, apple_id, 20)

    # Process a sale at branch 1
    sale_items = {
        apple_id: 5,
        banana_id: 10,
        orange_id: 3
    }
    sale = shop.process_sale(branch1_id, sale_items)

    if sale:
        print(f"Sale completed at {shop.branches[branch1_id].name}! Total amount: ${sale.total_amount:.2f}")
    else:
        print("Sale could not be processed")

    # Get inventory status for both branches
    print("\nInventory Status by Branch:")
    for branch_id, branch in shop.branches.items():
        print(f"\n{branch.name} ({branch.location}):")
        inventory_status = shop.get_branch_inventory_status(branch_id)
        for product_id, info in inventory_status.items():
            print(f"{info['name']}: {info['quantity']} units at ${info['price']:.2f} each")

    # Get sales report for branch 1
    print("\nSales Report for Downtown Branch:")
    sales_report = shop.get_branch_sales_report(branch1_id)
    for sale_info in sales_report:
        print(f"\nSale #{sale_info['sale_id']} - {sale_info['date']}")
        print(f"Total Amount: ${sale_info['total_amount']:.2f}")
        print("Items sold:")
        for item_name, item_info in sale_info['items'].items():
            print(f"  {item_name}: {item_info['quantity']} x ${item_info['price']:.2f}")
