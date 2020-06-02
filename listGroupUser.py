import requests
import json
from pprint import pprint
class User:

	def __init__(self, user1):
		self.user1 = user1

	def get_user(self):
		"""ПОЛУЧАЕТМ ID ПОЛЬЗОВАТЕЛЯ ДЛЯ ДАЛЬНЕЙШЕГО ИСПОЛЬЗОВАНИЯ"""
		URL = 'https://api.vk.com/method/users.get?'
		params = {
			'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
			'user_ids': self.user1,
			'v': '5.107'
		}
		try:
			r = requests.get(URL, params).json()
		except:
			pass
		return r['response'][0]['id'] # ID 171691064

	def get_groups(self):
		"""ПОЛУЧАЕМ СПИСОК ГРУПП В КОТОРЫХ СОСТОИТ ПОЛЬЗОВАТЕЛЬ"""
		list_groups = {}
		URL = 'https://api.vk.com/method/groups.get?'
		params = {'user_id':self.get_user(),
		          'extended':1,
		          'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
		          'fields':'links',
		          'v': '5.107'}
		try:
			r = requests.get(URL, params).json()
			for count_groups, name_group in enumerate(r['response']['items']):
				list_groups[count_groups] = f"https://vk.com/{name_group['screen_name']}"
		except:
			pass
		return list_groups # ФУНКЦИЯ ВОЗВРАЩАЕТ ССЫЛКИ НА ГРУППЫ

	def get_friends(self):
		"""ПОЛУЧАЕМ ДРУЗЕЙ ПОЛЬЗОВАТЕЛЯ"""
		list_id_friends = []
		URL = 'https://api.vk.com/method/friends.get?'
		params = {
			'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
			'user_id': self.get_user(),
			'v': '5.107'
		}
		try:
			r = requests.get(URL, params).json()
			list_id_friends.append(r['response']['items'])
		except:
			pass
		return list_id_friends

	def get_groups_friends(self):
		"""ПОЛУЧАЕМ ГРУППЫ В КОТОРЫХ СОСТОЯТ ДРУЗЬЯ ПОЛЬЗОВАТЕЛЯ"""
		list_friends_groups = {}
		URL = 'https://api.vk.com/method/groups.get?'
		params = {'user_id': self.get_friends(), # ПЕРЕДАЕМ СПИСОК ID ДРУЗЕЙ ДЛЯ ПОЛУЧЕНИЯ ИХ ГРУПП
		          'extended': 1,
		          'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
		          'fields': 'links',
		          'v': '5.107'}
		try:
			r = requests.get(URL, params).json()
			for count_groups, name_group in enumerate(r['response']['items']):
				list_friends_groups[count_groups] = f"https://vk.com/{name_group['screen_name']}"
		except:
			pass
		return list_friends_groups



user = User(171691064)
# s = user.get_user()
# pprint(user.get_groups())
# pprint(user.get_user('eshmargunov'))
# print(user.get_friends())
# pprint(user.get_groups_friends())

if __name__ == '__main__':
    pprint(user.get_groups_friends())