from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
#insérer le modèle utilisé ici
from keras.applications.inception_v3 import InceptionV3

from fastai.vision import *
from fastai.vision import load_learner, open_image
from app import UPLOAD_FOLDER
upload = UPLOAD_FOLDER

MAIN_FOLDER = "C:/Users/utilisateur/Desktop/projet chef-d'oeuvre"

def getPrediction(filename):
    """"
    model2 = InceptionV3(
    include_top=True, weights='imagenet', input_tensor=None,
    input_shape=None, pooling=None, classes=1000,
    classifier_activation='softmax')

    #model = VGG16()
    image = load_img(upload+filename, target_size=(299, 299))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    yhat = model2.predict(image)
    label = decode_predictions(yhat)
    label = label[0][0]
    print('%s (%.2f%%)' % (label[1], label[2]*100))
    return label[1], label[2]*100
    """""
   
   
    learn = load_learner(MAIN_FOLDER)
    img = open_image(upload+filename)
    pred,pred_idx,probs = learn.predict(img)
#lbl_pred = widgets.Label()
    prediction = str(f'{pred}')
    Probability = float( f'{probs[pred_idx]:.04f}')
    return prediction, Probability
    

def pred_test(image_path:str):
    learn = load_learner(MAIN_FOLDER)
    img = open_image(upload+image_path)
    pred_class,pred_idx,outputs = learn.predict(img)
    yhat = pred_class.obj
    print (yhat)
    return yhat


# pred_test("Acacia saligna (Labill.) H.L.Wendl., 1820 (22)")
"""<p>
		

		<label>adresse</label>
		<input id="adress2" type="text", name="adresse"/>
		
	</p>
"""
# <script language="javascript">
# 	var prediction = document.getElementById("valpred");


# 	function check(prediction){
# 		if (prediction>0.90){
# 			function Adresse (form2){
# 				let adress =document.form2.input.value;

# 				return adress
				
# 				} 
# 			}
# 		}
