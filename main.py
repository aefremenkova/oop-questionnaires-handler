from registry import Registry

HEADERS = ["№", "ФИО", "Роль", "Группа/кафедра", "Телефон"]

def find_cols_width(quests):
    cols_width = {}
    correction = 3

    for h in HEADERS:
        match h:
            case "№":
                cols_width[h] = len(quests) + correction
            case "ФИО":
                cols_width[h] = max(len(val) for val in [p.name for p in quests]) + correction
            case "Роль":
                cols_width[h] = max(len(val) for val in [p.role() for p in quests]) + correction
            case "Группа/кафедра":
                cols_width[h] = max(len(val) for val in ([p.extra() for p in quests] + ["Группа/кафедра"])) + correction
            case "Телефон":
                cols_width[h] = max(len(val) for val in [p.masked_phone() for p in quests]) + correction

    return cols_width

def main():
    registry = Registry()

    quest_file = input("Введите название файла с анкетами: ")
    res = registry.load_file(quest_file)
    if not res:
        print(f"Файл '{quest_file}' и файл по умолчанию 'anketa.txt' не найдены")
        return

    print(f"\nПринято: {len(registry)} | Отклонено строк: {registry.rejected_counter}\n")

    cols_width = find_cols_width(registry.accepted_quests)
    headers = f"{"№":<{cols_width["№"]}}{"ФИО":<{cols_width["ФИО"]}}{"Роль":<{cols_width["Роль"]}}" + \
              f"{"Группа/кафедра":<{cols_width["Группа/кафедра"]}}{"Телефон":<{cols_width["Телефон"]}}"
    print("=" * len(headers))
    print(headers)
    print("=" * len(headers))
    for i, rec in enumerate(registry.accepted_quests, 1):
        print(f"{i:<{cols_width["№"]}}{rec.name:<{cols_width["ФИО"]}}{rec.role():<{cols_width["Роль"]}}" + 
              f"{rec.extra():<{cols_width["Группа/кафедра"]}}{rec.masked_phone():<{cols_width["Телефон"]}}")

    print(f"\nОтклонено {len(registry.rejected_quests)} анкет:")
    for r in registry.rejected_quests:
        print(f"\tстрока {r[0]}: {r[2]}")
        print(f"\t\t{r[1]}")
    print()

    print("По ролям:")
    statistics = registry.statistics_by_role()
    for role, num in statistics.items():
        print(f"{role}: {num}")
    print()

    print("По группам:")
    statistics = registry.statistics_by_group()
    for group, num in statistics.items():
        print(f"{group}: {num}")
    print()

    registry.save_results()
    print("Принятые анкеты сохранены в файле ok.txt, отклонённые - в errors.txt")

if __name__ == "__main__":
    main()
