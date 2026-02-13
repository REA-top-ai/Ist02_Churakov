#1
board_games = ["Settlers of Catan", "Carcassone", "Power Grid", "Argicola", "Scrabble"]
sport_games = ["football", "foorball - American", "hockey", "baseball", "cricket"]
for game in board_games:
    print(game)
for game in sport_games:
    print(game)

#2
promise = "I will not chew gum in class"
for i in range(5):
    print(promise)

#3
student_period_A = ["Alex", "Briana", "Cheri", "Daniele"]
student_period_B = ["Dora", "Minerva", "Alexa", "Obie"]
for student in student_period_A:
    student_period_B.append(student)
print(student_period_B)

#4
dog_breeds_available_for_adoption = ['french_bulldog', 'dalmation', 'shihtzu', 'poodle', 'collie']
dog_breed_I_want = 'dalmation'
for dog in dog_breeds_available_for_adoption:
        print(dog)
        if dog == dog_breed_I_want:
            print("У них есть собака, которую я хочу")
            break
#5
sales_data = [[12, 17, 22], [2, 10, 3], [5, 12, 13]]
scoops_sold = 0
for shop in sales_data:
    for scoop in shop:
        scoops_sold+=scoop
print(scoops_sold)

#6
single_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
squares = []
for digit in single_digits:
    squares.append(digit**2)
    print(digit)
cubes = [digit**3 for digit in single_digits]
print(squares)
print(cubes)