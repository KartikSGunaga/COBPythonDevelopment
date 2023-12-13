class Employee:
    def __init__(self, name, position, salary, empID, mail):
        self.name = name
        self.position = position
        self.salary = salary
        self.empID = empID
        self.mailID = mail


class employeeRecord:
    def __init__(self):
        self.record = []

    def addEmployee(self, employee):
        self.record.append(employee)
        print("\nEmplyee details stored successfully!")

    def updateEmployee(self, name, updatedName, updatedPosition, updatedSalary, updatedEmpID, updatedMail):
        flag = False
        for employee in self.record:
            if name == employee.name.lower():
                employee.name = updatedName
                employee.position = updatedPosition
                employee.salary = updatedSalary
                employee.mailID = updatedMail
                employee.empID = updatedEmpID

                flag = True

        if not flag:
            print("\nEmployee doesn't exist.")
            add = input("\nAdd updated details to records?(yes or no): ").lower()

            if add == "yes":
                empRecord = employeeRecord()
                newEmployee = Employee(updatedName, updatedPosition, updatedSalary, updatedEmpID, updatedMail)

                empRecord.addEmployee(newEmployee)
                print("\nEmployee details stored successfully!")

    def searchEmployeeByName(self):
        name = input("\nEnter the employee's name: ").lower()

        found_employees = [employee for employee in self.record if employee.name.lower() == name]

        if found_employees:
            print("\nEmployee details are as follows:")
            for employee in found_employees:
                print(f"Name: {employee.name}")
                print(f"Position: {employee.position}")
                print(f"Salary: {employee.salary}")
                print(f"Employee ID: {employee.empID}")
                print(f"Email ID: {employee.mailID}")
        else:
            print("\nEmployee doesn't exist with that name.")

    def searchEmployeeByEmpID(self):
        empID = input("\nEnter the employee's name: ")

        found_employees = [employee for employee in self.record if employee.empID == empID]

        if found_employees:
            print("\nEmployee details are as follows:")
            for employee in found_employees:
                print(f"Name: {employee.name}")
                print(f"Position: {employee.position}")
                print(f"Salary: {employee.salary}")
                print(f"Employee ID: {employee.empID}")
                print(f"Email ID: {employee.mailID}")
        else:
            print("\nEmployee doesn't exist with that ID.")

    def searchEmployeeByPosition(self):
        position = input("\nenter the employee's position: ").lower()

        found_employees = [employee for employee in self.record if employee.position.lower() == position]

        if found_employees:
            print("\nEmployee details are as follows:")
            for employee in found_employees:
                print(f"Name: {employee.name}")
                print(f"Position: {employee.position}")
                print(f"Salary: {employee.salary}")
                print(f"Employee ID: {employee.empID}")
                print(f"Email ID: {employee.mailID}")
        else:
            print("\nEmployee doesn't exist in that position.")

    def searchEmployeeBySalaryRange(self):
        minSalary = int(input("\nEnter the employee's minimum salary: "))
        maxSalary = int(input("\nEnter the employee's maximum salary: "))

        found_employees = [employee for employee in self.record if employee.salary in range(minSalary, maxSalary + 1)]

        if found_employees:
            print("\nEmployee details are as follows:")
            for employee in found_employees:
                print(f"Name: {employee.name}")
                print(f"Position: {employee.position}")
                print(f"Salary: {employee.salary}")
                print(f"Employee ID: {employee.empID}")
                print(f"Email ID: {employee.mailID}")
        else:
            print("\nEmployee doesn't exist in that salary range.")

    def deleteEmployee(self, empID, name):
        flag = False
        for employee in self.record:
            if empID == employee.empID:
                self.record = [employees for employees in self.record if employee.empID is not empID]
                flag = True
                print("\nEmployee details deleted successfully!")
                break

            elif name == employee.name.lower():
                self.record = [employees for employees in self.record if employee.name is not name]
                flag = True
                print("\nEmployee details deleted successfully!")
                break

        if flag is not True:
            print("\nNeither that name nor that ID exists in the record.")


def menu():
    print("\n Menu \n"
          "1. View Menu \n"
          "2. Add employee \n"
          "3. Update employee \n"
          "4. Search employee by name \n"
          "5. Search employee by Employee ID \n"
          "6. Search employee by Position \n"
          "7. Search employee by salary range \n"
          "8. Delete Employee \n"
          "9. Exit")


def createEmployee():
    record = employeeRecord()

    name = input("\nEnter the employee's name: ")
    position = input("\nEnter the employee's position: ")
    salary = int(input("\nEnter the employee's salary: "))
    empID = int(input("\nEnter the employee's ID number: "))
    mailID = input("\nEnter the employee's name: ")

    employee = Employee(name, position, salary, empID, mailID)
    record.addEmployee(employee)
    print(f"\nEmployee-{empID} added successfully!")


def main():
    print("\nWelcome to Employee Records!")
    record = employeeRecord()

    while True:
        choice = int(input("\nEnter your choice(1-9): "))

        if choice == 1:
            menu()

        elif choice == 2:
            createEmployee()

        elif choice == 3:
            name = input("\nEnter the name of employee: ")
            updatedName = input("\nEnter the new name of employee: ")
            updatedPosition = input("\nEnter the new position of employee: ")
            updatedSalary = input("\nEnter the new salary of employee: ")
            updatedEmpID = input("\nEnter the new employee ID of employee: ")
            updatedMailID = input("\nEnter the new mail-ID of employee: ")

            record.updateEmployee(name, updatedName, updatedPosition, updatedSalary, updatedEmpID, updatedMailID)

        elif choice == 4:
            record.searchEmployeeByName()

        elif choice == 5:
            record.searchEmployeeByEmpID()

        elif choice == 6:
            record.searchEmployeeByPosition()

        elif choice == 7:
            record.searchEmployeeBySalaryRange()

        elif choice == 8:
            name = input("\nEnter the name of employee: ")
            empID = input("\nEnter the ID of employee: ")

            record.deleteEmployee(name, empID)

        elif choice == 9:
            print("\nThank you for using our Employee Records!")
            break

        else:
            print("\nInvalid choice. Please input integer between(1 - 9)")


if __name__ == "__main__":
    main()