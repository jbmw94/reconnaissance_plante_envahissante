from flask import Flask, render_template,session,  request, redirect, flash, url_for
import flask_login
import main
import urllib.request
from app import app, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from main import getPrediction
from mongoconnect import connection_mongo, insert_data, search_data, nom_ref
from geolocalisation import coord
from search_info import note
import os
import keras
import numpy
import tensorflow
import flask
from sqlconnect import role, connect, seach_user, create_account, check_user, good_password, password_exist, search_code
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
#import pillow


 
# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         result = request.form
#         n = result['adresse']
#         return n
#     else:
#         return render_template(URL_INDEX)
# @app.route('/')
# def index : 
#     return render_template(, title = 'Accueil')

# @app.route('/profil')
# def profil (): 
#     return render_template(profil.html, title ='Profil')


# @app.route('/login', methods= ['POST', 'GET'])
# def login() : 
#     username = request.form('username')
#     pasword = request.form('pasword')
#     if username == user['username'] and password == user['password']:
            
#             session['user'] = username
#             return redirect('/dashboard')



URL_LOGIN = "login.html"
URL_PROFILE = 'profile.html'
URL_SIGNUP = "signup.html"
URL_RESULT = "resultat2.html"
URL_INDEX = "index2.html"

@app.route('/', methods = ['POST', 'GET'])
def login (): 
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('username')
        password = request.form.get('password')
        session['webmail'] = email
        print(email, name, password)

        #iden = seach_user(email,  password, name)
        user_exist = check_user(email)
        if user_exist == 'True':
            print("utilisateur existant")
            good_id = good_password(email, password, name)
            # if good_id == "valid" :
            #     user = User()
            #     user.id = email
                # flask_login.login_user(user)
            print("authentifié")
            return redirect(url_for("profile"))
        else:
            print("mauvais mot de passe")
            wrong="le mot de passe est faux"
            return render_template(URL_LOGIN, wrong=wrong)#envoie message qui dit que le mot de pass est faux
            
        # else:
            
        #      return redirect('/signup')
       
        
    
    return render_template(URL_LOGIN)

@app.route("/profile", methods = ['POST', 'GET'])
def profile () : 
    mail = session.get('webmail', None)
    ID, email, pseudo, lvl, df = role(mail)
    code= search_code(mail)
    phrase = "donné des utilisateur de l'application"
    if lvl == "admin" : 

        return(render_template(URL_PROFILE, email=email, code=code, pseudo=pseudo, lvl=lvl, df=df, phrase=phrase))
    else : 
        return(render_template(URL_PROFILE, email=email, code=code, pseudo=pseudo, lvl=lvl))


@app.route('/signup', methods = ['POST', 'GET'])
def signup (): 
    if request.method=='POST': 
        email = request.form.get('mail')
        name = request.form.get('username')
        password = request.form.get('password')
        checkpassword= request.form.get('checkpassword')
        check_mail = check_user(email)
        check_password = password_exist(password)
       

        if check_mail == 'True' : 
            phrase = "un compte avec ce mail  existe déja"
            return render_template(URL_SIGNUP, phrase=phrase)
        else :
            pass 
        if check_password == 'indisponible' :
            phrase2 = "ce mot de passe existe déja"
            return render_template(URL_SIGNUP, phrase2=phrase2) 
        else : 
            pass
        if password==checkpassword : 

            create_account(email,  password, name)

            print(email, name, password)
            return redirect(url_for("submit_file"))
        else : 
            erreur = "le mot de passe doit être le même que celui tapé en vérification"
            return render_template(URL_SIGNUP, erreur=erreur)

    return render_template(URL_SIGNUP)

# app.route("/bienvenue", methods = ["POST", "GET"])
# def thank ():
#     return render_template("bienvenue.html")




    

@app.route('/analyse', methods=['POST', 'GET'])
def submit_file():
    

    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            getPrediction(filename)
            #label,
            #acc 
            prediction, probability = getPrediction(filename)

            if probability >0.9 : 
                redirect('/resultat')
                
                flash(prediction)
                #flash(label)
                flash(probability)
                flash(filename)
                
                location = request.form["adresse"]
                if location == "" :
                    requete = "vous n'avez pas donnée d'adresse"
                    return render_template(URL_INDEX, requete=requete) 
                else : 

                    
                    img_path = "/static/img_comparaison/"+prediction+".png"
                    #img_source = '../'+filename
                    print(img_path)
                    img_source = "/static/img_save/"+filename
                    
                    print (img_source)
                   

                    url_loc = "localhost"
                    code = 27017
                    data = "projet_final"
                    collection = "plante_collection"
                    sinfun, cursor, entries = connection_mongo(url_loc, code, data, collection) 
                    cd_name, verna = search_data(prediction, sinfun)
                    wiki_search = nom_ref(prediction)

                    # url_link_inpn = 'https://inpn.mnhn.fr/espece/cd_nom/'+cd_name
                    # url_link_wiki = 'https://fr.wikipedia.org/wiki/' + wiki_search
                    doc_inpn, doc_wiki1, doc_wiki2, doc_wiki3, doc_wiki4, doc_wiki_systematique=note(wiki_search, cd_name)

                    #print(url_link)

                    return render_template('/' + URL_RESULT, adresse=location, prediction=prediction, img_path=img_path, img_source=img_source, url_link=doc_inpn, url_wiki=doc_wiki1)




            elif probability >0.8 : 
                img_path = "/static/img_comparaison/"+prediction+".png"
                img_source = "/static/img_save/"+filename
                print(img_source)
                print(img_path)
                phrase ="metter une autre image, le résultat n'est pas certain, voici le résultat le plus probable"
                avec = "avec une probabilité de "
                phrase2 = "voici votre image"
                phrase3 = "voici une image de la plante probable"
                return render_template('/' + URL_INDEX, prediction=prediction, probabilité = probability,avec=avec, phrase2=phrase2, phrase3=phrase3, phrase=phrase, img_path=img_path, img_source=img_source)
            else : 
                phrase = "cela ne correspond pas a une plante envahisante, voulez vous analyser une autre image"
                return render_template('/' + URL_INDEX, phrase=phrase)
    else:
        return render_template(URL_INDEX)
    return render_template(URL_INDEX)
            

@app.route('/resultat',methods = ['POST', 'GET'])


def resultat():

    # result = request.form
    # n = result['adresse']
    #recupération des donné: 
    location = request.form["adresse"]
    print(location)
    url_loc = "localhost"
    code = 27017
    data = "projet_final"
    collection = "location plante"
    sinfun, cursor, entries = connection_mongo(url_loc, code, data, collection) 
    insert_data("plante", location, sinfun)



    return render_template(URL_RESULT, adresse=location)
        
# @app.route('/db-update',methods = ['POST', 'GET'])
# def update():
   # prediction, probability = getPrediction(filename)
    


if __name__ == '__main__':
    app.run(debug=False)
