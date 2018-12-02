from keras.applications.mobilenet_v2 import MobileNetV2
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

from sklearn.metrics.pairwise import cosine_similarity

from skimage import io
import numpy as np

from functools import partial

from operator import itemgetter
ig1 = itemgetter(1)


class ModelEmb:
    
    def __init__(self):
        self.img_nrows = 224
        self.img_ncols = 224
        
        self.base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        self.model._make_predict_function()
        
        self.content_layer = 'block_7_depthwise_relu'
        self.model_content = Model(inputs=self.base_model.input, outputs=base_model.get_layer(content_layer).output)
        self.model_content._make_predict_function()
        
        self.style_layers = ['block_3_depthwise_relu', 'block_5_depthwise_relu',
                             'block_7_depthwise_relu']
        self.models_style = []
        for layer in self.style_layers:
            self.models_style.append(Model(inputs=self.base_model.input, 
                                           outputs=self.base_model.get_layer(layer).output))
            self.models_style[-1]._make_predict_function()
            
            
    def update_urls(self, list_urls):
        self.list_urls = list_urls
        self.num = len(list_urls)
    
    
    def get_sim(self, img, urls, mode='emb') -> float:
        assert mode in {'emb', 'style', 'content'}
        imgs = self.preprocess(urls)
        res = sum(map(getattr(self, 'metric_' + mode), [img]*len(urls), imgs)) / len(urls)
        return res
    
    
    def metric_emb(self, img1, img2):
        img1_emb = self.base_model.predict(img1)
        img1_emb = img1_emb.sum(axis=1).sum(axis=1).mean(axis=0).reshape(1, -1)
        img2_emb = self.base_model.predict(img2)
        img2_emb = img2_emb.sum(axis=1).sum(axis=1).mean(axis=0).reshape(1, -1)
        return float(1 - cosine_similarity(img1_emb, img2_emb))
    
    
    def gram_matrix(x):
        features = x.reshape(x.shape[1] * x.shape[2], -1)
        gram = features @ features.T
        return gram


    def style_loss(x, y):
        S = gram_matrix(x)
        C = gram_matrix(y)
        channels = 3
        size = img_nrows * img_ncols
        return ((S - C) ** 2).sum() / (4.0 * (channels ** 2) * (size ** 2))


    def content_loss(x, y):
        return ((x - y) ** 2).sum()
    
    def metric_content(self, img1, img2):
        img1_content = self.model_content.predsict(img1)
        img2_content = self.model_content.predict(img2)
        C_loss = content_loss(img1_content, img2_content)
        return C_loss
    
    
    def metric_style(self, img1, img2):
        S_loss = 0
        for style_model in self.models_style:
            img1_style = style_model.predict(img1)
            img2_style = style_model.predict(img2)
            S_loss += style_loss(img1_style, img2_style)
        return S_loss
    
    
    def recs(self, img, mode='emb'):
        func = partial(self.get_sim, mode=mode)
        return sorted(enumerate(map(func, [emb]*self.num, self.list_urls)), key=ig1)