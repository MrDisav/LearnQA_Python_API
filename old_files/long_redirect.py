from requests import get

URL = 'https://playground.learnqa.ru/api/long_redirect'

response = get(url = URL)
numbers_of_redirect = len(response.history)

print(f'Numbers of redirect : {numbers_of_redirect}')
print(f'Last URL is {response.history[numbers_of_redirect - 1].url}')