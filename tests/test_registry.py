from people import Person, Student, Teacher, QuestionnaireError
from registry import Registry
import pytest

TEST_QUESTS = """s;  иванов   иВАН петрович ;IvAnov@Mail.Ru ; +7 (921) 111-22-33 ; 09с33
x;непонятный тип;a@b.ru;89211112233;что-то
t;смирнова ольга;smirnova@inbox.ru;+7921123;Кафедра И4
t;петров пётр сергеевич;petrov@voenmeh.ru;89217654321;Кафедра И9
s;кузнецов павел;kuznetsov.mail.ru;+79211234567;09с34
s;игнатьева Ксения ВЯЧЕСЛАВОВНА;ignatieva@yandex.ru;8918 423-60-17;09с41
"""

@pytest.fixture
def test_registry(tmp_path):
    put = tmp_path / "anketa.txt"
    put.write_text(TEST_QUESTS, encoding="utf-8")
    registry = Registry()
    registry.load_file(put)
    return registry

def test_student_record_is_correctly_parsed():
    test_registry = Registry()
    test_registry.process_record("s;  иванов   иВАН петрович ;IvAnov@Mail.Ru ; +7 (921) 111-22-33 ; 09с33", 1)
    quest = test_registry.accepted_quests[0]
    assert len(test_registry) == 1 and str(quest) == "Иванов Иван Петрович" and \
        quest.email == "ivanov@mail.ru" and quest.phone == "+7 (921) 111-22-33" and \
        quest.extra() == "09с33" and quest.role() == "студент"

def test_teacher_record_is_correctly_parsed():
    test_registry = Registry()
    test_registry.process_record("t;  иванов   иВАН петрович ;IvAnov@Mail.Ru ; +7 (921) 111-22-33 ; Кафедра И9", 1)
    quest = test_registry.accepted_quests[0]
    assert len(test_registry) == 1 and str(quest) == "Иванов Иван Петрович" and \
        quest.email == "ivanov@mail.ru" and quest.phone == "+7 (921) 111-22-33" and \
        quest.extra() == "Кафедра И9" and quest.role() == "преподаватель"

@pytest.mark.parametrize("input_data", [
    "x;непонятный тип;a@b.ru;89211112233;что-то",
    "s;  иванов   иВАН петрович ;IvAnov@Mail.Ru ;09с33",
    ""
    ])
def test_invalid_record_is_rejected(input_data):
    test_registry = Registry()
    test_registry.process_record(input_data, 1)
    assert len(test_registry.rejected_quests) == 1 and \
        test_registry.rejected_quests[0][1] == input_data and \
        (test_registry.rejected_quests[0][2].startswith("Должно быть 5 полей, получено") or \
        test_registry.rejected_quests[0][2].startswith("Неизвестный тип"))

def test_registry_is_empty_after_creation():
    test_registry = Registry()
    assert len(test_registry) == 0

def test_registry_has_3_accepted_from_TEST_QUESTS(test_registry):
    assert len(test_registry) == 3

def test_registry_has_3_rejected_from_TEST_QUESTS(test_registry):
    assert len(test_registry.rejected_quests) == 3

def test_registry_has_right_string_nums_from_TEST_QUESTS(test_registry):
    rejected_string_nums = [r[0] for r in test_registry.rejected_quests]
    assert rejected_string_nums == [2, 3, 5]

def test_nonexistent_file_load_return_false():
    test_registry = Registry()
    assert test_registry.load_file("unknown.txt") == False

def test_registry_statistics_by_role_returns_valid_dict(test_registry):
    stats = test_registry.statistics_by_role()
    assert list(stats.keys()) == ["студент", "преподаватель"] and \
        stats["студент"] == 2 and stats["преподаватель"] == 1

def test_registry_statistics_by_group_counts_only_students(test_registry):
    stats = test_registry.statistics_by_role()
    assert stats["студент"] == len([s for s in test_registry.accepted_quests if s.role() == "студент"])

def test_registry_iterated_by_for(test_registry):
    for rec in test_registry.accepted_quests:
        pass
    for rec in test_registry.rejected_quests:
        pass

def test_register_sorted_by_name_is_in_alphabet_order(test_registry):
    test_registry.sort_result_by_name()
    assert test_registry.accepted_quests[0].name == "Иванов Иван Петрович" and \
        test_registry.accepted_quests[1].name == "Игнатьева Ксения Вячеславовна" and \
        test_registry.accepted_quests[2].name == "Петров Пётр Сергеевич"

def test_register_save_accepted_write_1_line_for_1_person(test_registry):
    try:
        with open('ok.txt', 'r', encoding='utf-8') as f:
            line_count_before = sum(1 for _ in f)
    except FileNotFoundError:
        line_count_before = 0
    
    test_registry.save_accepted()
    with open('ok.txt', 'r', encoding='utf-8') as f:
        line_count_after = sum(1 for _ in f)

    assert line_count_after - line_count_before == 3

def test_register_save_rejected_has_reject_reason(test_registry):
    test_registry.save_rejected()
    with open("errors.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    test_quests_lines = lines[-3:]
    test_quests_lines_errors = [fields[-1].rstrip("\n") for fields in [line.split(";") for line in test_quests_lines]]

    assert test_quests_lines_errors == ["Неизвестный тип x", 
                                        "Номер телефона должен содержать 11 цифр, получено 7",
                                        "В эл.адресе отсутствует @"]

def test_register_sorted_by_cyrillic_name_is_in_alphabet_order():
    test_registry = Registry()
    persons = [Person("Яковлева Валентина", "yakovleva@mail.ru", "+79112345678"),
               Person("Ёлкина Юлия", "yolkina@mail.ru", "+79107776189"),
               Person("Абрамова Елизавета Викторовна", "abramova@mail.ru", "+79002345678"),]
    for p in persons:
        test_registry.accept(p)

    test_registry.sort_result_by_name()
    assert [quest.name for quest in test_registry.accepted_quests] == ["Абрамова Елизавета Викторовна",
                                                                       "Ёлкина Юлия", "Яковлева Валентина"]