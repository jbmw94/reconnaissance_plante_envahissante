import sqlite3
from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask.globals import request
import pandas as pd

DB_NAME_PLANTE = "plante_location"
DB_NAME_LOGIN = "login3_db"

TABLE_PLANTE = "location_plante"
TABLE_USERS = "Users"

def insert_request(table, columns):
    sql_request = "INSERT INTO " + table + " ("
    sql_values = " VALUES("
    i=0
    while i < len(columns):
        sql_request += columns[i] + ("," if i < len(columns)-1 else ")" )
        sql_values += "?" + ("," if i < len(columns)-1 else ")" )
        i +=1
    
    return sql_request + sql_values

def select_request(table):
    return "SELECT * FROM " + table

"""
columns : string (example '*' or 'id, name' ) , array of string or dict ({col, alias} or {col})
"""
def select_request(table, columns,where=""):
    cols = "" 
    i = 0
    if( isinstance(columns, str)):
        cols = columns
    else : 
        while i < len(columns):
            if (isinstance(columns[i], str)):
                cols += columns[i]
            else:
                cols += " " + columns[i]["col"] + ( " as " + columns[i]["alias"] if "alias" in columns[i] else "")
            cols += (", " if i < len(columns)-1 else " " )
            i +=1
     
    return "SELECT " + cols + " FROM " + table + ( " WHERE " + where if where else "")
   


    
def connect(prediction, location, img_source):
    try : 
        con_plante= sqlite3.connect(DB_NAME_PLANTE)

        cur_plante = con_plante.cursor()
        print("Connexion réussie à SQLite")
       
        sql = insert_request(TABLE_PLANTE, ["plante", "adresse", "img"])
        value = (prediction, location, img_source)
        cur_plante.execute(sql, value)    
       
        con_plante.commit()
        req = select_request(TABLE_PLANTE)
        result = cur_plante.execute(req)
        
        print("Enregistrement inséré avec succès dans la table person")
        cur_plante.close()
        con_plante.close()
        print("Connexion SQLite est fermée")
        
        return(result)
    except sqlite3.Error as error:
        print("Erreur lors de l'insertion dans la table person", error)

def role (mail) : 
    con_role = sqlite3.connect(DB_NAME_LOGIN) 
    cur_role = con_role.cursor()
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
    cur_role.close()
    con_role.close()
    return ID, email, pseudo, lvl, df

    
def search_code(mail):
    con_code = sqlite3.connect(DB_NAME_LOGIN) 
    cur_code = con_code.cursor()
    password_list = cur_code.execute(select_request(TABLE_USERS, "password", f"mail ='{mail}'"))  
    for row in password_list : 
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
    conn= sqlite3.connect(DB_NAME_LOGIN)

    cur = conn.cursor()
    print("Connexion réussie à SQLite")

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

    cur.close()
    conn.close()
    return isExist

    
                        
def create_account(mail, pasword, username) : 
    conect= sqlite3.connect(DB_NAME_LOGIN)
    curs = conect.cursor()
    sql = insert_request(TABLE_USERS, ["mail", "password", "username", "rôle"])

    if mail=="jb.mw@orange.fr":        
        value = (mail,  pasword, username, "admin")
    else :
        value = (mail,  pasword, username, "user")


    curs.execute(sql, value)    
    conect.commit()
            
    print("Enregistrement inséré avec succès dans la table Users")
    curs.close()
    conect.close()
    print("Connexion SQLite est fermée")
    

def check_user(mail) : 
    con_check= sqlite3.connect(DB_NAME_LOGIN)

    cur_check = con_check.cursor()
    
    cur_check.execute(select_request(TABLE_USERS, "*", f"mail ='{mail}'")) 
    resultat = list(cur_check)



    if len(cur_check.fetchall())==0 : 
        find = "False"
    else :
        #len(resultat) == 1
        find = "True"

    cur_check.close()
    con_check.close()
    return find



def good_password (mail, password, username): 
    con_pas= sqlite3.connect(DB_NAME_LOGIN)

    cur_pas = con_pas.cursor()
    print("Connexion réussie à SQLite")
    
    cur_pas.execute(select_request(TABLE_USERS, "*", f"mail = '{mail}' AND password = '{password}' AND username =  '{username}'"))
    resultat = list(cur_pas)


    if len(cur_pas.fetchall())==0 : 
        auth = "fail"
    else :
        # if len(resultat) == 1:
        auth = "valid"
    
    cur_pas.close()
    con_pas.close()
    return auth

def password_exist(password) : 
    con_check= sqlite3.connect(DB_NAME_LOGIN)

    cur_check = con_check.cursor()
    
    cur_check.execute(select_request(TABLE_USERS, "*", f"password = '{password}'")) 
    resultat = list(cur_check)


    if len(resultat) == 1:
        find = "indisponible"
        

        return find
    elif len(cur_check.fetchall())==0 : 
        find = "False"
        return find
    cur_check.close()
    con_check.close()




            
