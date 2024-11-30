import asyncio #multiprocessser good for sockets
import websockets , json # the json is bc we're sending a json object from the website
import wave , base64
import os #library for anything that has to do with your hard-drive
from french import stt

def highlight_differences(predicted, sentence):
    predicted=predicted.lower()
    sentence=sentence.lower()
    words_pred = predicted.split() #returns a LIST
    words_sentence = sentence.split()
    wc_pred = len(words_pred)
    wc_sentence = len(words_sentence)
    max_length = max (wc_pred, wc_sentence) #predicted is what the AI generated

    print(words_pred)
    for i in range (max_length):
        if (words_pred[i]==words_sentence[i]):
            print(f"ok word: {i}") #clean

        elif (words_pred[i]!=words_sentence[i]):
            print(f"word: {i} is not ok")
            words_pred[i] = f'<span id="wrong">{words_pred[i]}</span>'
            print(words_pred[i]) #clean


    words_pred=" ".join(words_pred)
    return words_pred

async def handle_connection(websocket):
    print(f"Client connected, {websocket.remote_address}")

    
    try:
        data= await websocket.recv()
        data_object = json.loads(data)
        print(f"data: {data_object}") 

        fpath="received_audio.wav" #name of the audio in the server (our computer in this case)
        with open(fpath, "wb") as audio_file: #received_audio is f.open, initialising this file. audio_file is the variable
                base64_string = data_object["blob"]
                actual_base64 = base64_string.split(',')[1]  # Get the Base64 part
                binary_data = base64.b64decode(actual_base64)
                audio_file.write(binary_data)
        the_words = stt(fpath) 
        predicted_sentence = highlight_differences(the_words,data_object["sentence"])
        message_returned = {"pred_sentence":predicted_sentence}

        print("Received audio file and saved as 'received_audio.wav'")
        await websocket.send(json.dumps(message_returned)) #waits until the sockets has sent everything and the pipe closes
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Client disconnected")

async def main():
    # Start the WebSocket server
    async with websockets.serve(handle_connection, "localhost", 8765, ssl=None):  # Standarised way of building a websocket. ssl not done yet!! (certificate)
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever


if __name__ == "__main__": #when you use a multi processer load, you use this so it doesnt crash. with asyncio you always have to do it
    asyncio.run(main())
