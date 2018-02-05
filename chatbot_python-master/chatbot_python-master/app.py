import os,sys
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response

app=Flask(__name__)

PAGE_ACCESS_TOKEN ="EAAB8egdZB0IkBACp1jbaiEXOYIEGMcezLZAFAgEN9FF4fDDnlL8v7QVZCKD9KPWBJ9WslZAhKkFkcfWxFeBtdeLFz3dqRYkSfXWbIPAvpTzDnKWdVcgpTkY6LHAzTyfSZCB5mmNa9qNZA0EkIxbOh9c72asqBncjEwDvNZBwpOJv2vD4y0XTA8a"
bot=Bot(PAGE_ACCESS_TOKEN)

@app.route("/",methods=['GET'])
def verify():
    #webhook verification
    if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")== "hello":
            return "Verification token mismatch",403
        return request.args["hub.challenge"],200
    return "Hello world whats up",200

@app.route("/" , methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                #IDs
                sender_id=messaging_event['sender']['id']
                recipient_id=messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text='no text'

                    response= None

                    entity,value = wit_response(messaging_text)
                    if entity== 'newstype':
                        response= "Ok . I will send you {} news".format(str(value))

                    elif entity == "location" :
                        response= " Ok. so, you live in {0}. I will send you top headlines from {0} ".format(str(value))

                    if response == None:
                        response = "Sorry,I didnt understand!"
                    bot.send_text_message(sender_id,response)

                 #   bot.send_text_message(sender_id,response)


    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()

    
if __name__=="__main__":
    app.run(debug=True,port=80)

#pip freeze > requirements.txt 
#this create a txt file after setting up virtual env which consists of all modules and there versions 
# echo > Procfile
#will create a procfile
