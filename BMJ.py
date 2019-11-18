import imaplib
import os
import email
import dbConfig
import pyodbc
import shutil
import env
import zipfile
from apireader import apipara
import urllib.request
from zip_extractor import extractor
from log import logerr
import socket
#To set the environment
curEnv=env.env()
urmacno=input("enter ur mac no:")
macno=socket.gethostname()
if urmacno==macno:
    print("Running.....")
    while True:
        try:
            
        #database configuration
            drop=dbConfig.dbcon()
               
            
            
            mail = imaplib.IMAP4_SSL(curEnv["emailhost"])
            mail.login(curEnv["Sourcemail"], curEnv["emailpassword"])
            mail.select('Inbox')
            type, data = mail.search(None,'UNSEEN')
            #if data == mail.search(None,'UNSEEN'):
             #print('true')
            #print(data)
            mail_ids = data[0]
            id_list = mail_ids.split()
            for num in data[0].split():
                typ, data = mail.fetch(num, '(RFC822)')
                raw_email = data[0][1]
            
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                for response_part in data:
                    if isinstance(response_part, tuple):
                            msg = email.message_from_string(
                                response_part[1].decode('utf-8'))
                            email_subject = msg['subject']
                            email_from = msg['from']
                            email_to = msg['to']
                            email_cc = str(msg['cc'])

                            
                            if email_cc == msg['cc']:
                                print ('Cc : ' + email_cc + '\n')
                            else:
                                email_cc = "none"
                                print ('Cc : ' + email_cc + '\n')
                                
                                
                            print ('From : ' + email_from + '\n')
                            print ('Subject : ' + email_subject + '\n')
                            print ('To : ' + email_to + '\n')
                            
                            
                count = 0
                fileName = ''
                fileArr = []
                b=''
                c=''
                cursor = drop.cursor() 
                sql=("INSERT INTO "+curEnv["Database"]+".dbo.BMJ_AssignedJob (fromid,toid,subjectcontent,cc) VALUES (?,?,?,?)")
                values=[email_from,email_to,email_subject,email_cc]
                cursor.execute(sql,values)
                
                cursor.execute("SELECT IDENT_CURRENT('dbo.BMJ_AssignedJob') ")
                
                result_set = cursor.fetchone()
                for a in result_set:
                    os.makedirs( curEnv["serverpath"] + '/BMJ_{}/Source/'.format(a))
                    os.makedirs(curEnv["serverpath"] + '/BMJ_{}/Extracted'.format(a))
                    os.makedirs(curEnv["serverpath"] + '/BMJ_{}/Metadata'.format(a))
                    for part in email_message.walk():
                    # this part comes from the snipped I don't understand yet...
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue
                        fileName = part.get_filename()
                        if bool(fileName):
                            file_arr = fileName.split('.')
                            filezip = file_arr[-1]
                            if filezip == 'zip':
                                count+=1
                                filePathname=os.path.join(curEnv["serverpath"]+ '/BMJ_'+str(a)+'/Source/', fileName)
                                fileArr.append(fileName)
                                fileName = ';'.join(fileArr)
                                sql=("UPDATE "+curEnv["Database"]+".dbo.BMJ_AssignedJob SET zip_filename = '"+str(fileName)+"', zip_file_count = "+str(count)+" where ID="+str(a))
                                cursor.execute(sql)
                                b=curEnv["serverpath"]+ '/BMJ_'+str(a)+'/Source/'
                                #print(b)
                                c=curEnv["serverpath"]+ '/BMJ_'+str(a)+'/Extracted/'
                                #print(c)
                                extractor(b,c)
                                if not os.path.isfile(filePathname):
                                    #print('true')
                                    fp = open(filePathname, 'wb')
                                    fp.write(part.get_payload(decode=True))
                                    fp.close()
                                    sql=("UPDATE "+curEnv["Database"]+".dbo.BMJ_AssignedJob SET Status_= 'S1' where ID="+str(a))
                                    cursor.execute(sql)
                                    
                                else:
                                    sql=("UPDATE "+curEnv["Database"]+".dbo.BMJ_AssignedJob SET Status_= 'F1' where ID="+str(a))
                                    cursor.execute(sql)
                    #print(fileName)
                    #print(count)
                    
                drop.commit()
                extractor(b,c)
                y=apipara(a)
                
                if str( y[0])=="False":
                    t="F1"
                else:
                    t="S1"
                
                
                
                        
                sql=("UPDATE "+curEnv["Database"]+".dbo.BMJ_AssignedJob SET Status_='"+str(t)+"' where ID="+str(a))
                cursor.execute(sql)
                sql=("UPDATE "+curEnv["Database"]+".dbo.BMJ_AssignedJob SET Remarks='"+str(y[1])+"' where ID="+str(a))
                cursor.execute(sql)
                print("Task added successfully")
        except Exception as e:
            logerr(e)
else:
    print("you can't able to run sorry..")
            
           
