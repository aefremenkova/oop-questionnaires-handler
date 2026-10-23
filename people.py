from exceptions import QuestionnaireError

class Person:
    def __init__(self, name, email, phone):
        self.verify_name(name)
        self.name = self.normalize_name(name)

        self.verify_email(email)
        self.email = self.normalize_email(email)

        self.verify_phone_number(phone)
        self.phone = self.normalize_phone_number(phone)

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
        self.group = group

    @staticmethod
    def verify_group(group):
        group = group.strip()
        if len(group) == 0:
            raise QuestionnaireError("Пустой номер группы")

    @staticmethod
    def normalize_group(group):
        return group.replace(" ", "").lower()

    def role(self):
        return "студент"

    def extra(self):
        return self.group