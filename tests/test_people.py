from people import Person, Student, Teacher, QuestionnaireError
import pytest

@pytest.mark.parametrize("input_data, expected", [
    ("петрова АННА", "Петрова Анна"),
    ("  Дмитриев василий  ", "Дмитриев Василий"),
    ("игнатьев   владислаВ КОНСТАНТИНОВИЧ", "Игнатьев Владислав Константинович"),
    ("               МОРОЗОВА СОФИЯ ВАСИЛЬЕВНА", "Морозова София Васильевна")
    ])
def test_name_is_uniformly_normalized(input_data, expected):
    assert Person.normalize_name(input_data) == expected

def test_one_word_name_is_denied():
    with pytest.raises(QuestionnaireError):
        Person.verify_name("Васильева")

@pytest.mark.parametrize("input_data, expected", [
    ("MARk@mail.RU", "mark@mail.ru"),
    ("MOROZOVA@YANDEX.RU", "morozova@yandex.ru")
    ])
def test_email_is_lowered(input_data, expected):
    assert Person.normalize_email(input_data) == expected

@pytest.mark.parametrize("input_data", [
    "@mail.RU"
    "MOROZOVA@",
    "vasilieva@mailru",
    "petrovivan"
    ])
def test_invalid_email_is_denied(input_data):
    with pytest.raises(QuestionnaireError):
        assert Person.verify_email(input_data)

@pytest.mark.parametrize("input_data, expected", [
    ("  8911 754-33-01", "+7 (911) 754-33-01"),
    ("796532321-20", "+7 (965) 323-21-20"),
    ("8 910 715 6680", "+7 (910) 715-66-80"),
    ("+7915 666   30 11", "+7 (915) 666-30-11")
    ])
def test_phone_is_uniformly_normalized(input_data, expected):
    assert Person.normalize_phone_number(input_data) == expected

@pytest.mark.parametrize("input_data", [
    "+7910777"
    "+96512389732",
    "8910000000000000"
    ])
def test_invalid_phone_is_denied(input_data):
    with pytest.raises(QuestionnaireError):
        assert Person.verify_phone_number(input_data)

@pytest.mark.parametrize("input_data, expected", [
    ("  8911 754-33-01", "+7 (911) ***-**-01"),
    ("796532321-20", "+7 (965) ***-**-20")
    ])
def test_phone_is_masked(input_data, expected):
    test_person = Person("Иванов Иван", "ivanov@mail.ru", input_data)
    assert test_person.masked_phone() == expected

@pytest.mark.parametrize("input_data, expected", [
    ("Иванов Иван", "Иванов И."),
    ("Игнатьева Василиса Андреевна", "Игнатьева В. А.")
    ])
def test_name_is_shortening(input_data, expected):
    test_person = Person(input_data, "test@maila.ru", "+79000000000")
    assert test_person.short_fio() == expected

def test_different_roles():
    test_student = Student("Иванов Иван", "ivanov@mail.ru", "+79000000000", "09с41")
    test_teacher = Teacher("Петрова Анна", "petrova@yandex.ru", "89111111111", "Кафедра А3")

    assert test_student.role() == "студент" and test_teacher.role() == "преподаватель"

@pytest.mark.parametrize("input_data", [
    ("Иванов Иван", "ivanov@mail.ru", "+79100000010", "  "),
    ("Иванов Иван", "ivanov@mail.ru", "+79100000010")
    ])
def test_student_without_group_is_denied(input_data):
    with pytest.raises(QuestionnaireError):
        if len(input_data) == 4:
            Student(input_data[0], input_data[1], input_data[2], input_data[3])
        else:
            Student(input_data[0], input_data[1], input_data[2])

def test_double_surname_correctly_capitalized():
    assert Person.normalize_name("петров-водкин кузьма") == "Петров-Водкин Кузьма"

def test_email_with_space_inside_is_rejected():
    with pytest.raises(QuestionnaireError):
        Person.verify_email("iv anov@mail.ru")
