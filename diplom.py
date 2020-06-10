import requests
from time import sleep
import json

class User:

    def __init__(self, user_name):
        self.token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
        self.v = '5.107'
        self.url = 'https://api.vk.com/method/execute?'
        self.user_name = user_name

    def execute(self):
        params = {
            'access_token': self.token,
            'v': self.v,
            # 'code': 'return API.groups.getMembers({"group_id": API.groups.get({"user_id": "171691064"}), "filter":"friends"});'

            'code': f'''
            var user_get = API.users.get({{"user_ids":"{self.user_name}"}})@.id;
            var group_id = API.groups.get({{"user_id": user_get}});
            var friends_on_groups = API.groups.getMembers({{"group_id": group_id, "filter":"friends"}});
            if(friends_on_groups.count == 0){{
            var total = API.groups.get({{"user_id": user_get,"fields":"members_count", "extended":1}}).items;
            return total;
            }}
            '''
        }
        r = requests.get(self.url, params).json()
        with open('list.json', 'w') as f:
            f.write(json.dumps(r['response'], sort_keys=True,
                               indent=4, ensure_ascii=False, separators=(',', ': ')))


if __name__ == '__main__':
    user_name = input('Введите имя пользователя или его ID: ').strip()
    user = User("" + user_name + "")
    user.execute()

# 171691064
# eshmargunov
