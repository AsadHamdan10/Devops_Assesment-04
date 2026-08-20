class RideBooking:
    def __init__(
        self,
        customer_id,
        pickup_location,
        drop_location,
        distance,
        passengers,
        vehicle_type,
        booking_time,
        driver_available=True
    ):
        self.customer_id = customer_id
        self.pickup_location = pickup_location
        self.drop_location = drop_location
        self.distance = distance
        self.passengers = passengers
        self.vehicle_type = vehicle_type
        self.booking_time = booking_time
        self.driver_available = driver_available
    def calculate_fare(self):
        if self.distance <= 0:
            return "Invalid booking: Zero or negative distance"
        if self.passengers <= 0:
            return "Invalid booking: Invalid passenger count"
        if self.passengers > 6:
            return "Invalid booking: Maximum passenger limit exceeded"
        if not self.driver_available:
            return "Invalid booking: Driver unavailable"
        if self.vehicle_type == "Bike":
            base_fare = 30
            distance_rate = 10
        elif self.vehicle_type == "Sedan":
            base_fare = 60
            distance_rate = 15
        elif self.vehicle_type == "SUV":
            base_fare = 100
            distance_rate = 20
        elif self.vehicle_type == "Premium":
            base_fare = 150
            distance_rate = 30
        else:
            return "Invalid booking: Invalid vehicle type"
        distance_fare = self.distance * distance_rate
        peak_surcharge = 0
        if self.booking_time in [
            "08:00",
            "09:00",
            "18:00",
            "19:00",
            "20:00"
        ]:
            peak_surcharge = 50
        hour = int(self.booking_time.split(":")[0])
        night_surcharge = 0
        if hour >= 22 or hour < 6:
            night_surcharge = 40
        passenger_surcharge = 0
        if self.passengers > 4:
            passenger_surcharge = 50
        promotional_discount = 0
        if self.distance >= 20:
            promotional_discount = 50
        final_fare = (
            base_fare
            + distance_fare
            + peak_surcharge
            + night_surcharge
            + passenger_surcharge
            - promotional_discount
        )
        return final_fare
    def allocate_driver(self):
        if not self.driver_available:
            return "Driver allocation failed: Driver unavailable"
        return "Driver allocated successfully"
if __name__ == "__main__":
    booking = RideBooking(
        customer_id="C001",
        pickup_location="VIT Vellore",
        drop_location="Katpadi",
        distance=10,
        passengers=2,
        vehicle_type="Sedan",
        booking_time="10:00",
        driver_available=True
    )
    print("=" * 60)
    print("RIDE BOOKING SYSTEM")
    print("=" * 60)
    print("Customer ID:", booking.customer_id)
    print("Pickup Location:", booking.pickup_location)
    print("Drop Location:", booking.drop_location)
    print("Distance:", booking.distance)
    print("Passengers:", booking.passengers)
    print("Vehicle Type:", booking.vehicle_type)
    print("Booking Time:", booking.booking_time)
    fare = booking.calculate_fare()
    print("Final Fare:", fare)
    print("Driver Status:", booking.allocate_driver())
    print("=" * 60)