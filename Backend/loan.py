""" A fuction that checks for loan eligibility """

def check_status(age, gender, name):
    """ Gets input for age and gender """
    if age is not None and gender is not None:
        if age.isdigit():
            comfirmed_age = int(age)
        else:
            print("*** please input a valid number for age ***")
            return
        if gender.isdigit():
            print(f"***{gender} is not a valid gender ***")
            return
        if comfirmed_age > 70 and gender == "female":
            print(f"**** {name} Your age: {age} and gender: {gender} qualifies you for this loan ****")
        else:
            print(f"**** {name} Sorry only the female gender above 70 years can apply for this loan ****")

if __name__ == '__main__':
    """ Initiate the stdin to receive user input """
    username = input("Enter name pls: ")
    if username is not None:
        name = username.capitalize()
    age = input("please input your age: ")
    gender = input("please input your gender: ")
    # call the check_status function
    check_status(age, gender, name)