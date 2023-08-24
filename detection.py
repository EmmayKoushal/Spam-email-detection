import smtplib
import time
import imaplib
import email
import traceback 
import pickle

ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "emmaykoushal" + ORG_EMAIL 
FROM_PWD = "pqjonofkgulbcjvc" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

def extract_url(body):
    words = body.split(' ')
    url = ''
    max = 0
    for word in words:
        dots = word.count('.')
        slashs = word.count('/')
        ds = dots + slashs + len(word)
        if ds > max:
            url = word
            max = ds

    return url

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        id_list = id_list[-3:]
        print(len(id_list))
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('-'*30)
                    print('From : ' + email_from + '\n')
                    # print('Subject : ' + email_subject + '\n')
                    # print ("body:")
                    for part in msg.walk():  
                        #print(part.get_content_type())
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload()
                            url = extract_url(body)
                            if url == '':
                                print("No URL found !!")
                                return None
                                
                            loaded_model = pickle.load(open('phishing.pkl', 'rb'))
                            result = loaded_model.predict([url])

                            if result[0] == 'good':
                                print('\n\n')
                                print("This is a safe email")
                                print('\n\n')

                            else:
                                print('\n\n')
                                print("This Email contains Malicious URL. DONOT open this email !!")
                                print('\n\n')
                                
                            #print (part.get_payload())
                            print('-'*30)

    except Exception as e:
        traceback.print_exc() 
        print(str(e))

read_email_from_gmail()