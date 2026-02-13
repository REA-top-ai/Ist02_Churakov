#1
favour_word = "концептульно"
print(favour_word)

#2
first_name = "Виталий"
last_name = "Красилов"
new_account = last_name[:5]
temp_password = last_name[2:6]
print(new_account, temp_password)

#3
def account_generator(first_name, last_name):
    return first_name[:3]+last_name[:3]
new_account = account_generator("Виталий", "Красилов")
print(new_account)

#4
def password_generator(first_name, last_name):
    return first_name[len(first_name)-3:] + last_name[len(last_name)-3:]
temp_password= password_generator("Виталий", "Красилов")
print(temp_password)

#5
company_motto = "Мечты сбываются"
second_to_last = company_motto[-2]
final_word = company_motto[-4:]
print(second_to_last, final_word)

#6
first_name = "Боб Дейли"
fixed_first_name = "Р" + first_name[1:]
print(fixed_first_name)

#7
password = 'theycallme\"crazy\"91'
print(password)

#8
poem_title = "spring storm"
poem_title_fixed = poem_title.title()
poem_author = "William Carlos Williams"
print(poem_title, poem_title_fixed)
