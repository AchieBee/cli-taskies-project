from Review import Review

class Restaurant(Review):
    def __init__(self,name):
        self._name = name
    def name(self):
        return self._name
    def reviews(self):
        reviews_list = super().all_reviews
        restaurant_review = []
        for review in reviews_list:
            if review['Restaurant'] == self._name:
                restaurant_review.append(review)
        return restaurant_review
    def customers(self):
        reviews_list = super().all_reviews
        customer_list = []
        for review in reviews_list:
            if review['Restaurant'] == self._name:
                customer_list.append(review['Customer'])
        return customer_list
    def average_star_rating(self):
        reviews_list = super().all_reviews
        total_rating = 0
        rating_list =[]
        for review in reviews_list:
            if review['Restaurant'] == self._name:
                total_rating += review['Rating']
                rating_list.append(review['Rating'])
        average = total_rating/len(rating_list)
        return average

Annex = Restaurant(Review)        