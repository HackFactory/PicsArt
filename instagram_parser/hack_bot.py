import os
import sys
import cv2
import time
import random
import numpy as np
from pathlib import Path
from instabot import Bot
sys.path.append(os.path.join(sys.path[0], '../'))

class Hack_bot:
    def __init__(self):
        self.bot = Bot()
        self.bot.login()
        
        
    def get_media_urls(self, account, max_photos=None):
        """
        :param account: @k_artemkaa, @yar.spirin, etc., string.

        :param max_photos: number of maximum photos to download. If None then
        all photos will be downloaded.

        :param path: path to directory where function will save photos.
        If directory doesn't exist it will create it.

        If path is None then function will create directory with name 'photos/account/
        :returns nothing, just downloads
        """
        if not isinstance(account, str):
            raise RuntimeError('Wrong account object, it must be string')

        if account[0] != '@':
            account = "@" + account

        medias = self.bot.get_total_user_medias(account)

        list_links = self.bot.download_photos(medias, max_photos=max_photos)

        return list_links


    def get_avatar_url(self, account):
        """
        """
        data = self.bot.get_user_info(account)
        url = None
        if data.get('profile_pic_url'):
            url = data['profile_pic_url']
        if not url:
            raise TypeError("No profile picture")
        return url
    
    def get_names_from_niks(self,  nicks):
        """
        """
        names = []
        for nick in nicks:
            data = self.bot.get_user_info(nick)
            names.append(data["full_name"])
#     def get_top_friends(self, my_account):
#         my_folls = set(self.parse_all_followers(my_account)[:10])
#         top_friends = {}
#         for i, fol in enumerate(my_folls):
#             print(i, fol)
#             delay = 0.5
# #             time.sleep(delay*3/4 + delay*random.random()/2)
#             self.like_delay(self.bot)
#             try:
#                 him_folls = set(self.parse_all_followers(fol))
#                 intercept_num = len(my_folls & him_folls)
#                 top_friends[fol] = intercept_num
#             except Exception:
#                 top_friends[fol] = 0
#         return sorted(top_friends, key=lambda x: top_friends[x])[:5]
        
    
    def parse_all_followers(self, my_account):
        """
        """
        followers_ids = self.bot.get_user_followers(my_account)[:20]
        followers_names = []
        for pers in followers_ids:
#             delay = 0.25
#             time.sleep(delay*3/4 + delay*random.random()/2)
            followers_names.append(self.bot.get_username_from_userid(pers))
        return followers_names
        
        
    def get_json_profile(self, my_account):
        followers_names = self.parse_all_followers(my_account)
        ids = np.random.choice(np.arange(10), 5, replace=False)
        
        res = {}
        for i in ids:
            
            avatar_link = self.get_avatar_url(followers_names[i])
            res[followers_names[i]] = [avatar_link]
            links = self.get_media_urls(followers_names[i], max_photos=5)
            res[followers_names[i]].extend(links)
        return res
        
    def sleep_if_need(self, last_action, target_delay):
        now = time.time()
        elapsed_time = now - last_action
        if elapsed_time < target_delay:
            remains_to_wait = target_delay - elapsed_time
            time.sleep(add_dispersion(remains_to_wait))
            
    def like_delay(self, bot):
        self.sleep_if_need(bot.last_like, bot.like_delay)
        bot.last_like = time.time()
        
        


