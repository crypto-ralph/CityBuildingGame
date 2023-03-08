import pygame


class BuildingManager:
    def __init__(self):
        self.buildings = []

    def add_building(self, building):
        self.buildings.append(building)

    def remove_building(self, building):
        self.buildings.remove(building)

    def get_income(self):
        total_income = 0
        for building in self.buildings:
            income = building.get_income()
            total_income += income
        return total_income


class GameManager:
    # Set up the income update interval
    income_update_interval = 10000  # 10 seconds

    def __init__(self, money: int = 10000):
        self.money = money
