import psycopg2
from psycopg2 import extensions, OperationalError
from src.config import db_config
from typing import Optional
from src.external_api import employers_info, vacancies_info


def create_db() -> None:
    """Создает базу данных, если она еще не существует."""
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_config.get("user"),
            password=db_config.get("password"),
            host=db_config.get("host"),
            port=db_config.get("port"),
        )
        conn.autocommit = True
        cur = conn.cursor()

        db_name = db_config["dbname"]
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {db_name}")
            print(f"База данных '{db_name}' создана")
        else:
            print(f"База данных '{db_name}' уже существует")

    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_db_connection() -> extensions.connection:
    """Возвращает соединение с базой данных"""
    try:
        conn: extensions.connection = psycopg2.connect(**db_config)
        print("Подключение успешно!")
        return conn
    except OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        raise


def create_tables(conn: extensions.connection) -> None:
    """Создает таблицы в базе данных"""
    cursor: Optional[extensions.cursor] = None
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employers (
                employer_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255),
                open_vacancies INTEGER
            )
        """
        )
        print("Таблица employers создана/проверена")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id),
                employer_name VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                salary_from VARCHAR(100),
                salary_to VARCHAR(100),
                url VARCHAR(255)
            )
        """
        )
        print("Таблица vacancies создана/проверена")

        conn.commit()
        print("База данных готова к использованию!")

    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()


def add_employer(conn: extensions.connection, employer: list) -> None:
    """Вставляет данные о работодателе или компании в таблицу employers."""

    command = """
    INSERT INTO employers (employer_id, name, url, open_vacancies)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (employer_id) DO NOTHING
    """

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(command, (employer[0], employer[1], employer[2], employer[3]))
        conn.commit()
        print(f"Работодатель '{employer[1]}' добавлен/обновлен")

    except psycopg2.DatabaseError as e:
        conn.rollback()
        print(f"Ошибка базы данных при добавлении работодателя: {e}")
    except Exception as e:
        conn.rollback()
        print(f"Неизвестная ошибка при добавлении работодателя: {e}")
    finally:
        if cursor:
            cursor.close()


def add_vacancy(conn: extensions.connection, vacancy: list) -> None:
    """Вставляет данные о вакансии в таблицу vacancies."""

    if len(vacancy) < 7:
        print(f"Недостаточно данных в вакансии: {vacancy}")
        return

    command = """
        INSERT INTO vacancies (vacancy_id, employer_id, employer_name, name, salary_from, salary_to, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (vacancy_id) DO NOTHING
        """

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            command,
            (
                vacancy[0],  # vacancy_id
                vacancy[1],  # employer_id
                vacancy[2],  # employer_name
                vacancy[3],  # name
                vacancy[4],  # salary_from
                vacancy[5],  # salary_to
                vacancy[6],  # url
            ),
        )
        conn.commit()
        print(f"Вакансия '{vacancy[3]}' добавлена")

    except psycopg2.DatabaseError as e:
        conn.rollback()
        print(f"Ошибка базы данных при добавлении вакансии: {e}")
    except Exception as e:
        conn.rollback()
        print(f"Неизвестная ошибка при добавлении вакансии: {e}")
    finally:
        if cursor:
            cursor.close()


def db_ready() -> None:
    """Объединяет весь функционал api и db."""
    create_db()
    conn = get_db_connection()
    create_tables(conn)
    companies = employers_info()
    print(companies)
    for employer in companies:
        add_employer(conn, employer)
    vacancies = vacancies_info()
    for vacancy in vacancies:
        add_vacancy(conn, vacancy)
