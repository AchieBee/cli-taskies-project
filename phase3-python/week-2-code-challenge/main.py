class Customer:
    customers = []

    def __init__(self,given_name,family_name,full_name):
        self.given_name = given_name
        self.family_name = family_name
        self.full_name = full_name

    def given_name(self):
        print(self.given_name)

    def family_name(self):
        print(self.family_name )    

    def full_name(self):
        print(f"{self.given_name} {self.family_name}")     

class Restaurant:
    def __init__(self,name):
        self.name = name


class Review:
    reviews = []

    def __init__(self,customer,restaurant,rating):
        self.customer = customer
        self.restaurant = restaurant
        self.rating = rating 



cust1 = Customer("jane", "wilson", "jane wilson")
print(cust1.full_name)
rest1 = Restaurant("annex")
print(rest1.name)
rev1 = Review(cust1, rest1, "top notch customer service")
print(rev1.rating)


