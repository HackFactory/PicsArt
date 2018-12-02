import os
from io import open

from tqdm import tqdm

from . import delay


def upload_photo(self, photo, caption=None, upload_id=None):
    delay.small_delay(self)
    if super(self.__class__, self).uploadPhoto(photo, caption, upload_id):
        self.logger.info("Photo '%s' is %s ." % (photo, 'uploaded'))
        return True
    self.logger.info("Photo '%s' is not %s ." % (photo, 'uploaded'))
    return False


def download_photo(self, media_id, path='photos/', filename=None, description=False):
#     delay.very_small_delay(self)
    
    try:
        link = super(self.__class__, self).downloadPhoto(media_id, filename, False, path)
    except Exception:
        link = None
        
    return link


def download_photos(self, medias, path, max_photos=10, description=False):
    broken_items = []
    if not medias:
        self.logger.info("Nothing to downloads.")
        return broken_items
    self.logger.info("Going to download %d medias." % (len(medias)))
    list_links = []
    for media in tqdm(medias):
        link = self.download_photo(media, path, description=description)
        if link is not None:
            list_links.append(link)
        print("len links = {}".format(len(list_links)))
        if len(list_links) == max_photos:
            break
         
    return list_links
        

