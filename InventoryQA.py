import unittest
import threading

from InventoryManagement import InventorySystem


class TestInventorySystem(unittest.TestCase):

    def setUp(self):
        self.system = InventorySystem()

        self.system.add_supplier(
            "S1",
            "Global Logistics Corp"
        )

        self.system.add_product(
            "P100",
            "Wireless Mouse",
            reorder_threshold=5,
            supplier_id="S1"
        )

    def test_stock_availability(self):
        self.system.add_stock(
            "Warehouse A",
            "P100",
            10
        )

        success, message = self.system.fulfill_order(
            "P100",
            4
        )

        self.assertTrue(success)
        self.assertIn(
            "Fulfilled by Warehouse A",
            message
        )

    def test_insufficient_inventory(self):
        self.system.add_stock(
            "Warehouse A",
            "P100",
            3
        )

        success, message = self.system.fulfill_order(
            "P100",
            5
        )

        self.assertFalse(success)
        self.assertEqual(
            message,
            "Insufficient inventory"
        )

    def test_warehouse_transfer(self):
        self.system.add_stock(
            "Warehouse A",
            "P100",
            10
        )

        self.system.transfer_stock(
            "Warehouse A",
            "Warehouse B",
            "P100",
            4
        )

        self.assertEqual(
            self.system.warehouses[
                "Warehouse A"
            ].inventory["P100"],
            6
        )

        self.assertEqual(
            self.system.warehouses[
                "Warehouse B"
            ].inventory["P100"],
            4
        )

    def test_concurrent_orders(self):
        self.system.add_stock(
            "Warehouse A",
            "P100",
            10
        )

        def place_single_order():
            self.system.fulfill_order(
                "P100",
                1
            )

        threads = [
            threading.Thread(
                target=place_single_order
            )
            for _ in range(12)
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        total_stock = sum(
            wh.inventory.get("P100", 0)
            for wh in self.system.warehouses.values()
        )

        self.assertEqual(
            total_stock,
            0
        )

    def test_reorder_threshold(self):
        self.system.add_stock(
            "Warehouse A",
            "P100",
            6
        )

        success, message = self.system.fulfill_order(
            "P100",
            3
        )

        self.assertTrue(success)

        self.assertIn(
            "Low stock alert: Reorder triggered with Supplier Global Logistics Corp",
            message
        )

    def test_invalid_product(self):
        success, message = self.system.fulfill_order(
            "INVALID_ID",
            1
        )

        self.assertFalse(success)

        self.assertEqual(
            message,
            "Invalid product"
        )

    def test_negative_inventory(self):
        self.system.add_stock(
            "Warehouse A",
            "P100",
            5
        )

        with self.assertRaises(ValueError):
            self.system.warehouses[
                "Warehouse A"
            ].remove_stock(
                "P100",
                10
            )

    def test_multiple_warehouses(self):
        self.system.add_stock(
            "Warehouse A",
            "P100",
            2
        )

        self.system.add_stock(
            "Warehouse B",
            "P100",
            10
        )

        success, message = self.system.fulfill_order(
            "P100",
            5
        )

        self.assertTrue(success)

        self.assertIn(
            "Fulfilled by Warehouse B",
            message
        )
if __name__ == "__main__":
    unittest.main()