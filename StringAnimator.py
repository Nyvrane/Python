import string
import time

target_word = "hello world"
current_word = ""
index = 0
alphabet = string.ascii_lowercase

while current_word != target_word:
    for letter in alphabet:
        if target_word[index] == " ":
            current_word += " "
            index += 1
            break
        print(current_word + letter, end="\r", flush=True)
        time.sleep(0.1)
        if letter == target_word[index]:
            current_word += letter
            index += 1
            break
