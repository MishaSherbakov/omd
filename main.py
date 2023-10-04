import csv
from typing import List, Dict, Any


def make_departments(path_to_csv: str = '/Users/oleg/Downloads/Corp_Summary.csv') -> Dict[str, List[List[Any]]]:
    """
    Функция, которая создает словарь departments, где ключи - названия департаментов,
    а значения - это списки списков с двумя "столбцами",
    в которых лежит вся нужная информация для наших функций,
    а именно - "Название отдела" и "Оклад сотрудника", остальная информация отброшена,
    чтобы не занимать память. Получается своеобразный group_by, но без агрегации.

    :param path_to_csv: путь к файлу csv.
    :return: Словарь departments, описанный выше.
    """

    departments = dict()
    with open(path_to_csv, 'r') as file:
        full_csv = list(csv.DictReader(file, delimiter=';'))
        for row in full_csv:
            if row['Департамент'] not in departments:
                departments[row['Департамент']] = list()
                department = row['Департамент']
                departments[department].append([value for key, value in row.items() if key in ('Отдел', 'Оклад')])
            else:
                department = row['Департамент']
                departments[department].append([value for key, value in row.items() if key in ('Отдел', 'Оклад')])

    return departments


def department_report(departments: Dict[str, List[List[Any]]]) -> None:
    """
    Функция, которая выводит в консоль департамент и все команды(отделы), которые входят в него.

    :param departments: словарь, содержащий информацию об отделах для каждого департамента.
    :rtype: None
    """
    department_hierarchy = dict()
    for department in departments:
        department_hierarchy[department] = set()
    for department, information in departments.items():
        for row in information:
            department_hierarchy[department].add(row[0])
    for department in department_hierarchy:
        print(f"{department} : {', '.join(map(str, department_hierarchy[department]))}")
    print()


def array_calculations(salaries: List[int]) -> Dict[str, Any]:
    """
    Функция, которая за один проход по массиву считает count, max, min и avg.

    :param salaries: Столбик с зарплатами людей для конкретного департамента.
    :rtype: None
    """
    answer = dict()
    max_value = salaries[0]
    min_value = salaries[0]
    sum_values = 0
    count = 0

    for num in salaries:
        if num > max_value:
            max_value = num
        if num < min_value:
            min_value = num
        sum_values += num
        count += 1

    avg_value = round(sum_values / count, 2)

    answer['count'] = count
    answer['min'] = min_value
    answer['max'] = max_value
    answer['avg'] = avg_value
    return answer


def make_salary_report(departments: Dict[str, List[List[Any]]]) -> List[List[Any]]:
    """
    Функция, которая создает таблицу(List[List[]]) salary_report, где первая строка - названия столбцов,
    остальные строчки - это значения для каждого департамента. Дальше salary_report используется
    в функциях salary_report_print и salary_report_save_csv в зависимости от запроса пользователя.

    :param departments: словарь, содержащий информацию о зарвлатах для каждого департамента.
    :return: таблица salary_report
    """
    salary_report = list()
    salary_report.append(['Депарпамент', 'Кол-во сотрудников', 'Вилка min-max по зарплатам', 'Среднаяя зарплата'])
    for departament, information in departments.items():
        calculations = array_calculations([int(column[1]) for column in information])
        salary_report.append([
            departament,
            calculations['count'],
            f"{calculations['min']} - {calculations['max']}",
            calculations['avg']
        ])
    return salary_report


def salary_report_print(departments: Dict[str, List[List[Any]]]) -> None:
    """
    Функция, которая выводит в консоль сводный отчёт по департаментам

    :param departments: словарь, содержащий информацию о зарпоатах для каждого департамента.
    :rtype: None
    """
    salary_report = make_salary_report(departments)
    column_widths = [max(len(str(item)) for item in column) for column in zip(*salary_report)]

    # Вывод таблицы с выравниванием
    for row in salary_report:
        row_str = ''
        for i, item in enumerate(row):
            row_str += str(item).ljust(column_widths[i] + 2)
        print(row_str)
    print()


def salary_report_save_csv(departments: Dict[str, List[List[Any]]]) -> None:
    """
    Функция, сохраняет сводный отчёт по департаментам в файл 'salary_report.csv'

    :param departments: словарь, содержащий информацию о зарпоатах для каждого департамента.
    :rtype: None
    """
    salary_report = make_salary_report(departments)
    with open('salary_report.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerows(salary_report)
    print("Файл сохранен в salary_report.csv.")
    print()


def choice_menu() -> None:
    """
    Функция, которая реализует меню для взаимодействия с пользователем
    и запускает нужные функции в зависимости от ввода.

    :rtype: None
    """
    departments = make_departments()
    while True:
        print('Выберите один из вариантов:')
        print('Введите 1 - Чтобы вывести иерархию команд;')
        print('Введите 2 - Чтобы вывести сводный отчёт;')
        print('Введите 3 - Чтобы сохранить сводный отчёт;')
        print('Введите что-то другое - Чтобы завершить программу;')
        user_answer = int(input())
        print()
        if user_answer == 1:
            department_report(departments)
        elif user_answer == 2:
            salary_report_print(departments)
        elif user_answer == 3:
            salary_report_save_csv(departments)
        else:
            break


if __name__ == "__main__":
    choice_menu()
