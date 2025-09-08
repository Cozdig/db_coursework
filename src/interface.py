from src.db_manager import DBManager


def main_interface() -> int:
    """Базовый интерфейс, спрашивает у пользователя нужное действие и возвращает его."""
    user_input = int(
        input(
            """1: Получить список всех компаний и количество вакансий у каждой компании.
2: Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
3: Получить среднюю зарплату по вакансиям.
4: Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
5: Получить список всех вакансий по ключевому слову.
6: Выход.
Ваш выбор: """
        )
    )
    return user_input


def print_employers_and_vacancies(db_manager: DBManager) -> None:
    """Выводит кампании и сколько открытых вакансий в этой компании."""
    employers = db_manager.get_companies_and_vacancies_count()
    result = ""
    for employer in employers:
        result += f"\nКомпания: {employer[0]}, Кол-во открытых вакансий: {employer[1]}, Ссылка {employer[2]}\n"

    print(result)


def print_all_vacancies(db_manager: DBManager) -> None:
    """Выводит все вакансии и информацию о каждой."""
    vacancies = db_manager.get_all_vacancies()
    result = ""
    for vac in vacancies:
        result += f"""\nКомпания: {vac[0]}, Вакансия: {vac[1]},
Зарплата от: {vac[2]} до: {vac[3]},
Ссылка: {vac[4]}\n"""

    print(result)


def print_avg_salary(db_manager: DBManager) -> None:
    """Выводит среднюю зарплату по всем вакансиям."""
    vacancies = db_manager.get_avg_salary()
    result = f"\nСредняя зарплата: {int(vacancies[0][0])}\n"

    print(result)


def print_vacancies_with_higher_salary(db_manager: DBManager) -> None:
    """Выводит все вакансии, у которых зарплата выше средней."""
    vacancies = db_manager.get_vacancies_with_higher_salary()
    result = ""
    for vac in vacancies:
        result += f"\nВакансия: {vac[0]}, Зарплата: {vac[1]}, Ссылка: {vac[2]}\n"

    print(result)


def ask_keyword(db_manager: DBManager) -> str:
    """Запрашивает у пользователя ключевое слово, потом возвращает вакансии по этому слову."""
    keyword = input("Введите ключевое слово: ")
    vacancies = db_manager.get_vacancies_with_keyword(keyword)
    if not vacancies:
        return "\nВакансии не найдены\n"

    result = ""
    for vac in vacancies:
        result += f"""\nКомпания: {vac[4]}, Вакансия: {vac[1]},
Зарплата от: {vac[2]} до: {vac[3]},
Ссылка: {vac[6]}\n"""

    return result
