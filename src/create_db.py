import psycopg2
from psycopg2 import extensions, OperationalError
from src.config import db_config, companies
from typing import Optional


def create_db() -> None:
    """Создает базу данных, если она еще не существует."""
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_config.get('user'),
            password=db_config.get('password'),
            host=db_config.get('host'),
            port=db_config.get('port')
        )
        conn.autocommit = True
        cur = conn.cursor()

        db_name = db_config['dbname']
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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                url VARCHAR(255)
            )
        """)
        print("Таблица employers создана/проверена")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id),
                name VARCHAR(255) NOT NULL,
                description TEXT,
                salary VARCHAR(100),
                url VARCHAR(255)
            )
        """)
        print("Таблица vacancies создана/проверена")

        conn.commit()
        print("База данных готова к использованию!")

    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()


def add_employer(conn: extensions.connection, employer: dict) -> None:
    """Вставляет данные о работодателе или компании в таблицу employers."""
    if not all(key in employer for key in ["id", "name"]):
        print("Отсутствуют обязательные поля id или name")
        return

    command = """
    INSERT INTO employers (employer_id, name, description, url)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (employer_id) DO NOTHING
    """

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            command,
            (
                employer["id"],
                employer["name"],
                employer.get("description"),
                employer.get("alternate_url")
            )
        )
        conn.commit()
        print(f"Работодатель '{employer['name']}' добавлен/обновлен")

    except psycopg2.DatabaseError as e:
        conn.rollback()
        print(f"Ошибка базы данных при добавлении работодателя: {e}")
    except Exception as e:
        conn.rollback()
        print(f"Неизвестная ошибка при добавлении работодателя: {e}")
    finally:
        if cursor:
            cursor.close()


def add_vacancy(conn: extensions.connection, vacancy: dict) -> None:
    """Вставляет данные о вакансии в таблицу vacancies."""

    if not all(key in vacancy for key in ["id", "name", "employer"]):
        print("Отсутствуют обязательные поля в вакансии")
        return

    if not all(key in vacancy["employer"] for key in ["id"]):
        print("Отсутствует id работодателя")
        return

    command = """
    INSERT INTO vacancies (vacancy_id, employer_id, name, description, salary, url)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (vacancy_id) DO NOTHING
    """

    cursor = None
    try:
        cursor = conn.cursor()

        # Получаем данные о зарплате
        salary_data = vacancy.get("salary", {})
        salary_from = salary_data.get("from") if salary_data else None

        cursor.execute(
            command,
            (
                vacancy["id"],
                vacancy["employer"]["id"],
                vacancy["name"],
                vacancy.get("description"),
                salary_from,
                vacancy.get("alternate_url"),
            ),
        )
        conn.commit()
        print(f"Вакансия '{vacancy['name']}' добавлена/обработана")

    except psycopg2.DatabaseError as e:
        conn.rollback()
        print(f"Ошибка базы данных при добавлении вакансии: {e}")
    except Exception as e:
        conn.rollback()
        print(f"Неизвестная ошибка при добавлении вакансии: {e}")
    finally:
        if cursor:
            cursor.close()

# create_db()
# conn = get_db_connection()
# create_tables(conn)
# for employer in companies:
#     add_employer(conn, employer)
#
# vacancy_data = {
#     "id": 1001,
#     "name": "Python Developer",
#     "employer": {"id": 1740, "name": "Яндекс"},
#     "salary": {"from": 150000, "to": 250000, "currency": "RUR"},
#     "alternate_url": "https://hh.ru/vacancy/1001",
#     "description": "Разработка на Python",
#     "snippet": {"requirement": "Python 3+", "responsibility": "Разработка"}
# }
#
# add_vacancy(conn, vacancy_data)