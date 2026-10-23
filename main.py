from people import Person
from registry import Registry

def main():
    registry = Registry()

    quest_file = input("Введите название файла с анкетами или нажмите " +
                       "Enter, чтобы использовать файл по умолчанию (anketa.txt): ")
    if not quest_file.strip():
        res = registry.load_file()
    else:
        res = registry.load_file(quest_file)
    if not res:
        print(f"Файл '{quest_file}' не найден")
        return

    registry.sort_result_by_name()
    print(f"\nПринято: {len(registry)} | Отклонено строк: {registry.rejected_counter}\n")

    headers = f"{"№":<{len(registry.accepted_quests) + Person.col_width_correction}}" + \
              f"{"ФИО":<{Person.name_col_width}}{"Роль":<{Person.role_col_width}}" + \
              f"{"Группа/кафедра":<{Person.extra_col_width}}{"Телефон":<{Person.phone_col_width}}"
    print("=" * len(headers))
    print(headers)
    print("=" * len(headers))
    for i, rec in enumerate(registry.accepted_quests, 1):
        print(f"{i:<{len(registry.accepted_quests) + Person.col_width_correction}}" +\
              f"{rec.name:<{Person.name_col_width}}{rec.role():<{Person.role_col_width}}" + 
              f"{rec.extra():<{Person.extra_col_width}}{rec.masked_phone():<{Person.phone_col_width}}")

    print(f"\nОтклонено {len(registry.rejected_quests)} анкет:")
    for r in registry.rejected_quests:
        print(f"\tстрока {r[0]}: {r[2]}")
        print(f"\t\t{r[1]}")
    print()

    print("По ролям:")
    statistics = registry.statistics_by_role()
    for role, num in statistics.items():
        print(f"\t{role}: {num}")
    print()

    print("По группам:")
    statistics = registry.statistics_by_group()
    for group, num in statistics.items():
        print(f"\t{group}: {num}")
    print()

    registry.save_accepted()
    registry.save_rejected()
    print("Принятые анкеты сохранены в файле ok.txt, отклонённые - в errors.txt")

if __name__ == "__main__":
    main()
