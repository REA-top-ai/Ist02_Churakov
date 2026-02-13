correct_answers = (1, 2, 3, 2, 1, 2, 1, 3, 1, 2, 1, 2, 3, 3, 2, 1, 2, 1, 2, 1)
user_answers = []
for i in range(20):
    answer = int(input(f"Введите ответ на вопрос {i+1}: "))
    user_answers.append(answer)
if tuple(user_answers) == correct_answers:
    print("Экзамен сдан")
else:
    print("Экзамен провален")