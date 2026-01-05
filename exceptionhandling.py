class AgeError(Exception):
    pass
try:
    age = int(input("Enter your age: "))
    if age < 18:
        raise AgeError
except AgeError:
    print("Your age is : ")