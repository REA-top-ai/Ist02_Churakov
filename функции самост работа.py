#1
def f_to_c(f_temp):
    c_temp = (f_temp - 32) * 5/9
    return c_temp
f100_in_celsius = f_to_c(100)
print(f100_in_celsius)
def c_to_f(c_temp):
    f_temp = c_temp * 9/5 + 32
    return f_temp
c0_in_fahrenheit = c_to_f(0)
print(c0_in_fahrenheit)


#2
def get_force(train_mass, train_acceleration):
    force = train_mass * train_acceleration
    return force
train_force = get_force(22680,10)
print(f"Поезд GE поставляет {train_force} ньютонов силы")
def get_energy(bomb_mass, c=3*10**8):
    energy=bomb_mass * c**2
    return energy
bomb_energy = get_energy(1)
print(f"1 кг бомбы составляет {bomb_energy} Джоулей")
def get_work(train_mass, train_acceleration, train_distance):
    work = train_force * train_distance
    return work
train_work = get_work(22680, 10, 100)
train_distance = 100
print(train_work)
print(f"Поезд выполняет {train_work} Джоулей за {train_distance} метров")

#3
clothes = "домашняя одежда"
def better_clothes(time):
    sentance = f"{time} лучше всего подходит {clothes}"
    print(sentance)
print("У меня большой гардероб")
better_clothes("Утром")
better_clothes("Днем")
better_clothes("Вечером")
better_clothes("Ночью")
print("Мои предпочтения")
meal = "шоколад"
def better_meal(intake):
    sentance = f"На {intake} лучше всего подходит {meal}"
    print(sentance)
better_meal("завтрак")
better_meal("обед")
better_meal("ужин")


#4
def user_check_1(user_name):
    if user_name == "Дмитрий":
        print("Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!")
    else:
        print("Добро пожаловать!")
user_check_1("Дмитрий")
user_check_1("Ангелина")

def user_check_2(user_name, arm):
    if user_name == "Дмитрий" and arm==1 or user_name == "Ангелина" and arm==2 \
            or user_name == "Василий" and arm==3 \
            or user_name == "Екатерина" and arm==4:
        print("Добро пожаловать!")
    elif user_name == "Дмитрий" and arm!= 1:
        print("Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!")
    else:
        print("Логин или пароль не верный, попробуйте еще раз")
user_check_2("Дмитрий", 1)
user_check_2("Дмитрий", 2)
user_check_2("Ангелина", 2)
user_check_2("Екатерина", 2)


#5
def grade(middle_mark):
    if middle_mark >= 4.0:
        print("A")
    elif middle_mark >= 3.0:
        print("B")
    elif middle_mark >= 2.0:
        print("C")
    elif middle_mark >= 1.0:
        print("D")
    elif middle_mark >= 0.0:
        print("F")
grade(3.1)