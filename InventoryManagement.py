import threading
from typing import Dict, List, Optional, Tuple


class Product:
    def __init__(
        self,
        product_id: str,
        name: str,
        reorder_threshold: int
    ):
        self.product_id = product_id
        self.name = name
        self.reorder_threshold = reorder_threshold


class Supplier:
    def __init__(
        self,
        supplier_id: str,
        name: str
    ):
        self.supplier_id = supplier_id
        self.name = name
        self.managed_products: List[str] = []


class Warehouse:
    def __init__(self, name: str):
        self.name = name
        self.inventory: Dict[str, int] = {}

    def add_stock(
        self,
        product_id: str,
        qty: int
    ):
        if qty < 0:
            raise ValueError("Quantity cannot be negative")

        self.inventory[product_id] = (
            self.inventory.get(product_id, 0) + qty
        )

    def remove_stock(
        self,
        product_id: str,
        qty: int
    ):
        if qty < 0:
            raise ValueError("Quantity cannot be negative")

        current_qty = self.inventory.get(product_id, 0)

        if current_qty < qty:
            raise ValueError(
                "Insufficient inventory: stock cannot be negative"
            )

        self.inventory[product_id] = current_qty - qty


class InventorySystem:

    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.suppliers: Dict[str, Supplier] = {}

        self.warehouses: Dict[str, Warehouse] = {
            "Warehouse A": Warehouse("Warehouse A"),
            "Warehouse B": Warehouse("Warehouse B"),
            "Warehouse C": Warehouse("Warehouse C")
        }

        self.product_supplier_map: Dict[str, str] = {}

        self.lock = threading.Lock()

    def add_product(
        self,
        product_id: str,
        name: str,
        reorder_threshold: int,
        supplier_id: Optional[str] = None
    ):
        with self.lock:
            self.products[product_id] = Product(
                product_id,
                name,
                reorder_threshold
            )

            if supplier_id and supplier_id in self.suppliers:
                self.product_supplier_map[product_id] = supplier_id

                if product_id not in self.suppliers[
                    supplier_id
                ].managed_products:
                    self.suppliers[
                        supplier_id
                    ].managed_products.append(product_id)

    def remove_product(self, product_id: str):
        with self.lock:

            if product_id in self.products:
                del self.products[product_id]

            if product_id in self.product_supplier_map:
                supp_id = self.product_supplier_map[product_id]

                if (
                    supp_id in self.suppliers
                    and product_id in
                    self.suppliers[supp_id].managed_products
                ):
                    self.suppliers[
                        supp_id
                    ].managed_products.remove(product_id)

                del self.product_supplier_map[product_id]

            for warehouse in self.warehouses.values():
                if product_id in warehouse.inventory:
                    del warehouse.inventory[product_id]

    def add_supplier(
        self,
        supplier_id: str,
        name: str
    ):
        with self.lock:
            self.suppliers[supplier_id] = Supplier(
                supplier_id,
                name
            )

    def add_stock(
        self,
        warehouse_name: str,
        product_id: str,
        qty: int
    ):
        with self.lock:

            if product_id not in self.products:
                raise ValueError("Invalid product")

            if warehouse_name not in self.warehouses:
                raise ValueError("Invalid warehouse")

            self.warehouses[
                warehouse_name
            ].add_stock(product_id, qty)

    def transfer_stock(
        self,
        from_warehouse: str,
        to_warehouse: str,
        product_id: str,
        qty: int
    ):
        with self.lock:

            if (
                from_warehouse not in self.warehouses
                or to_warehouse not in self.warehouses
            ):
                raise ValueError("Invalid warehouse choice")

            if product_id not in self.products:
                raise ValueError("Invalid product")

            self.warehouses[
                from_warehouse
            ].remove_stock(product_id, qty)

            self.warehouses[
                to_warehouse
            ].add_stock(product_id, qty)

    def detect_low_stock(
        self,
        product_id: str
    ) -> bool:

        if product_id not in self.products:
            raise ValueError("Invalid product")

        total_stock = sum(
            wh.inventory.get(product_id, 0)
            for wh in self.warehouses.values()
        )

        return (
            total_stock
            < self.products[product_id].reorder_threshold
        )

    def trigger_reorder(
        self,
        product_id: str
    ) -> str:

        supplier_id = self.product_supplier_map.get(
            product_id
        )

        if (
            supplier_id
            and supplier_id in self.suppliers
        ):
            return (
                f"Reorder triggered with Supplier "
                f"{self.suppliers[supplier_id].name}"
            )

        return "Reorder triggered (No supplier assigned)"

    def select_warehouse_for_order(
        self,
        product_id: str,
        qty: int
    ) -> Optional[str]:

        # Search warehouses in priority order: A -> B -> C
        for wh_name in [
            "Warehouse A",
            "Warehouse B",
            "Warehouse C"
        ]:
            if (
                self.warehouses[
                    wh_name
                ].inventory.get(product_id, 0)
                >= qty
            ):
                return wh_name

        return None

    def fulfill_order(
        self,
        product_id: str,
        qty: int
    ) -> Tuple[bool, str]:

        with self.lock:

            if product_id not in self.products:
                return False, "Invalid product"

            warehouse_name = (
                self.select_warehouse_for_order(
                    product_id,
                    qty
                )
            )

            if not warehouse_name:
                return False, "Insufficient inventory"

            self.warehouses[
                warehouse_name
            ].remove_stock(product_id, qty)

            status_msg = (
                f"Fulfilled by {warehouse_name}"
            )

            if self.detect_low_stock(product_id):
                reorder_msg = self.trigger_reorder(
                    product_id
                )

                status_msg += (
                    f" | Low stock alert: {reorder_msg}"
                )

            return True, status_msg