import psycopg2
from abc import ABC, abstractmethod
from src.config import db_config


class DBBase(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        pass


class DBManager:
    """Класс для взаимодействия с базой данных."""

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=db_config["dbname"],
            user=db_config.get("user"),
            password=db_config.get("password"),
            host=db_config.get("host"),
            port=db_config.get("port"),
        )
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.cursor.execute(
            """SELECT e.name, COUNT(v.vacancy_id) as vacancy_count, e.url
               FROM employers e
               INNER JOIN vacancies v ON e.employer_id = v.employer_id
               GROUP BY e.name, e.url;"""
        )
        employers = self.cursor.fetchall()
        return employers

    def get_all_vacancies(self) -> list:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        self.cursor.execute(
            """SELECT employer_name,name,salary_from,salary_to,url
                        FROM vacancies;"""
        )
        vacancies = self.cursor.fetchall()
        return vacancies

    def get_avg_salary(self) -> list:
        """Получает среднюю зарплату по вакансиям."""
        self.cursor.execute(
            """SELECT AVG(salary_from)
                        FROM vacancies
                        WHERE salary_from > 0;"""
        )
        avg_salary = self.cursor.fetchall()
        return avg_salary

    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        avg_salary = avg_salary[0][0]
        self.cursor.execute(
            f"""SELECT name, salary_from, url
                        FROM vacancies
                        WHERE salary_from > {avg_salary};"""
        )
        vacancies = self.cursor.fetchall()
        return vacancies

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        self.cursor.execute(
            """
            SELECT
                vacancy_id,
                name,
                salary_from,
                salary_to,
                employer_name,
                employer_id,
                url
            FROM vacancies
            WHERE name ILIKE %s
            ORDER BY name
        """,
            (f"%{keyword}%",),
        )

        vacancies = self.cursor.fetchall()
        return vacancies
