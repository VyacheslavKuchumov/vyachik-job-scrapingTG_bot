import os
import requests
import logging
import time
from pprint import pprint
from datetime import datetime
from dbConnection import db
from SECRET import HH_RU_TOKEN

vyachik_id = 1403125548
import requests
import json

# # Replace with your bot token and recipient's chat ID

from SECRET import TELEGRAM_TOKEN

def bot_send_message( message, chat_id=vyachik_id, bot_token=TELEGRAM_TOKEN):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=params)
    return json.loads(response.text)


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ApiHhRu:
    BASE_URL = 'https://api.hh.ru'
    COUNTRY = 'Россия'
    # AREAS = ['Пермский край', 'Свердловская область', 'Москва', 'Московская область', 'Санкт-Петербург', 'Ленинградская область', 'Республика Татарстан', 'Новосибирская область', 'Краснодарский край', 'Ханты-Мансийский автономный округ', 'Приморский край', 'Челябинская область', 'Калужская область']
    ACCESS_TOKEN = None

    # AREAS = ['Пермский край', 'Свердловская область']
    AREAS = None


    def __init__(self, token, areas):
        self.ACCESS_TOKEN = token
        self.headers = {'Authorization': f'Bearer {self.ACCESS_TOKEN}'}
        self.AREAS = areas

    def _get(self, url, params=None):
        """Helper method for GET requests."""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None

    def fetch_countries(self):
        """Fetches the list of countries."""
        return self._get(f'{self.BASE_URL}/areas/countries') or []

    def find_country_url(self, country_name):
        """Finds the country URL by name."""
        countries = self.fetch_countries()
        return next((country['url'] for country in countries if country['name'] == country_name), '')

    def fetch_areas(self):
        """Fetches areas based on the specified country."""
        country_url = self.find_country_url(self.COUNTRY)
        if not country_url:
            logging.error("Country not found.")
            return []

        areas = self._get(country_url)
        if areas:
            return [area for area in areas.get('areas', []) if area['name'] in self.AREAS]
        return []

    def fetch_professional_roles(self):
        """Fetches the list of professional roles."""
        url = f'{self.BASE_URL}/professional_roles'
        roles = self._get(url)
        # pprint(roles)
        return roles.get('categories', []) if roles else []

    def get_vacancies(self, area_id, professional_role_id, page=0):
        """Fetches vacancies for a given area and role with retry logic."""
        params = {
            'area': area_id,
            'professional_role': professional_role_id,
            'page': page,
            'per_page': 100,
            # 'period': 365
        }
        return self._get(f'{self.BASE_URL}/vacancies', params)

    def fetch_all_vacancies(self, area_id, professional_role_id):
        """Fetches all vacancies for a given area and professional role."""
        vacancies, page, total_pages = [], 0, 1

        while page < total_pages:
            logging.info(f"Fetching page {page} for area {area_id} and role {professional_role_id}")
            data = self.get_vacancies(area_id, professional_role_id, page)

            if not data or 'items' not in data:
                logging.warning("No vacancies found or invalid data.")
                break

            vacancies.extend(data['items'])
            total_pages = data.get('pages', 1)
            page += 1

        return vacancies

    def save_vacancies_to_db(self, vacancies, area_name):
        """Saves vacancies to the database, avoiding duplicates."""
        inserted, duplicates = 0, 0

        for vacancy in vacancies:
            vacancy['entry_date'] = datetime.utcnow().strftime('%d.%m.%Y')
            vacancy['area_name'] = area_name

            if db.find_one({"id": vacancy['id'],
                            "entry_date": vacancy['entry_date']}):
                duplicates += 1
                continue

            try:
                db.insert_one(vacancy)
                inserted += 1
            except Exception as e:
                logging.error(f"Error saving vacancy {vacancy['url']}: {e}")

        bot_send_message(f"Inserted: {inserted}, Duplicates: {duplicates}")
        logging.info(f"Inserted: {inserted}, Duplicates: {duplicates}")

    def fetch_and_store_vacancies(self):
        """Fetches and stores vacancies for all areas and roles."""
        areas = self.fetch_areas()
        if not areas:
            logging.error("No areas found.")
            return

        professional_roles = self.fetch_professional_roles()
        if not professional_roles:
            logging.error("No professional roles found.")
            return

        for area in areas:
            bot_send_message(message=f"Processing area {area['name']} (ID: {area['id']})")
            logging.info(f"Processing area {area['name']} (ID: {area['id']})")
            for category in professional_roles:
                for role in category['roles']:
                    bot_send_message(message=f"Fetching vacancies for role {role['name']} (ID: {role['id']})")
                    logging.info(f"Fetching vacancies for role {role['name']} (ID: {role['id']})")
                    vacancies = self.fetch_all_vacancies(area['id'], role['id'])
                    self.save_vacancies_to_db(vacancies, area['name'])



if __name__ == "__main__":
    job_api = ApiHhRu(token=HH_RU_TOKEN, areas=['Пермский край', 'Свердловская область'])
    job_api.fetch_and_store_vacancies()
