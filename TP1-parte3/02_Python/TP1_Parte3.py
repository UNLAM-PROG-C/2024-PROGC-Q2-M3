import threading
import time
import random

class Bathroom:
    def __init__(self):
        self.max_capacity = 3  # Maximum bathroom capacity
        self.current_in_bathroom = 0  # Current number of people in the bathroom
        self.current_gender = None  # Gender of the people in the bathroom (None, 'Man', 'Woman')
        self.lock = threading.Lock()  # Protects concurrent access to current_gender and current_in_bathroom
        self.sem = threading.Semaphore(self.max_capacity)  # Controls the bathroom capacity

    def enter_bathroom(self, gender):
        with self.lock:
            # If the bathroom is empty, the allowed gender can be changed
            if self.current_in_bathroom == 0:
                self.current_gender = gender
                print(f"The bathroom is now for {gender}s")
            elif self.current_gender != gender:
                print(f"{gender} waiting because the bathroom is occupied by {self.current_gender}s")
                return False

        # Try to enter the bathroom
        self.sem.acquire()

        with self.lock:
            self.current_in_bathroom += 1
            print(f"{gender} has entered the bathroom ({self.current_in_bathroom}/{self.max_capacity})")
        return True

    def leave_bathroom(self, gender):
        time.sleep(random.uniform(0.5, 2))  # Simulate time in the bathroom

        with self.lock:
            self.current_in_bathroom -= 1
            print(f"{gender} has left the bathroom ({self.current_in_bathroom}/{self.max_capacity})")

            if self.current_in_bathroom == 0:
                print(f"The bathroom is empty")
                self.current_gender = None

        # Release the semaphore so others can enter
        self.sem.release()


# Function to simulate employees trying to use the bathroom
def employee(bathroom, gender):
    for _ in range(5):
        if bathroom.enter_bathroom(gender):
            bathroom.leave_bathroom(gender)
        time.sleep(random.uniform(0.1, 1))  # Simulate time outside the bathroom


def main():
    bathroom = Bathroom()
    # Create male and female employees
    employees = []
    for i in range(5):  # 5 men
        male_employee = threading.Thread(target=employee, args=(bathroom, "Man"))
        employees.append(male_employee)

    for i in range(5):  # 5 women
        female_employee = threading.Thread(target=employee, args=(bathroom, "Woman"))
        employees.append(female_employee)

    # Start all threads
    for e in employees:
        e.start()
    # Keep the program running
    for e in employees:
        e.join()

if __name__ == "__main__":
    main()