# Tip meal calculator

def mealCost(meal):
 tax = 6.75 / 100
 tip = 15.0 / 100
 meal = meal + meal * tax
 total = meal + meal * tip
  return print("%.1f" % total)

mealCost(meal)