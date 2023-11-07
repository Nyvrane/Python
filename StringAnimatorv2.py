import string
import time
import os
import platform


if platform.system() == "Linux" or platform.system() == "Darwin":  # Linux veya macOS
    clear_command = "clear"
else:
    clear_command = "cls"  # Windows

target_word = "hello world"
current_word = ""
index = 0
alphabet = string.ascii_lowercase

while current_word != target_word:
    for letter in alphabet:
        if index < len(target_word) and target_word[index] == " ":
            current_word += " "
            index += 1
            break
        print(current_word + letter, end="\r", flush=True)
        time.sleep(0.1)
        if letter == target_word[index]:
            current_word += letter
            index += 1
            break
        os.system(clear_command)
print(target_word)
