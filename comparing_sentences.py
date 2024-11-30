
predicted="hola me llamo Olivia"
sentence="hola me chiamo Lidia"

predicted=predicted.lower()
sentence=sentence.lower()
words_pred = predicted.split() #returns a LIST
words_sentence = sentence.split()
wc_pred = len(words_pred)
wc_sentence = len(words_sentence)
max_length = max (wc_pred, wc_sentence) #predicted is what the AI generated

print(words_pred)
if (wc_pred == wc_sentence):
    for i in range (max_length):
        if (words_pred[i]==words_sentence[i]):
            print(f"ok word: {i}")

        elif (words_pred[i]!=words_sentence[i]):
            print(f"word: {i} is not ok")
            words_pred[i] = f"<div id='wrong'>{words_pred[i]}"
            print(words_pred[i])

words_pred=" ".join(words_pred)
print(words_pred)

