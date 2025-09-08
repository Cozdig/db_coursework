import requests
from src.config import companies, hh_api


def get_employers():
    """Возвращает информацию о компаниях"""
    employers = []
    for company in companies:
        params = {"employer_id": company["id"]}
        data = requests.get(url=hh_api + "employers/" + str(company["id"]), params=params)
        employers.append({company["name"]: data.json()})
    return employers


def get_vacancies():
    """Возвращает информацию о вакансиях работодателей"""
    vacancies = []
    for company in companies:
        params = {"employer_id": company["id"], "per_page": 100}
        data = requests.get(url=hh_api + "vacancies", params=params)
        vacancies.append(data.json())
    return vacancies


def employers_info():
    employers = get_employers()
    employers_data = []
    for i in employers:
        for employer in i:
            employers_data.append(
                [i[employer]["id"], i[employer]["name"], i[employer]["alternate_url"], i[employer]["open_vacancies"]]
            )
    return employers_data


def vacancies_info():
    vacancies = get_vacancies()
    vacancies_data = []
    for i in vacancies:
        for vacancy in i["items"]:
            vacancies_data.append(
                [
                    vacancy.get("id"),
                    vacancy.get("employer").get("id"),
                    vacancy.get("employer").get("name"),
                    vacancy.get("name"),
                    vacancy.get("salary", {}).get("from") if vacancy.get("salary") else 0,
                    vacancy.get("salary", {}).get("to") if vacancy.get("salary") else 0,
                    vacancy["alternate_url"],
                ]
            )
    return vacancies_data
