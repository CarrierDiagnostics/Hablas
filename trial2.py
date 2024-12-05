sen1p= "hello oh no no my name is namia" 
sen2 = "hello my name is namie"

words_pred = sen1p.split() #returns a LIST
words_sentence = sen2.split()

# Initialize indices for both lists
i, j = 0, 0

# Iterate through both lists
while i < len(words_pred) and j < len(words_sentence):
    if words_pred[i] == words_sentence[j]:
        print(f"ok word: {i} - {words_pred[i]}")
        i += 1
        j += 1
    else:
        words_pred[i] = f'<span id="wrong">{words_pred[i]}</span>'
        print(f"word: {i} is not ok - {words_pred[i]}")
        # Check if the next word in sen2 can be skipped
        if j + 1 < len(words_sentence) and words_pred[i] == words_sentence[j + 1]:
            print(f"Resyncing: skipping '{words_sentence[j]}'")
            j += 1  # Skip the word in sen2
        else:
            # If no match and no skip possible, just move to the next word in sen1p
            i += 1

# Handle any remaining words in either sentence
while i < len(words_pred):
    print(f"Remaining word in sen1p: {words_pred[i]}")
    i += 1

while j < len(words_sentence):
    print(f"Remaining word in sen2: {words_sentence[j]}")
    j += 1

words_pred=" ".join(words_pred)
print(f"final sentence after comparison: {words_pred} ")

    