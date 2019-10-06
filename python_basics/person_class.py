# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 15:29:54 2019

@author: admin
"""

class Person:
    population = 0
    def __init__(self, myAge):
        self.age = myAge
        Person.population += 1
    def get_population(self):
        return Person.population
    def get_age(self):
        return self.age
