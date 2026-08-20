class Patient:
    def __init__(
        self,
        patient_id,
        age,
        oxygen_level,
        heart_rate,
        blood_pressure,
        temperature,
        medical_conditions,
        emergency=False
    ):
        self.patient_id = patient_id
        self.age = age
        self.oxygen_level = oxygen_level
        self.heart_rate = heart_rate
        self.blood_pressure = blood_pressure
        self.temperature = temperature
        self.medical_conditions = medical_conditions
        self.emergency = emergency
        self.priority_score = 0
        self.priority = "LOW"
class ICUAllocationSystem:
    def __init__(self, icu_beds):
        self.icu_beds = icu_beds
        self.allocated_beds = {}
        self.waiting_list = []
        self.patients = {}
    def validate_patient(self, patient):
        if patient.patient_id in self.patients:
            return "Duplicate patient ID"
        if patient.oxygen_level < 0 or patient.oxygen_level > 100:
            return "Invalid oxygen level"
        if patient.heart_rate <= 0:
            return "Invalid heart rate"
        if patient.age < 0 or patient.age > 120:
            return "Invalid age"
        if patient.temperature < 25 or patient.temperature > 45:
            return "Invalid temperature"
        if patient.blood_pressure <= 0:
            return "Invalid blood pressure"
        return "Valid"
    def calculate_priority_score(self, patient):
        score = 0
        if patient.oxygen_level < 85:
            score += 40
        elif patient.oxygen_level < 90:
            score += 30
        elif patient.oxygen_level < 95:
            score += 15
        if patient.heart_rate > 130 or patient.heart_rate < 45:
            score += 25
        elif patient.heart_rate > 110 or patient.heart_rate < 55:
            score += 15
        if patient.blood_pressure < 80:
            score += 20
        elif patient.blood_pressure < 90:
            score += 10
        if patient.temperature >= 40 or patient.temperature < 35:
            score += 15
        elif patient.temperature >= 39:
            score += 10
        if patient.age >= 75:
            score += 10
        if patient.medical_conditions:
            score += 15
        if patient.emergency:
            score += 100
        patient.priority_score = score
        if score >= 70:
            patient.priority = "CRITICAL"
        elif score >= 45:
            patient.priority = "HIGH"
        elif score >= 20:
            patient.priority = "MEDIUM"
        else:
            patient.priority = "LOW"
        return patient.priority_score
    def add_patient(self, patient):
        validation = self.validate_patient(patient)
        if validation != "Valid":
            return validation
        self.calculate_priority_score(patient)
        self.patients[patient.patient_id] = patient
        return "Patient added successfully"
    def allocate_bed(self, patient_id):
        if patient_id not in self.patients:
            return "Patient not found"
        patient = self.patients[patient_id]
        if patient_id in self.allocated_beds:
            return "Patient already has an ICU bed"
        if self.icu_beds <= 0:
            if patient_id not in self.waiting_list:
                self.waiting_list.append(patient_id)
            return "No ICU bed available: Patient placed on waiting list"
        self.icu_beds -= 1
        self.allocated_beds[patient_id] = patient.priority
        return (
            f"ICU bed allocated: {patient.priority}"
        )
    def allocate_by_priority(self):
        if not self.patients:
            return "No patients available"
        sorted_patients = sorted(
            self.patients.values(),
            key=lambda p: p.priority_score,
            reverse=True
        )
        allocation_results = []
        for patient in sorted_patients:
            if self.icu_beds <= 0:
                if patient.patient_id not in self.allocated_beds:
                    if patient.patient_id not in self.waiting_list:
                        self.waiting_list.append(patient.patient_id)
                continue
            if patient.patient_id not in self.allocated_beds:
                self.icu_beds -= 1
                self.allocated_beds[
                    patient.patient_id
                ] = patient.priority
                allocation_results.append(
                    f"{patient.patient_id} -> {patient.priority}"
                )
        if allocation_results:
            return allocation_results
        return "No ICU beds available"
    def emergency_allocation(self, patient_id):
        if patient_id not in self.patients:
            return "Patient not found"
        patient = self.patients[patient_id]
        if patient_id in self.allocated_beds:
            return "Patient already has an ICU bed"
        patient.emergency = True
        self.calculate_priority_score(patient)
        if self.icu_beds > 0:
            self.icu_beds -= 1
            self.allocated_beds[
                patient.patient_id
            ] = patient.priority
            if patient.patient_id in self.waiting_list:
                self.waiting_list.remove(
                    patient.patient_id
                )
            return "Emergency ICU bed allocated"
        return "Emergency case requires immediate allocation"
    def get_waiting_list(self):
        return self.waiting_list
    def get_patient_priority(self, patient_id):
        if patient_id not in self.patients:
            return "Patient not found"
        patient = self.patients[patient_id]
        return (
            patient.priority,
            patient.priority_score
        )
if __name__ == "__main__":
    system = ICUAllocationSystem(icu_beds=2)
    patient1 = Patient(
        patient_id="P001",
        age=65,
        oxygen_level=82,
        heart_rate=135,
        blood_pressure=75,
        temperature=39.5,
        medical_conditions=True
    )
    patient2 = Patient(
        patient_id="P002",
        age=30,
        oxygen_level=98,
        heart_rate=75,
        blood_pressure=120,
        temperature=37.0,
        medical_conditions=False
    )
    print("=" * 60)
    print(" HOSPITAL ICU RESOURCE ALLOCATION SYSTEM ")
    print("=" * 60)
    print(system.add_patient(patient1))
    print(system.add_patient(patient2))
    print(
        "P001 Priority:",
        system.get_patient_priority("P001")
    )
    print(
        "P002 Priority:",
        system.get_patient_priority("P002")
    )
    print(system.allocate_by_priority())
    print("Waiting List:", system.get_waiting_list())
    print("=" * 60)