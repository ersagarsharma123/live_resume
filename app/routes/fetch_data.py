import requests


def get_data():
    # url = "https://api.damanplatform.com/api/webapi/GetNoaverageEmerdList"
    url = "https://api.damanapiopawer.com/api/webapi/GetNoaverageEmerdList"

    payload = "{\"pageSize\":10,\"pageNo\":1,\"typeId\":30,\"language\":0,\"random\":\"deca7fec07934ff984aa9a72ff4bf524\",\"signature\":\"83747B4479D0E8D0E6A276AD81F1EE4E\",\"timestamp\":1742809529}"
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'ar-origin': 'https://damangames.bet',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzQyODA4MTAyIiwibmJmIjoiMTc0MjgwODEwMiIsImV4cCI6IjE3NDI4MDk5MDIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIzLzI0LzIwMjUgMzoyMTo0MiBQTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6Ijc1NTgxOCIsIlVzZXJOYW1lIjoiOTE4MTA4NDY0NjQ1IiwiVXNlclBob3RvIjoiaHR0cHM6Ly9hcGkubGlnaHRzcGFjZWNkbi5jb20vaW1nL2F2YXRhci5jZmE4ZGQ5ZC5zdmciLCJOaWNrTmFtZSI6IlNhZ2FyIiwiQW1vdW50IjoiMy4yMyIsIkludGVncmFsIjoiMCIsIkxvZ2luTWFyayI6Ikg1IiwiTG9naW5UaW1lIjoiMy8yNC8yMDI1IDI6NTE6NDIgUE0iLCJMb2dpbklQQWRkcmVzcyI6IjEzOS41LjMwLjkzIiwiRGJOdW1iZXIiOiIwIiwiSXN2YWxpZGF0b3IiOiIwIiwiS2V5Q29kZSI6Ijk4NyIsIlRva2VuVHlwZSI6IkFjY2Vzc19Ub2tlbiIsIlBob25lVHlwZSI6IjAiLCJVc2VyVHlwZSI6IjAiLCJVc2VyTmFtZTIiOiIiLCJpc3MiOiJqd3RJc3N1ZXIiLCJhdWQiOiJsb3R0ZXJ5VGlja2V0In0.xRUqsZqFkXbM0AHH7IyVF8xEa6MR-e4M8tNxicn5EA0',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://damangames.bet',
    'priority': 'u=1, i',
    'referer': 'https://damangames.bet/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    data = json_data.get('data').get('list')[0]
    number = int(data.get('number'))
    last_sb = None
    if number < 5:
        last_sb = 's'
    else:
        last_sb = 'b'
    # print(response.text)
    return last_sb


def get_balance():
    import requests
    try:
        
        url = "https://api.damanapiopawer.com/api/webapi/GetBalance"

        payload = "{\"language\":0,\"random\":\"75a46d8c50e146c6919abb176ceb9aa2\",\"signature\":\"6A2D74D42E8EF626736B30B224B464B9\",\"timestamp\":1743785738}"
        headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'ar-origin': 'https://damangames.bet',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzQzNzg1NTM1IiwibmJmIjoiMTc0Mzc4NTUzNSIsImV4cCI6IjE3NDM3ODczMzUiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI0LzQvMjAyNSAxMDo1MjoxNSBQTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6Ijc1NTgxOCIsIlVzZXJOYW1lIjoiOTE4MTA4NDY0NjQ1IiwiVXNlclBob3RvIjoiaHR0cHM6Ly9hcGkubGlnaHRzcGFjZWNkbi5jb20vaW1nL2F2YXRhci5jZmE4ZGQ5ZC5zdmciLCJOaWNrTmFtZSI6IlNhZ2FyIiwiQW1vdW50IjoiMTQ1LjM4IiwiSW50ZWdyYWwiOiIwIiwiTG9naW5NYXJrIjoiSDUiLCJMb2dpblRpbWUiOiI0LzQvMjAyNSAxMDoyMjoxNSBQTSIsIkxvZ2luSVBBZGRyZXNzIjoiMTM5LjUuMjYuMTc0IiwiRGJOdW1iZXIiOiIwIiwiSXN2YWxpZGF0b3IiOiIwIiwiS2V5Q29kZSI6IjEwNzMiLCJUb2tlblR5cGUiOiJBY2Nlc3NfVG9rZW4iLCJQaG9uZVR5cGUiOiIwIiwiVXNlclR5cGUiOiIwIiwiVXNlck5hbWUyIjoiIiwiaXNzIjoiand0SXNzdWVyIiwiYXVkIjoibG90dGVyeVRpY2tldCJ9.z_PJsGG_d-AXcb0vXUCs7uAgsisoEqivyaYUNmCnJpc',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://damangames.bet',
        'priority': 'u=1, i',
        'referer': 'https://damangames.bet/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        balace = 0
        json_data = response.json()
        print('json_data_balance==',  json_data)
        data = json_data.get('data').get('amount')
    except Exception as e:
        print('e==', e)
    return data
    



