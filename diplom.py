import requests
import json
from pprint import pprint
#from time import sleep


class User:

    def __init__(self, user1):
        self.user1 = user1
        self.URL = 'https://api.vk.com/method/'
        self.params = {
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v': '5.107'
        }

    def get_user(self):
        """ПОЛУЧАЕТМ ID ПОЛЬЗОВАТЕЛЯ"""
        method = 'users.get?'
        self.params['user_ids'] = self.user1
        r = requests.get(self.URL+method, self.params).json()
        return r['response'][0]['id']  # ID 171691064

    def get_groups(self):
        """ПОЛУЧАЕМ ID ГРУПП В КОТОРЫХ СОСТОИТ ПОЛЬЗОВАТЕЛЬ"""
        list_groups = []
        method = 'groups.get?'
        self.params['user_id'] = self.get_user()
        self.params['extended'] = 1
        self.params['fields'] = 'links'
        r = requests.get(self.URL+method, self.params).json()
        for name_group in r['response']['items']:
            list_groups.append(name_group['id'])
        return list_groups

    def get_friends(self):
        """ПОЛУЧАЕМ ID ДРУЗЕЙ ПОЛЬЗОВАТЕЛЯ"""
        list_id_friends = []
        method = 'friends.get?'
        self.params['user_id'] = self.get_user()
        r = requests.get(self.URL+method, self.params).json()
        list_id_friends.append(r['response']['items'])
        return list_id_friends

    def get_groups_friends(self):
        """список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей"""
        s = self.get_friends()
        method = 'groups.get?'
        d = len(s[0])-1
        i = 0
        t = dict()
        groups_friends = []
        while i < d:
            i = i+1
            self.params['user_id'] = s[0][i]
            try:
                r = requests.get(self.URL + method, self.params).json()
                t[self.params['user_id']] = r['response']['items']
            except Exception:
                print('.', end='')
        for m in t.values():
            for h in m:
                groups_friends.append(h)
        groups_user = self.get_groups()
        result = set(groups_user) - set(groups_friends)
        return list(result)

    def get_dict_groups(self):
        """"ЗАПИСЬ ИНФОРМАЦИИ О ГРУППАХ В list.json"""
        v = []
        f = []
        for id_group in self.get_groups_friends():
            method = 'groups.getById?'
            self.params['group_ids'] = id_group
            self.params['fields'] = 'members_count, name, id'
            r = requests.get(self.URL+method, self.params).json()
            [v.append(x) for x in r['response']]
        for d in v:
            f.append({i: d[i] for i in d if i == 'screen_name' or i == 'id' or i == 'members_count'})
        with open('list.json', 'a') as file:
            file.write(json.dumps(f, sort_keys=True,
                                  indent=4, ensure_ascii=False, separators=(',', ':')))


if __name__ == '__main__':
    user_name = input('Введите имя пользователя или его ID: ').strip()
    user = User(user_name)
    user.get_dict_groups()
# 171691064
