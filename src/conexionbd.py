import cx_Oracle

#Connect to Database
#connstr = cx_Oracle.connect("user/password@server/ServiceName")
connstr = "admin/admin123@gestion.c82paqlf0zlv.us-east-1.rds.amazonaws.com:1521/gestion"
try:
    conn = cx_Oracle.connect(connstr)
except Exception as e:
    print("No se pudo conectar a la bd. Error: "+str(e))
else:
    print("Conexion establecida fuck yeaaaah !")
    cnx = True
    cursor = conn.cursor()
    #Execute Query
    cursor.execute("SELECT * FROM usuario ")
    result = cursor.fetchall()

    #Fetch results
    #print(result)
    conn.close()

def getConn():
    if cnx == True:
        conn = cx_Oracle.connect(connstr)
        return conn
    return


