from Resources.Dish import Dish
from Resources.Dishes import Dishes
from Resources.Meal import Meal
from Resources.Meals import Meals


def load_resources(api):
    api.add_resource(Meals, '/meals')
    api.add_resource(Meal, '/meals/<int:id>', '/meals/<string:name>')
    api.add_resource(Dishes, '/dishes')
    api.add_resource(Dish, '/dishes/<int:dish_id>', '/dishes/<string:dish_name>')
