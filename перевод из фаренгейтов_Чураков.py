# Задача 1: Перевод Фаренгейта в Цельсий и обратно

# 1. Функция для перевода Фаренгейта в Цельсий
def f_to_c(f_temp):
    c_temp = (f_temp - 32) * 5/9
    return c_temp

# 2. Проверка функции для 100°F
f100_in_celsius = f_to_c(100)
print(f"100°F = {f100_in_celsius}°C")

# 3. Функция для перевода Цельсия в Фаренгейт
def c_to_f(c_temp):
    f_temp = c_temp * (9/5) + 32
    return f_temp

# 4. Проверка функции для 0°C
c0_in_fahrenheit = c_to_f(0)
print(f"0°C = {c0_in_fahrenheit}°F")

print("\n" + "="*50 + "\n")

# Задача 2: Физические расчеты

# 1. Функция для расчета силы
def get_force(mass, acceleration):
    return mass * acceleration

# 2. Тестирование функции с переменными train_mass и train_acceleration
train_mass = 10000  # масса поезда в кг
train_acceleration = 5  # ускорение в м/с²
train_force = get_force(train_mass, train_acceleration)

# 3. Вывод результата
print(f"Поезд GE поставляет {train_force} ньютонов силы")

# 4. Функция для расчета энергии
def get_energy(mass, c=3*10**8):
    return mass * c**2

# Тестирование функции get_energy
train_energy = get_energy(train_mass)
print(f"Энергия поезда: {train_energy} джоулей")
