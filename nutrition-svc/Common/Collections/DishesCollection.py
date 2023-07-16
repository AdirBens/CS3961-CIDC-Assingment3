from Utils.DataBase import DataBase


class DishesCollection(DataBase):
    """
    A Collection of Dishes.
    Stores all dishes Resources and provides encapsulation and interface to handle dish Resources.
    > An extension to DataBase class.
    [!] This is a singleton class, which can be shared among relevant classes
    """
    _instance = None

    def __init__(self):
        super().__init__()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DishesCollection, cls).__new__(cls)
        return cls._instance
