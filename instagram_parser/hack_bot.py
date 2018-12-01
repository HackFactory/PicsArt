import os
import sys
import cv2
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
    
    
    def parse_all_followers(self, my_account):
        """
        """
        followers_ids = self.bot.get_user_followers(my_account)
        followers_names = []
        for pers in followers_ids:
            followers_names.append(self.bot.get_username_from_userid(pers))
        return followers_names
        
        
    def get_json_profile(self, my_account):
        followers_names = self.parse_all_followers(my_account)
        res = {}
        for usr in followers_names:
            avatar_link = self.get_avatar_url(usr)
            res[usr] = [avatar_link]
            links = self.get_media_urls(usr, max_photos=5)
            res[usr].extend(links)
        return res
        
        
        
        
        


