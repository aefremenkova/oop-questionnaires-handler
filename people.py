class QuestionnaireError(Exception):
    pass

class Person:
    col_width_correction = 3
    name_col_width = len("ФИО") + col_width_correction
    email_col_width = len("Email") + col_width_correction
    phone_col_width = len("Телефон") + col_width_correction
    role_col_width = len("Роль") + col_width_correction
    extra_col_width = len("Группа/кафедра") + col_width_correction

    def __init__(self, name, email, phone):
        self.verify_name(name)
        self.name = self.normalize_name(name)
        if len(self.name) > Person.name_col_width:
            Person.name_col_width = len(self.name) + Person.col_width_correction

        self.verify_email(email)
        self.email = self.normalize_email(email)
        if len(self.email) > Person.email_col_width:
            Person.email_col_width = len(self.email) + Person.col_width_correction

        self.verify_phone_number(phone)
        self.phone = self.normalize_phone_number(phone)
        if len(self.phone) > Person.phone_col_width:
            Person.phone_col_width = len(self.phone) + Person.col_width_correction

    @staticmethod
    def verify_name(name):
        parts = name.split()
        if len(parts) < 2:
            raise QuestionnaireError("В ФИО меньше двух слов")

    @staticmethod
    def normalize_name(name):
        norm_parts = [n.capitalize() for n in name.split()]

        return " ".join(norm_parts)

    @staticmethod
    def verify_email(email):
        errors = []

        at_count = email.count("@")
        if at_count != 1:
            raise QuestionnaireError("В эл.адресе отсутствует @" if at_count == 0 
                                 else "В эл.адресе несколько @")
    
        parts = email.split("@")
        if any(p == '' for p in parts):
            raise QuestionnaireError("Пустое имя почтового ящика или домен в эл.адресе")

        user = parts[0]
        domen = parts[1]

        if "." not in domen:
            errors.append("В домене эл.адреса отсутствует точка")

        if domen[0] == ".":
            errors.append("В домене эл.адреса отсутствует имя домена")

        if domen[-1] == ".":
            errors.append("В домене эл.адреса отсутствует доменная зона")

        if len(errors) != 0:
            raise QuestionnaireError(errors)

    @staticmethod
    def normalize_email(email):
        return email.lower()

    @staticmethod
    def verify_phone_number(phone):
        digits = [s for s in phone if s.isdigit()]

        if len(digits) != 11:
            raise QuestionnaireError(f"Номер телефона должен содержать 11 цифр, получено {len(digits)}")

        if digits[0] != "7" and digits[0] != "8":
            return QuestionnaireError("Номер телефона должен начинаться с 7 или 8, получено {digits[0]}")

    
    @staticmethod
    def normalize_phone_number(phone):
        digits = [s for s in phone if s.isdigit()]

        norm_phone_parts = ["+7", f"({"".join(digits[1:4])})", 
                            f"{"".join(digits[4:7])}-{"".join(digits[7:9])}-{"".join(digits[9:])}"]

        return " ".join(norm_phone_parts)


    def masked_phone(self):
        digits = [s for s in self.phone if s.isdigit()]

        mask_phone_parts = ["+7", f"({"".join(digits[1:4])})", f"***-**-{"".join(digits[9:])}"]

        return " ".join(mask_phone_parts)

    def short_fio(self):
        name_parts = self.name.split()
        surname_initials = [name_parts[0]]
        for n in name_parts[1:]:
            surname_initials.append(n[0] + ".")

        return " ".join(surname_initials)

    def role(self):
        pass

    def extra(self):
        pass

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return str(self) < str(other)

class Student(Person):
    def __init__(self, name, email, phone, group=''):
        super().__init__(name, email, phone)

        self.verify_group(group)
        self.group = self.normalize_group(group)
        if len(self.group) > Person.extra_col_width:
            Person.extra_col_width = len(self.group) + Person.col_width_correction

        if len(self.role()) > Person.role_col_width:
            Person.role_col_width = len(self.role()) + Person.col_width_correction

    @staticmethod
    def verify_group(group):
        group = group.strip()
        if len(group) == 0:
            raise QuestionnaireError("Пустой номер группы")

    @staticmethod
    def normalize_group(group):
        return group.strip().replace(" ", "").lower()

    def role(self):
        return "студент"

    def extra(self):
        return self.group

class Teacher(Person):
    def __init__(self, name, email, phone, department=''):
        super().__init__(name, email, phone)

        self.verify_department(department)
        self.department = department
        if len(self.department) > Person.extra_col_width:
            Person.extra_col_width = len(self.department) + Person.col_width_correction

        if len(self.role()) > Person.role_col_width:
            Person.role_col_width = len(self.role()) + Person.col_width_correction

    @staticmethod
    def verify_department(department):
        department = department.strip()
        if len(department) == 0:
            raise QuestionnaireError("Пустое наименование кафедры")

    @staticmethod
    def normalize_group(department):
        return department.lower()

    def role(self):
        return "преподаватель"

    def extra(self):
        return self.department

if __name__ == "__main__":
    print("=" * 45 + "ПРОВЕРКА КЛАССА Student" + "=" * 45)
    test_data = [("Петрова", "petrova@mail.ru", "+79205673421", "09с33"),
                 ("Игнатьев Иван", "ignatiev", "89526334980", "09с33"),
                 ("Петрова Мария Аркадьевна", "petrova@", "89332715541", "09с33"),
                 ("Голубева Александра Львовна", "golubeva@gmailcom", "7 (956) 850-65-70", "09с33"),
                 ("Корчагина Вера Дмитриевна", "@yandex.ru", "8982 407-91-05", "09с33"),
                 ("Марков Иван", "markov@mail.ru", "+792056734", "09с33"),
                 ("Борисов Артём Павлович", "borisov@mail.ru", "556-75-07", "09с33"),
                 ("Куликова Вероника Дмитриевна", "kulikova@mail.ru", "7 (952) 077-25-40", ""),
                 ("Полякова Марьям Георгиевна", "polyakova@gmail.com", "7971537-87-22", " "),
                 ("МАРКОВ иван МАКарОВИЧ", "MARKOV@mail.ru", "7 (970) 450-02-03", "09с41"),
                 ("Морозова София", "morozova@yandex.ru", "7910453-00-18", "09с33")]

    students = []

    for d in test_data:
        try:
            students.append(Student(d[0], d[1], d[2], d[3]))

        except QuestionnaireError as e:
            print(f"Не принято {d[0]}: {e}")

    print()
    for p in students:
        print(f"{p.role()} {p} ({p.short_fio()}) {p.masked_phone()} {p.extra()}")

    sort_persons = sorted(students)
    print("\nПо ФИО:")
    for p in sort_persons: print(p)
    print("\n")

    print("=" * 45 + "ПРОВЕРКА КЛАССА Teacher" + "=" * 45)
    test_data = [("Петрова", "petrova@mail.ru", "+79205673421", "Кафедра И9"),
                 ("Игнатьев Иван", "ignatiev", "89526334980", "Кафедра И9"),
                 ("Петрова Мария Аркадьевна", "petrova@", "89332715541", "Кафедра И9"),
                 ("Голубева Александра Львовна", "golubeva@gmailcom", "7 (956) 850-65-70", "Кафедра И9"),
                 ("Корчагина Вера Дмитриевна", "@yandex.ru", "8982 407-91-05", "Кафедра И9"),
                 ("Марков Иван", "markov@mail.ru", "+792056734", "Кафедра И9"),
                 ("Борисов Артём Павлович", "borisov@mail.ru", "556-75-07", "Кафедра И9"),
                 ("Куликова Вероника Дмитриевна", "kulikova@mail.ru", "7 (952) 077-25-40", ""),
                 ("Полякова Марьям Георгиевна", "polyakova@gmail.com", "7971537-87-22", " "),
                 ("МАРКОВ иван МАКарОВИЧ", "MARKOV@mail.ru", "7 (970) 450-02-03", "Кафедра А4"),
                 ("Морозова София", "morozova@yandex.ru", "7910453-00-18", "Кафедра О7")]

    teachers = []

    for d in test_data:
        try:
            teachers.append(Teacher(d[0], d[1], d[2], d[3]))

        except QuestionnaireError as e:
            print(f"Не принято {d[0]}: {e}")

    print()
    for p in teachers:
        print(f"{p.role()} {p} ({p.short_fio()}) {p.masked_phone()} {p.extra()}")

    sort_persons = sorted(teachers)
    print("\nПо ФИО:")
    for p in sort_persons: print(p)