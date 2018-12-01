import os
import sys
import cv2
from pathlib import Path
from instabot import Bot

sys.path.append(os.path.join(sys.path[0], '../'))


def download_from_account(account, max_photos=None):
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

    bot = Bot()
    bot.login()
    medias = bot.get_total_user_medias(account)
    
    list_links = bot.download_photos(medias, max_photos=max_photos)
        
    return list_links


def upload_photos_from_account(path_to_dir):
    """
    :param path_to_dir: path to photos from account.
    :return: list with photos in BRG

    :raises RuntimeError if no photos were found.
    """

    path_to_dir = Path(path_to_dir)
    path_to_dir = str(path_to_dir) + '/'
    photos = os.listdir(path_to_dir)

    list_of_photos = []
    for file in photos:
        current_path = Path(path_to_dir) / file
        current_path = str(current_path)
        list_of_photos.append(cv2.imread(current_path))

    if len(list_of_photos) == 0:
        raise RuntimeError('Photos were not found in {}'.format(path_to_dir))

    return list_of_photos
