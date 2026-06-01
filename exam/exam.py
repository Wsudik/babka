from abc import ABC, abstractmethod
from typing import Dict, Optional

# ==========================================
# ООП-ЗАВДАННЯ
# ==========================================

# 1. Абстрактний клас Dish
class Dish(ABC):
    def __init__(self, name: str, cooking_time_min: int):
        self.name = name
        self.cooking_time_min = cooking_time_min

    @abstractmethod
    def get_nutrition(self) -> dict:
        pass

# 2. Класи VeganDish та MeatDish що успадковують Dish
class VeganDish(Dish):
    def __init__(self, name: str, cooking_time_min: int, calories: int):
        super().__init__(name, cooking_time_min)
        self.calories = calories

    def get_nutrition(self) -> dict:
        return {"calories": self.calories, "type": "vegan"}


class MeatDish(Dish):
    def __init__(self, name: str, cooking_time_min: int, calories: int, protein_g: float):
        super().__init__(name, cooking_time_min)
        self.calories = calories
        self.protein_g = protein_g

    def get_nutrition(self) -> dict:
        return {"calories": self.calories, "protein_g": self.protein_g, "type": "meat"}

# 3. Клас CookBook
class CookBook:
    def __init__(self):
        # Приватний словник (інкапсуляція)
        self.__recipes: Dict[str, Dish] = {}

    def add(self, dish: Dish):
        # Зберігаємо ключі в нижньому регістрі для зручного пошуку
        self.__recipes[dish.name.lower()] = dish

    def find(self, name: str) -> Optional[Dish]:
        return self.__recipes.get(name.lower())

    def list_all(self):
        """Демонстрація поліморфізму через виклик get_nutrition()"""
        all_info = {}
        for name, dish in self.__recipes.items():
            # Метод get_nutrition() поводиться по-різному залежно від типу об'єкта
            all_info[dish.name] = dish.get_nutrition()
        return all_info

# ==========================================
# AI-АГЕНТ
# ==========================================

# Інструмент (tool)
def get_recipe_info(dish_name: str) -> dict:
    cookbook = CookBook()
    # Наповнюємо заздалегідь визначеними стравами
    cookbook.add(VeganDish("Овочеве рагу", 45, 320))
    cookbook.add(MeatDish("Стейк з яловичини", 20, 650, 55.0))
    cookbook.add(VeganDish("Тофу-салат", 10, 210))

    dish = cookbook.find(dish_name)
    
    if dish:
        # Отримуємо харчову цінність і додаємо час приготування
        info = dish.get_nutrition()
        info["cooking_time_min"] = dish.cooking_time_min
        info["found"] = True
        return info
    else:
        return {"found": False}

# Демонстрація роботи інструменту
if __name__ == "__main__":
    print(get_recipe_info("Стейк з яловичини")) 
    # {'calories': 650, 'protein_g': 55.0, 'type': 'meat', 'cooking_time_min': 20, 'found': True}
    
    print(get_recipe_info("Тофу-салат"))
    # {'calories': 210, 'type': 'vegan', 'cooking_time_min': 10, 'found': True}
    
    print(get_recipe_info("Борщ"))
    # {'found': False}