import sqlite3
from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask.globals import request
import pandas as pd
from constantes import DB_NAME_PLANTE, DB_NAME_LOGIN, TABLE_PLANTE, TABLE_USERS
from sql_request.py import insert_request, select_all_request, select_request 


def conn(db):
    try : 
        con = sqlite3.connect(db)
        cur = con.cursor()
        print("Connexion réussie à SQLite")
        return cur, con
    except sqlite3.Error as error:
        print("Erreur lors de la connexion à SQLite. ", error)


def close(cur, con):
    cur.close()
    con.close()
    print("Connexion SQLite est fermée")

    
def commit(cur, con, sql, value):
    cur.execute(sql, value)    
    con_plante.commit()

def connect(prediction, location, img_source):
    try : 
        cur_plante, con_plante = conn(DB_NAME_PLANTE)
       
        sql = insert_request(TABLE_PLANTE, ["plante", "adresse", "img"])
        value = (prediction, location, img_source)
        commit(cur_plante, con_plante, sql, value)

        req = select_request(TABLE_PLANTE)
        result = cur_plante.execute(req)
        
        print("Enregistrement inséré avec succès dans la table person")
        close(cur_plante, con_plante)
        
        return(result)
    except sqlite3.Error as error:
        print("Erreur lors de l'insertion dans la table person", error)

def role (mail) : 
    cur_role, con_role = conn(DB_NAME_LOGIN)

    role_list = cur_role.execute( select_request(TABLE_USERS, "rôle", f"mail ='{mail}'"))
    for row in role_list : 
        if row[0] == 'admin' : 
       # if role_list == admin : 
            print('vous être admin')
            user = cur_role.execute(select_request(TABLE_USERS, ["ID", "mail", "username", "rôle"]))  
            df = pd.DataFrame(user, columns = ["ID", "mail", "username", "accreditation"])
                    
        else : 
            print("vous êtes user")
            df="none"
            
        show = cur_role.execute(select_request(TABLE_USERS, "*", f"mail ='{mail}'"))    
        for row in show : 
            ID = row[0]
            email = row[1]
            code = row[2]
            pseudo  =row[3]
            lvl =   row[4] 

    close(cur_role, con_role)

    return ID, email, pseudo, lvl, df

    
def search_code(mail):
    cur_code, con_code = conn(DB_NAME_LOGIN)

    password_list = cur_code.execute(select_request(TABLE_USERS, "password", f"mail ='{mail}'"))  
    for row in password_list : 
        code = row[0]
        close(cur_code, con_code)
        return code
    


    # else : 
    #     show = cur_role.execute(f"Select * from Users wheres mail ='{mail}'")
    #     for row in show : 
    #         print("ID : ", row[0])
    #         print("mail : ", row[1])
    #         print("password :", row[2])
    #         print("username  :" , row[3])
                

     

def seach_user (mail, password, username) : 
    cur, conn = conn(DB_NAME_LOGIN)

    isExist = False
    cur.execute(select_request(TABLE_USERS, "*")) 
    if cur.fetchall() == [] : 
        print( 'rediriger vers create account')
        
    else : 
        print(mail, password)
        cur.execute(select_request(TABLE_USERS, "*", f"mail = '{mail}' AND password = '{password}' AND username =  '{username}'"))
        resultat = list(cur)

        if len(resultat) == 1:
            print("vous êtes authentifier")
            isExist =  True
                
        elif len(cur.fetchall())==0 : 
            print("veuiller vous inscrire")

    close(cur, conn)
    return isExist

    
                        
def create_account(mail, pasword, username) : 
    curs, conect = conn(DB_NAME_LOGIN)
    sql = insert_request(TABLE_USERS, ["mail", "password", "username", "rôle"])

    if mail=="jb.mw@orange.fr":        
        value = (mail,  pasword, username, "admin")
    else :
        value = (mail,  pasword, username, "user")

    commit(curs, conect, sql, value)
            
    print("Enregistrement inséré avec succès dans la table Users")
    close(curs, connect)
    

def check_user(mail) : 
    cur_check, con_check = conn(DB_NAME_LOGIN)
    cur_check.execute(select_request(TABLE_USERS, "*", f"mail ='{mail}'")) 

    find = "False " if len(cur_check.fetchall()) == 0 else "True"

    close(cur_check, con_check)
    return find



def good_password (mail, password, username): 
    cur_pas, con_pas = conn(DB_NAME_LOGIN)
    cur_pas.execute(select_request(TABLE_USERS, "*", f"mail = '{mail}' AND password = '{password}' AND username =  '{username}'"))

    auth = "fail " if len(cur_check.fetchall()) == 0 else "valid"

    close(cur_pas, con_pas)
    return auth

def password_exist(password) : 
    cur_check, con_check = conn(DB_NAME_LOGIN)
    cur_check.execute(select_request(TABLE_USERS, "*", f"password = '{password}'")) 
    resultat = list(cur_check)

    find = "indisponible " if len(cur_check.fetchall()) == 0 else "False"

    close(cur_check, con_check)
    return find






            
