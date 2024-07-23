from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import cast, Optional, Dict, Any, List, Tuple, TypedDict
from urllib import request
import json


class SiteCrawler:
    def __init__(self, site_link: str = '') -> None:
        self.base_link = site_link

    def get_items(self, many: bool, searched_item: str, searched_attribute: str, searched_value: str):
        if many:
            data = self.bs_source.findAll(
                searched_item, {searched_attribute: searched_value})
        else:
            data = self.bs_source.find(
                searched_item, {searched_attribute: searched_value})
        return data

    def get_metadata(self, keys: List[str]):
        path = f'{self.base_link}/offer/'
        self.open_site(path)
        SEARCHED_ITEM = 'script'
        SEARCHED_ATTRIBUTE = 'id'
        SEARCHED_VALUE = 'filters-data'
        data: Optional[Tag] = cast(Tag, self.get_items(
            False, SEARCHED_ITEM, SEARCHED_ATTRIBUTE, SEARCHED_VALUE)) or None
        json_data: Dict[str, Dict[str, str]] = {}
        response:  Dict[str, Dict[str, str]] = {}
        if data is not None:
            json_data = json.loads(data.text)
        for key in keys:
            if key in json_data and json_data[key]:
                response[key] = json_data[key]
        return response

    def get_semesters(self):
        path = f'{self.base_link}/courses/'
        self.open_site(path)
        SEARCHED_ITEM = 'a'
        SEARCHED_ATTRIBUTE = 'class'
        SEARCHED_VALUE = 'semester-link'
        data: List[Tag] = cast(List[Tag], self.get_items(
            True, SEARCHED_ITEM, SEARCHED_ATTRIBUTE, SEARCHED_VALUE)) or []

        semesters: List[Tuple[str, str]] = list(filter(lambda x: x[0] != '' and x[1] != '', [cast(Tuple[str, str], (semester.get('href'), semester.text)) if semester.get(
            'href') and len(semester.text) else ('', '') for semester in data]))
        return semesters

    def get_semester_data(self, semester: str, file_name: str):
        semester_link = f'{self.base_link}{semester}'
        print(semester_link, file_name)
        self.fetch_site(semester_link, file_name)

    def get_semester_subjects(self, semester):
        path = f'{self.base_link}{semester}'
        print(path)
        SEARCHED_ITEM = 'script'
        SEARCHED_ATTRIBUTE = 'id'
        SEARCHED_VALUE = 'courses-data'
        self.open_site(path)
        data: Optional[Tag] = cast(Tag, self.get_items(
            False, SEARCHED_ITEM, SEARCHED_ATTRIBUTE, SEARCHED_VALUE)) or None

        json_data: List[Dict[str, Any]] = []
        if data:
            json_data = json.loads(data.text)

        return json_data

    def get_subject_details(self, link: str) -> int:
        path = f'{self.base_link}{link}'
        self.open_site(path)
        SEARCHED_ITEM = 'table'
        SEARCHED_ATTRIBUTE = 'id'
        SEARCHED_VALUE = 'table-info'
        table: Optional[Tag] = cast(Tag, self.get_items(
            False, SEARCHED_ITEM, SEARCHED_ATTRIBUTE, SEARCHED_VALUE)) or None
        ects_value = 0
        if table:
            rows: List[Tag] = cast(List[Tag], table.find_all('tr'))

            for row in rows:
                th = row.find('th')
                if th and 'ECTS' in th.get_text():
                    td = row.find('td')
                    if td:
                        ects_value = int(td.get_text(strip=True))
                        break
        return ects_value

    def fetch_site(self, link, name) -> None:
        with request.urlopen(link) as response:
            data = response.read()
            with open(name, 'wb') as file:
                file.write(data)

    def get_semester_courses(self):
        pass

    def open_site(self, path: str):
        with request.urlopen(path) as response:
            self.bs_source = BeautifulSoup(response, 'lxml')


if __name__ == '__main__':
    sc = SiteCrawler('https://zapisy.ii.uni.wroc.pl')
