import requests
from src.config import companies, hh_api


def get_employers():
    """Возвращает информацию о компаниях"""
    employers = []
    for company in companies:
        params = {"employer_id":company["id"]}
        data = requests.get(url=hh_api+"employers/"+str(company["id"]), params=params)
        employers.append({company["name"]:data.json()})
    return employers

def get_vacancies():
    """Возвращает информацию о вакансиях работодателей"""
    vacancies = []
    for company in companies:
        params = {"employer_id": company["id"], "per_page": 100}
        data = requests.get(url=hh_api+"vacancies", params=params)
        vacancies.append(data.json())
    return vacancies
