TABLE_PLANTE = "location_plante"

def insert_request(table, columns):
    sql_request = "INSERT INTO " + table + " ("
    sql_values = " VALUES("
    i=0
    while i < len(columns):
        sql_request += columns[i] + ("," if i < len(columns)-1 else ")" )
        sql_values += "?" + ("," if i < len(columns)-1 else ")" )
        i +=1
    
    return sql_request + sql_values

def select_all_request(table):
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
   

def connection():
    print(insert_request(TABLE_PLANTE, ["plante", "adresse", "img"]))
    print(select_all_request(TABLE_PLANTE))
    columns = [{"col":"role", "alias":"role"}, {"col":"test"}, "hello"]
    print(select_request(TABLE_PLANTE, columns, "role=user"))
    print(select_request(TABLE_PLANTE, "*", "role=user"))
    mail = "gwen@gmail.com"
    print(select_request(TABLE_PLANTE, ["rôle"], f"mail ='{mail}"))

connection()
