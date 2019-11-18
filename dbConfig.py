import pyodbc
import env
curEnv=env.env()
#print(curEnv["username"])
#print(curEnv["password"])
def dbcon():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server='+curEnv["dbserver"]+';'
                          'Database='+curEnv["Database"]+';'
                          'UID='+curEnv["username"]+';'
                          'PWD='+curEnv["password"]+';'
                          'Trusted_Connection=NO;')
    conn.autocommit = True
    return conn

