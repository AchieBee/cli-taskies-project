class Customer:
    customers = []

    def __init__(self,given_name,family_name):
        self.given_name = given_name
        self.family_name = family_name

class Restaurant:
    def __init__(self,name):
        self.name = name


class Review:
    reviews = []

    def __init__(self,customer,restaurant,rating):
        self.customer = customer
        self.restaurant = restaurant
        self.rating = rating        


