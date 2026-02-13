# 1. Создаем словарь букв и очков
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
points = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 4, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]

letter_to_points = {letter: point for letter, point in zip(letters, points)}

# 2. Добавляем счетчик
letter_to_points[" "] = 0

# 3-5. Функция подсчета очков слова
def score_word(word):
    point_total = 0
    for letter in word.upper():
        point_total += letter_to_points.get(letter, 0)
    return point_total

# 6. Тестирование функции
print(f"Слово 'BROWNIE' стоит: {score_word('BROWNIE')} очков")
print(f"Слово 'python' стоит: {score_word('python')} очков")

# 7. Создаем словарь игроков и их слов
player_to_words = {
    "player1": ["BLUE", "TENNIS", "EXIT"],
    "wordNerd": ["EARTH", "EYES", "MACHINE"],
    "Lexi Con": ["ERASER", "BELLY", "HUSKY"],
    "Prof Reader": ["ZAP", "COMA", "PERIOD"]
}

# 8. Создаем пустой словарь для очков игроков
player_to_points = {}

# 9-11. Подсчет очков для каждого игрока
for player, words in player_to_words.items():
    player_points = 0
    for word in words:
        player_points += score_word(word)
    player_to_points[player] = player_points

# 12. Выводим результаты
print("\n--- Текущее положение в игре ---")
for player, points in player_to_points.items():
    print(f"{player}: {points} очков")

# ДОП задание

# 1. Функция добавления слова игроку
def play_word(player, word):
    if player in player_to_words:
        player_to_words[player].append(word)
    else:
        player_to_words[player] = [word]
    update_point_totals()  # Обновляем очки после добавления слова

# 2. Функция обновления всех очков
def update_point_totals():
    global player_to_points
    player_to_points = {}
    for player, words in player_to_words.items():
        player_points = 0
        for word in words:
            player_points += score_word(word)
        player_to_points[player] = player_points

# 3. Демонстрация дополнительных функций
print("\n--- Демонстрация дополнительных функций ---")

# Добавляем новое слово игроку
play_word("player1", "PYTHON")
print(f"После добавления слова 'PYTHON' player1:")
print(f"Слова player1: {player_to_words['player1']}")
print(f"Очки player1: {player_to_points['player1']}")

# Добавляем нового игрока
play_word("New Player", "CODE")
print(f"\nНовый игрок 'New Player':")
print(f"Слова: {player_to_words['New Player']}")
print(f"Очки: {player_to_points['New Player']}")

# Финальная таблица
print("\n--- Финальное положение в игре ---")
for player, points in sorted(player_to_points.items(), key=lambda x: x[1], reverse=True):
    print(f"{player}: {points} очков - слова: {player_to_words[player]}")