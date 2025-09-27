import requests

class TestPlaceAPI:
    """Класс для работы с Google Maps API"""

    BASE_URL = "https://rahulshettyacademy.com/maps/api/place"
    KEY = "qaclick123"

    def create_location(self, name_suffix=""):
        """Создание новой локации через POST"""
        post_url = f"{self.BASE_URL}/add/json?key={self.KEY}"
        json_body = {
            "location": {"lat": -38.383494, "lng": 33.427362},
            "accuracy": 50,
            "name": f"Frontline house{name_suffix}",
            "phone_number": "(+91) 983 893 3937",
            "address": "29, side layout, cohen 09",
            "types": ["shoe park", "shop"],
            "website": "http://google.com",
            "language": "French-IN"
        }
        r = requests.post(post_url, json=json_body)
        assert r.status_code == 200, "POST статус код не 200"
        place_id = r.json().get("place_id")
        print(f"Создан place_id: {place_id}")


       
        with open("place_id.txt", "a", encoding="utf-8") as f:
            f.write(f"{place_id}\n")
        return place_id

    def delete_location(self, place_id):
        """Удаление локации через DELETE"""
        delete_url = f"{self.BASE_URL}/delete/json?key={self.KEY}"
        r = requests.post(delete_url, json={"place_id": place_id})
        assert r.status_code == 200, f"DELETE ошибка для {place_id}"
        print(f"Удалена place_id: {place_id}")

    def get_location(self, place_id):
        """GET-запрос для проверки существования локации"""
        get_url = f"{self.BASE_URL}/get/json?key={self.KEY}&place_id={place_id}"
        r = requests.get(get_url)
        if r.status_code == 200:
            return True, r.json().get("name")
        else:
            return False, None



api = TestPlaceAPI()
for i in range(5):
    api.create_location(name_suffix=f" {i+1}")



with open("place_id.txt", "r") as f:
    list_place_ids = [line.strip() for line in f]


for index in [1, 3]:  
    api.delete_location(list_place_ids[index])


existing_place_ids = []
non_existing_place_ids = []

for pid in list_place_ids:
    exists, name = api.get_location(pid)
    if exists:
        existing_place_ids.append(pid)
    else:
        non_existing_place_ids.append(pid)



with open("несуществующие place_id.txt", "w") as f:
    for pid in existing_place_ids:
        f.write(f"{pid}\n")


print(f"\nСуществующие place_id: {existing_place_ids}")
print(f"Несуществующие place_id: {non_existing_place_ids}")
