from keras.applications.mobilenet_v2 import MobileNetV2
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ModelEmb:
    
    def __init__(self):
        #init model
        self.model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        
    def run(self, img):
        assert img.shape[1:] == (224, 224, 3)
        img = preprocess_input(img)
        features = self.model.predict(img)
        return features.sum(axis=1).sum(axis=1).mean(axis=0).reshape(1, -1)
    
    def run_path(self, path):
        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        return self.run(x)
