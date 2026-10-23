#from people import Student
#from exceptions import QuestionnaireError

def main():
    """
    test_data = [("Петрова", "petrova@mail.ru", "+79205673421", "09с33"),
                 ("Игнатьев Иван", "ignatiev", "89526334980", "09с33"),
                 ("Петрова Мария Аркадьевна", "petrova@", "89332715541", "09с33"),
                 ("Голубева Александра Львовна", "golubeva@gmailcom", "7 (956) 850-65-70", "09с33"),
                 ("Корчагина Вера Дмитриевна", "@yandex.ru", "8982 407-91-05", "09с33"),
                 ("Марков Иван", "markov@mail.ru", "+792056734", "09с33"),
                 ("Борисов Артём Павлович", "borisov@mail.ru", "556-75-07", "09с33"),
                 ("Куликова Вероника Дмитриевна", "kulikova@mail.ru", "7 (952) 077-25-40", ""),
                 ("Полякова Марьям Георгиевна", "polyakova@gmail.com", "7971537-87-22", " "),
                 ("МАРКОВ иван МАКарОВИЧ", "MARKOV@mail.ru", "7 (970) 450-02-03", "09с41")]

    persons = []

    for d in test_data:
        try:
            persons.append(Student(d[0], d[1], d[2], d[3]))

        except QuestionnaireError as e:
            print(f"Не принято {d[0]}: {e}")

    print()
    for p in persons:
        print(f"{p.role()} {p} ({p.short_fio()}) {p.masked_phone()} {p.extra()}")

    sort_persons = sorted(persons)
    print("\nПо ФИО:")
    for p in sort_persons: print(p)
    """
    pass

if __name__ == "__main__":
    main()
