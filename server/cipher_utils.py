import binascii
from collections import defaultdict

def simple_substitution_encrypt(plaintext, key="zyxwvutsrqponmlkjihgfedcba"):
    print("text: ", plaintext)
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():
            encrypted_text += key[ord(char.lower()) - ord('a')].upper() if char.isupper() else key[ord(char) - ord('a')]
        else:
            encrypted_text += char
    return encrypted_text

def simple_substitution_decrypt(ciphertext, key="zyxwvutsrqponmlkjihgfedcba"):
    decrypted_text = ""
    inverse_key = {v: k for k, v in zip(key, 'abcdefghijklmnopqrstuvwxyz')}
    for char in ciphertext:
        if char.isalpha():
            decrypted_text += inverse_key[char.lower()].upper() if char.isupper() else inverse_key[char]
        else:
            decrypted_text += char
    return decrypted_text

def double_transposition_encrypt(plaintext, key):
    return encryptr_f(encryptr_f(plaintext,key),key)

def double_transposition_decrypt(ciphertext, key):
    return decryptr_f(decryptr_f(ciphertext,key),key)

def _rc4_algorithm(text, key):
    S = list(range(256))
    j = 0
    out = []

    # KSA (Key-Scheduling Algorithm)
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA (Pseudo-Random Generation Algorithm)
    i = j = 0
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

    # return "".join(out)
    # Convert the output to hexadecimal representation
    encrypted_text = "".join(out)
    return encrypted_text

def rc4_encrypt(plaintext, key):
    encrypted_text = _rc4_algorithm(plaintext, key)
    encrypted_hex = binascii.hexlify(encrypted_text.encode()).decode()

    return encrypted_hex

def rc4_decrypt(ciphertext, key):
    # Convert hexadecimal input to binary
    encrypted_text = binascii.unhexlify(ciphertext.encode()).decode()

    # Decrypt the binary text using rc4_encrypt function
    decrypted_text = _rc4_algorithm(encrypted_text, key)

    return decrypted_text

def encryptr_f(plaintext, key):
 print(f"plaintext {plaintext} and key {key}")
 r = [['\n' for i in range(len(plaintext))]
      for j in range(key)]
 dir_down = False
 row, col = 0, 0
 for i in range(len(plaintext)):
     if (row == 0) or (row == key - 1):
         dir_down = not dir_down
     r[row][col] = plaintext[i]
     col += 1
     if dir_down:
         row += 1
     else:
         row -= 1
 result = []
 for i in range(key):
     for j in range(len(plaintext)):
         if r[i][j] != '\n':
             result.append(r[i][j])
 return("" . join(result))


def decryptr_f(ciphertext, key):
 print(f"ciphertext: {ciphertext} and key {key}")
 r = [['\n' for i in range(len(ciphertext))]
      for j in range(key)] 
 dir_down = None
 row, col = 0, 0
 for i in range(len(ciphertext)):
     if row == 0:
         dir_down = True
     if row == key - 1:
         dir_down = False
     r[row][col] = '*'
     col += 1
     if dir_down:
         row += 1
     else:
         row -= 1
 index = 0
 for i in range(key):
     for j in range(len(ciphertext)):
         if ((r[i][j] == '*') and
         (index < len(ciphertext))):
             r[i][j] = ciphertext[index]
             index += 1
 result = []
 row, col = 0, 0
 for i in range(len(ciphertext)):
     if row == 0:
         dir_down = True
     if row == key-1:
         dir_down = False
     if (r[row][col] != '*'):
         result.append(r[row][col]) 
         col += 1
     if dir_down:
         row += 1
     else:
         row -= 1
 return("".join(result))
