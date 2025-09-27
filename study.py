import requests

class Testing_Google_map_API_PUT_Create_New_Location:
    """
    Я работаю с Google Maps API:
    - создаю новое место через POST
    - проверяю последнее место через GET
    """
    
    def __init__(self, URL_basic, resource1, resource2, body, key):
        # Сохраняю основные данные для работы с API
        self.URL_basic = URL_basic
        self.resource1 = resource1
        self.resource2 = resource2
        self.body = body
        self.key = key
        self.URL1 = f"{self.URL_basic}{self.resource1}?key={self.key}"  # URL для POST

    def POST_request_and_write_text_file(self):
        # Отправляю POST запрос и получаю place_id
        response = requests.post(self.URL1, json=self.body)
        assert response.status_code == 200, "Ошибка POST запроса"

        place_id = response.json().get("place_id")
        assert place_id, "place_id отсутствует"

        # Сохраняю place_id в файл
        with open("my_file.txt", "a", encoding="utf-8") as file:
            file.write(f"{place_id}\n")
        
        return place_id

    def GET_request_check_last_place_id(self):
        # Беру последний place_id из файла
        last_place_id = None
        with open("my_file.txt", "r", encoding="utf-8") as file:
            for line in file:
                clean_line = line.strip()
                if clean_line:
                    last_place_id = clean_line

        if not last_place_id:
            print("Файл пустой, нет place_id для проверки")
            return

        # Отправляю GET запрос и проверяю имя места
        URL_get = f"{self.URL_basic}{self.resource2}?place_id={last_place_id}&key={self.key}"
        response = requests.get(URL_get)
        if response.status_code != 200:
            print(f"Ошибка GET запроса для place_id={last_place_id}")
            return

        data = response.json()
        if data.get("name") == self.body.get("name"):
            print(f"Последний place_id={last_place_id} успешно проверен")
        else:
            print(f"Последний place_id={last_place_id} проверка не пройдена")


# Настройки API
URL_basic = "https://rahulshettyacademy.com"
resource1 = "/maps/api/place/add/json"
resource2 = "/maps/api/place/get/json"
key = "qaclick123"

body = {
    "location": {"lat": -38.383494, "lng": 33.427362},
    "accuracy": 50,
    "name": "Frontline house",
    "phone_number": "(+91) 983 893 3937",
    "address": "29, side layout, cohen 09",
    "types": ["shoe park", "shop"],
    "website": "http://google.com",
    "language": "French-IN"
}

# Создаю объект
new_object = Testing_Google_map_API_PUT_Create_New_Location(
    URL_basic=URL_basic,
    resource1=resource1,
    resource2=resource2,
    body=body,
    key=key
)

# Создаю новое место
res_place_id = new_object.POST_request_and_write_text_file()
print(f"Создан place_id: {res_place_id}")

# Проверяю последнее место
new_object.GET_request_check_last_place_id()