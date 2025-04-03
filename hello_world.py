#print('Hello from Dmitriy')
from requests import get

url = 'https://playground.learnqa.ru/api/get_text'

response = get(url)
print(response.text)