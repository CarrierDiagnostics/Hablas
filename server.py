import asyncio, difflib #multiprocessser good for sockets
import websockets , json # the json is bc we're sending a json object from the website
import wave , base64
import os #library for anything that has to do with your hard-drive
from french import stt

def highlight_differences(predicted, sentence):
    predicted=predicted.lower()   #predicted is what the AI generated
    sentence=sentence.lower()
    predicted2 = predicted.replace("-"," ").strip()
    sentence2 = sentence.replace("-"," ").strip()
    print(f"sentence from book: {sentence2} and predicted sentence: {predicted2}")
    words_pred = predicted2.split() #returns a LIST
    words_sentence = sentence2.split()
   
   # Initialize indices for both lists
    i, j = 0, 0
    
    # Iterate through both lists
    while i < len(words_pred) and j < len(words_sentence):
        if words_pred[i] == words_sentence[j]:
            print(f"ok word: {i} - {words_pred[i]}")
            i += 1
            j += 1
        else:            
            print(f"word from the book: {words_sentence[i]} - predicted word: {words_pred[i]}")
            words_pred[i] = f'<span id="wrong">{words_pred[i]}</span>'
            # Check if the next word in actual sentence can be skipped
            if j + 1 < len(words_sentence) and words_pred[i] == words_sentence[j + 1]:
                print(f"Resyncing: skipping '{words_sentence[j]}'")
                j += 1  # Skip the word in actual sentence
            else:
                # If no match and no skip possible, just move to the next word in predicted sent
                i += 1

    # Handle any remaining words in either sentence
    while i < len(words_pred):
        print(f"Remaining word in predicted sentence: {words_pred[i]}")
        i += 1

    while j < len(words_sentence):
        print(f"Remaining word in actual sentence: {words_sentence[j]}")
        j += 1

    words_pred=" ".join(words_pred)
    print(f"final sentence after comparison: {words_pred} ")

    return words_pred

class TextComparator:
    @staticmethod
    def generate_html_report(text1, text2, output_file='text_comparison_report.html'):
        words1 = text1.lower().split()
        words2 = text2.lower().split()
        matcher = difflib.SequenceMatcher(None, words1, words2)       
        marked_words2 = words2.copy()        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            print((tag,i1, i2, j1, j2))
            if tag != 'equal':
                for j in range(j1, j2):
                    marked_words2[j] = f'<span id="wrong" style="color:red;">{marked_words2[j]}</span>'
        
        marked_text2 = ' '.join(marked_words2)
        
        similarity_ratio = matcher.ratio()
        
       
        return marked_text2, similarity_ratio

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
        the_words = stt(fpath,data_object["language"])
        #predicted_sentence = highlight_differences(the_words,data_object["sentence"])
        predicted_sentence, similarity_ratio = TextComparator.generate_html_report(data_object["sentence"], the_words)
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
