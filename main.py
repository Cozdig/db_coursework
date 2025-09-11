from src.create_db import db_ready
import src.interface
from src.db_manager import DBManager


def main() -> None:
    """Главная функция, объединяет весь функционал в проекте"""
    db_ready()
    db_manager = DBManager()
    answer = {
        1: lambda: src.interface.print_employers_and_vacancies(db_manager),
        2: lambda: src.interface.print_all_vacancies(db_manager),
        3: lambda: src.interface.print_avg_salary(db_manager),
        4: lambda: src.interface.print_vacancies_with_higher_salary(db_manager),
        5: lambda: print(src.interface.ask_keyword(db_manager)),
        6: exit,
    }

    while True:
        try:
            user_input = src.interface.main_interface()
            if user_input in answer:
                answer[user_input]()
            else:
                print("Некорректный ввод. Пожалуйста, выберите число от 1 до 6")

        except ValueError:
            print("Пожалуйста, введите число от 1 до 6")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
