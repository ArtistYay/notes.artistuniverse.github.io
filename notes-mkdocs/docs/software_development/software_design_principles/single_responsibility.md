## Overview

The reason for single responsibility is having a centralized place to change code. Your class or module must not contain multiple tasks or jobs. It's a way to have clean code.

## Best Practices

* Segregate the software into concentric layers, with clear, unyielding dependency rules.
* Identify responsibilities, ask “What is this class supposed to do?”
* Use descriptive names for classes and methods to reflect their single purpose (e.g., EmailService instead of NotificationManager).

!!! youtube "Single Responsibility Principle (SRP)"
	<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/UQqY3_6Epbg?si=AMBY3xzrXv-q9YyO" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Real-world scenario

Got this example from [Geeks for Geeks](https://www.geeksforgeeks.org/system-design/solid-principle-in-programming-understand-with-real-life-examples/#:~:text=1%2E%20Single%20Responsibility%20Principle)

``` py linenums="1"
# Class for baking bread
class BreadBaker:
    def bakeBread(self):
        print("Baking high-quality bread...")

# Class for managing inventory
class InventoryManager:
    def manageInventory(self):
        print("Managing inventory...")

# Class for ordering supplies
class SupplyOrder:
    def orderSupplies(self):
        print("Ordering supplies...")

# Class for serving customers
class CustomerService:
    def serveCustomer(self):
        print("Serving customers...")

# Class for cleaning the bakery
class BakeryCleaner:
    def cleanBakery(self):
        print("Cleaning the bakery...")

def main():
    baker = BreadBaker()
    inventoryManager = InventoryManager()
    supplyOrder = SupplyOrder()
    customerService = CustomerService()
    cleaner = BakeryCleaner()

    # Each class focuses on its specific responsibility
    baker.bakeBread()
    inventoryManager.manageInventory()
    supplyOrder.orderSupplies()
    customerService.serveCustomer()
    cleaner.cleanBakery()

if __name__ == "__main__":
    main()
```

[The Single Responsibility Principle (SRP): A view of SRP at different levels of architecture](https://medium.com/@gabrieldos540/the-single-responsibility-principle-srp-far-beyond-one-reason-to-change-816b366405b4)