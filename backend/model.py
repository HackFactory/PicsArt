from keras.applications.mobilenet_v2 import MobileNetV2
# from keras.applications.inception_v3 import InceptionV3

from keras.models import Model
from keras.preprocessing import image

from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
# from keras.applications.inception_v3 import preprocess_input, decode_predictions


from sklearn.metrics.pairwise import cosine_similarity

from skimage import io
import numpy as np

from functools import partial

from operator import itemgetter
ig1 = itemgetter(1)


def gram_matrix(x):
    features = x.reshape(x.shape[1] * x.shape[2], -1)
    gram = features @ features.T
    return gram


def style_loss(x, y, img_nrows=224, img_ncols=224):
    S = gram_matrix(x)
    C = gram_matrix(y)
    channels = 3
    size = img_nrows * img_ncols
    return ((S - C) ** 2).sum() / (4.0 * (channels ** 2) * (size ** 2))


def content_loss(x, y):
    return ((x - y) ** 2).sum()


class RankModel(object):
    
    def __init__(self):
        self.img_nrows = 299
        self.img_ncols = 299
        self.num = 1
        
        self.base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(self.img_nrows, self.img_ncols, 3))
#         self.base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(self.img_nrows, self.img_ncols, 3))
        
        self.base_model._make_predict_function()
        
        self.content_layer = 'block_7_depthwise_relu'
        self.model_content = Model(inputs=self.base_model.input, outputs=self.base_model.get_layer(self.content_layer).output)
        self.model_content._make_predict_function()
        
        self.style_layers = ['block_3_depthwise_relu', 'block_5_depthwise_relu',
                             'block_7_depthwise_relu']
        self.models_style = []
        for layer in self.style_layers:
            self.models_style.append(Model(inputs=self.base_model.input, 
                                           outputs=self.base_model.get_layer(layer).output))
            self.models_style[-1]._make_predict_function()
    
    
    def preprocess(self, urls):
        imgs = map(io.imread, urls)
        imgs = map(image.array_to_img, imgs)
        imgs = [img.resize((self.img_nrows, self.img_ncols)) for img in imgs]
        imgs = map(image.img_to_array, imgs)
        imgs = map(preprocess_input, imgs)
        return np.array(list(imgs))
    
    
    def preprocess_image(self, img):
        img = image.array_to_img(img)
        img = img.resize((self.img_nrows, self.img_ncols))
        img = image.img_to_array(img)
        img = preprocess_input(img)
        return np.array([img])
    
    
    def update_urls(self, list_urls):
        self.list_urls = list_urls
        self.num = len(list_urls)
        self.imgs = list(map(self.preprocess, self.list_urls))
    

    def get_sim(self, img, ind, mode='emb') -> float:
        assert mode in {'emb', 'style', 'content'}
        res = sum(map(getattr(self, 'metric_' + mode), [img]*self.num, self.imgs[ind])) / self.num
        return res
    
    
    def metric_emb(self, img1, img2):
        img1_emb = self.base_model.predict(img1)
        img1_emb = img1_emb.sum(axis=1).sum(axis=1).mean(axis=0).reshape(1, -1)
        img2_emb = self.base_model.predict(img2[np.newaxis,:])
        img2_emb = img2_emb.sum(axis=1).sum(axis=1).mean(axis=0).reshape(1, -1)
        
        return float(1 - cosine_similarity(img1_emb, img2_emb))
   
    
    def metric_content(self, img1, img2):
        img1_content = self.model_content.predict(img1)
        img2_content = self.model_content.predict(img2[np.newaxis,:])
        C_loss = content_loss(img1_content, img2_content)
        return C_loss
    
    
    def metric_style(self, img1, img2):
        S_loss = 0
        for style_model in self.models_style:
            img1_style = style_model.predict(img1)
            img2_style = style_model.predict(img2[np.newaxis,:])
            S_loss += style_loss(img1_style, img2_style, self.img_nrows, self.img_ncols)
        return S_loss 
    
    
    def recs(self, img, mode='emb'):
        func = partial(self.get_sim, mode=mode)
        prob = list(map(func, [img]*self.num, range(self.num)))
        print(prob)
        prob = np.array(prob)
        prob /= prob.sum()
        prob = 1 - prob
        prob = (prob - min(prob) ) / ( max(prob) * 1.002 - min(prob))
        recs = sorted(enumerate(prob), key=ig1, reverse=True)
        inds, probs = zip(*recs)
        return list(inds), list(probs)