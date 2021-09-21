import sqlite3
from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask.globals import request
import pandas as pd

def connect(prediction, location, img_source):
    try : 
        con_plante= sqlite3.connect("plante_location")

        cur_plante = con_plante.cursor()
        print("Connexion réussie à SQLite")
       
       
        sql = "INSERT INTO location_plante (plante, adresse, img) VALUES (?, ?, ?)"
        value = (prediction, location, img_source)
        cur_plante.execute(sql, value)    
       
        con_plante.commit()
        req = "select * from location_plante"
        result = cur_plante.execute(req)
        
        print("Enregistrement inséré avec succès dans la table person")
        cur_plante.close()
        con_plante.close()
        print("Connexion SQLite est fermée")
        
        return(result)
    except sqlite3.Error as error:
        print("Erreur lors de l'insertion dans la table person", error)

def role (mail) : 
    con_role = sqlite3.connect("login3_db") 
    cur_role = con_role.cursor()
    rank = cur_role.execute(f"select rôle from Users where mail ='{mail}'")
    for row in rank : 
        if row[0] == 'admin' : 
       # if rank == admin : 
            print('vous être admin')
            show = cur_role.execute("Select ID, mail, username, rôle from Users")
            df = pd.DataFrame(show, columns = ["ID", "mail", "username", "accreditation"])
            
            show2 = cur_role.execute(f"Select * from Users where mail ='{mail}'")
            for row in show2 : 
                ID = row[0]
                email = row[1]
                code = row[2]
                pseudo  =row[3]
                lvl =   row[4] 
            return ID, email, pseudo, lvl, df                
                


        else : 
            print("vous êtes user")
            df="none"
            show = cur_role.execute(f"Select * from Users where mail ='{mail}'")
            for row in show : 
                ID = row[0]
                email = row[1]
                code = row[2]
                pseudo  =row[3]
                lvl =   row[4] 
            return ID, email, pseudo, lvl, df
    cur_role.close()
    con_role.close()
    
def search_code(mail):
    con_code = sqlite3.connect("login3_db") 
    cur_code = con_code.cursor()
    rank = cur_code.execute(f"select password from Users where mail ='{mail}'")
    for row in rank : 
       code = row[0]
       return code
    


    # else : 
    #     show = cur_role.execute(f"Select * from Users wheres mail ='{mail}'")
    #     for row in show : 
    #         print("ID : ", row[0])
    #         print("mail : ", row[1])
    #         print("password :", row[2])
    #         print("username  :" , row[3])
                

     

def seach_user (mail, password, username) : 
        
        conn= sqlite3.connect("login3_db")

        cur = conn.cursor()
        print("Connexion réussie à SQLite")
        
        cur.execute("Select * from Users")
        if cur.fetchall() == [] : 
            print( 'rediriger vers create account')
        else : 
           
            print(mail, password)
            cur.execute(f"Select * from Users where mail = '{mail}' AND password = '{password}' AND username =  '{username}'" )
            resultat = list(cur)


            if len(resultat) == 1:
                print("vous êtes authentifier")

                return True
            elif len(cur.fetchall())==0 : 
                print("veuiller vous inscrire")
                return False
        cur.close()
        conn.close()
        

    
                        
def create_account(mail, pasword, username) : 
    conect= sqlite3.connect("login3_db")
    if mail=="jb.mw@orange.fr":
        

        curs = conect.cursor()
        sql = "INSERT INTO Users (mail, password, username, rôle) VALUES (?, ?, ?,?)"
        value = (mail,  pasword, username, "admin")
    else :
        curs = conect.cursor()
        sql = "INSERT INTO Users (mail, password, username, rôle) VALUES (?, ?, ?,?)"
        value = (mail,  pasword, username, "user")


    curs.execute(sql, value)    

    conect.commit()
            
    print("Enregistrement inséré avec succès dans la table Users")
    curs.close()
    conect.close()
    print("Connexion SQLite est fermée")

def check_user(mail) : 
    con_check= sqlite3.connect("login3_db")

    cur_check = con_check.cursor()
    
    cur_check.execute(f"Select * from Users where mail = '{mail}'")
    resultat = list(cur_check)


    if len(resultat) == 1:
        find = "True"
        

        return find
    elif len(cur_check.fetchall())==0 : 
        find = "False"
        return find
    cur_check.close()
    con_check.close()



def good_password (mail, password, username): 
    con_pas= sqlite3.connect("login3_db")

    cur_pas = con_pas.cursor()
    print("Connexion réussie à SQLite")
    

    cur_pas.execute(f"Select * from Users where mail = '{mail}' AND password = '{password}' AND username =  '{username}'" )
    resultat = list(cur_pas)


    if len(resultat) == 1:
        auth = "valid"

        return auth
    elif len(cur_pas.fetchall())==0 : 
        auth = "fail"
        return auth
    cur_pas.close()
    con_pas.close()

def password_exist(password) : 
    con_check= sqlite3.connect("login3_db")

    cur_check = con_check.cursor()
    
    cur_check.execute(f"Select * from Users where password = '{password}'")
    resultat = list(cur_check)


    if len(resultat) == 1:
        find = "indisponible"
        

        return find
    elif len(cur_check.fetchall())==0 : 
        find = "False"
        return find
    cur_check.close()
    con_check.close()




            
