from flask import Flask, request
import requests
import json


from openai import OpenAI
import os


OPENAI_API_KEY = " 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"
os.environ["OPENAI_API_KEY"]= OPENAI_API_KEY 

client = OpenAI()



app=Flask(__name__)

@app.route("/saludar", methods= ["GET"])
def Saludar():
    return "Hola mundo"


@app.route("/whatssap", methods= ["GET"])
def VerifyToken():
    try:
        access_token = "myaccesstokensecreto"
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
    
        
        if token == access_token:       
            return challenge
        else:
            return "errores",400
    except Exception as e:
            print("Error: {e}")
            return "Error", 400

@app.route("/whatssap", methods= ["POST"])
def ReceivedMessage():
     try:
        body = request.get_json()
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        message = value["messages"][0]
        text = message ["text"]
        question_user = text["body"]
        numero = message["from"]

        print("Este es el texto recibido", question_user)

        body_answer  = enviarMensaje(question_user,numero)
        #body_answer  = enviarImagen(question_user,numero)
        send_message = whatssappService(body_answer)

        if send_message:
            print("Mensaje enviado correctamente")
        else:
            print("Error al envio del mensaje")
        
        return "EVENT_RECEIVED"
     
     except Exception as e:
        print(e)
        return "EVENT_RECEIVED"

def whatssappService(body):
     
     try:

        #token = "EAAFzWXju9WMBO6iZA8kadbGPIZCkb12STcA1HPY8Jg9pHEcpLONE3JpEsBPZBxaLHk8tnTZByumPZCxGkDcQXY6dOahrn9z4Yu2xgoYQALv0zYSt0jvcd7nCZAgDNuIZB9jcoHV7WGUQp8PX84kGahTq0jEDXrfGNzhjtCspivCk8VkFz3PvC9B5StoU4XwZAbaH4xlbZCEu0xtr2pJLJFNvSYnUCnC3pDftpZBxQZD"
        token = "EAAFzWXju9WMBO2t4LOAkWMZCuOvED6IidVoxHsI7TxZBX9vEK1eVZABSLNMrLZBrdTqHHRm3SBgftBzKQZBKG3ayDBPlyNwZA5cRUOZAbTCD2idv6ZAuVeQbTbgLjBk1z7tuEXwu0ZBMBWFAWdDfdZANIm7x2byQSsPl3klYTHVZCYUSlq9qskO11uZBgVQGfG8SjDWK"
       
        api_url = "https://graph.facebook.com/v18.0/201106959761535/messages"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer "+token
        }

        response=requests.post(api_url,
                        data = json.dumps(body),
                        headers = headers)
        
    
        if response.status_code==200:
             
             return True
        else:
             return False
     

     except Exception as e:
          print(e)
          return False


def enviarMensaje(text,numero):
     
    

     
     url = "https://openaiservicegpt-r5hgt5gndq-uc.a.run.app/getresponsegpt?user_prompt="+text
     responseGPT = requests.get(url).content.decode("utf-8")



     context = [ {'role':'system', 'content':"""
      Comportate como un detector de intencion de orden de compra de productos de young living/
      responde construyendo un archivo json del mensaje previo/
      los campos deben ser 1) mensaje, 2) intencion, el valor de mensaje prompt y la/
      intencion True si hay intencion de orden de compra y False si no
      """} ] 
     
     messages =  context.copy()
     messages.append({'role':'user', 'content': text }, )
     response = get_completion_from_messages(messages, temperature=0)
     print(response)



     body = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to":numero,
            "type": "text",
            "text": {
                "body": responseGPT
            }
            
    }
     return body


def enviarImagen(link,numero):
   body = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": numero,
    "type": "image",
    "image": {
        "link": "https://i.imgur.com/JEbwlcf.jpeg"
    }
}
   return body


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):

    response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=temperature,
  )
    return response.choices[0].message.content

if __name__== "__main__":
    app.run(host="0.0.0.0", port=8002, debug = True)