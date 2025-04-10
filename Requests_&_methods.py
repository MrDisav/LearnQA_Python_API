import  requests


URL = 'https://playground.learnqa.ru/ajax/api/compare_query_type'


def any_method(method):
    params = {
        'method' : method
    }
    return params

# 1 question
response = requests.post(url=URL)
print(f'Answer for 1-st question: "{response.text}"')


# 2 question
response_2 = requests.head(url=URL,data=any_method('HEAD'))
print(f'Answer for 2-nd question : "{response_2.status_code}" status code')


# 3 question
response_3 = requests.put(url=URL, data=any_method('PUT'))
try:
    json_response = response_3.json()
    print(f'Answer for 3-rd question: "{json_response['success']}"')
except ValueError:
    print(f'Response has no JSON, contains only "{response.text}"')


#4 question
def output_info()-> str:
    return f'For method {every_method.__name__.upper()} and params {every_params_method} - {response_4.text}'


print('Answers for 4-th question ▼')
methods = [requests.get, requests.post, requests.put, requests.delete]
methods_params = ['GET', 'POST', 'PUT', 'DELETE']
for every_method in methods:
    for every_params_method in methods_params:
        if every_method == requests.get:
            response_4 = every_method(URL, params=any_method(every_params_method))
            if every_method.__name__.upper() != every_params_method and response_4.text == '{"success":"!"}':
                print(output_info())
        else:
            response_4 = every_method(URL, data=any_method(every_params_method))
            if every_method.__name__.upper() != every_params_method and response_4.text == '{"success":"!"}':
                print(output_info())