from people import Student, Teacher, QuestionnaireError

class Registry:
    def __init__(self):
        self.accepted_quests = []
        self.rejected_quests = []
        self.rejected_counter = 0
 
    def accept(self, person):
        self.accepted_quests.append(person)

    def reject(self, rec_num, rec, error):
        self.rejected_counter += 1
        self.rejected_quests.append((rec_num, rec, error))

    def process_record(self, record, rec_num):
        fields = record.split(";")

        if len(fields) != 5:
            self.reject(rec_num, record, f"Должно быть 5 полей, получено {len(fields)}")
            return

        match fields[0].lower():
            case 's':
                try:
                    self.accept(Student(fields[1], fields[2], fields[3], fields[4]))
                except QuestionnaireError as e:
                    self.reject(rec_num, record, e)

            case 't':
                try:
                    self.accept(Teacher(fields[1], fields[2], fields[3], fields[4]))
                except QuestionnaireError as e:
                    self.reject(rec_num, record, e)

            case _:
                self.reject(rec_num, record, f"Неизвестный тип {fields[0]}")


    def load_file(self, filename = "anketa.txt"):
        records = []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    records.append(line)

            i = 0
            for record in records:
                i += 1

                record = record.strip()
                if len(record) == 0:
                    self.rejected_counter += 1
                    continue

                self.process_record(record, i)

        except FileNotFoundError:
            return False

    def statistics_by_group(self):
        accepted_by_group = {}
        for obj in self.accepted_quests:
            if obj.role() != "студент":
                continue

            group = obj.extra()
            if group not in accepted_by_group:
                accepted_by_group[group] = [obj]
            else:
                accepted_by_group[group].append(obj)

        statistics = {}
        for group, recs in accepted_by_group.items():
            statistics[group] = len(recs)

        return statistics

    def statistics_by_role(self):
        accepted_by_role = {}
        for obj in self.accepted_quests:
            role = obj.role()
            if role not in accepted_by_role:
                accepted_by_role[role] = [obj]
            else:
                accepted_by_role[role].append(obj)

        statistics = {}
        for role, recs in accepted_by_role.items():
            statistics[role] = len(recs)

        return statistics

    def save_results(self):
        with open("ok.txt", "a", encoding="utf-8") as f:
            for person in self.accepted_quests:
                f.writelines(f"{person.name};{person.email};{person.phone};{person.role()};{person.extra()}\n")

        with open("errors.txt", "a", encoding="utf-8") as f:
            for quest in self.rejected_quests:
                f.writelines(f"{quest[1]}{";" if quest[1][-1] != ";" else ""}{quest[2]}\n")

    def __len__(self):
        return len(self.accepted_quests) 

if __name__ == "__main__":
    registry = Registry()

    registry.load_file("anketa.txt")

    print(f"Принято: {len(registry)} | Отклонено строк: {registry.rejected_counter}\n")

    print("Принято:")
    for i, rec in enumerate(registry.accepted_quests, 1):
        print(f"{i:<5}{rec.name:<35}{rec.role():<20}{rec.extra():<20}{rec.masked_phone():<20}")
    print()

    print(f"Отклонено {len(registry.rejected_quests)} анкет:")
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
