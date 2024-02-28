import random
import os
import pickle

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def generate_key_pair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q
    phi = (p-1) * (q-1)

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))

def encrypt(pk, file_path):
    key, n = pk
    encrypted_data = []

    with open(file_path, 'rb') as f:
        byte = f.read(1)
        while byte:
            encrypted_data.append(pow(int.from_bytes(byte, byteorder='big'), key, n))
            byte = f.read(1)

    return encrypted_data


def decrypt(pk, encrypted_data):
    key, n = pk
    decrypted_data = []

    for num in encrypted_data:
        decrypted_data.append(pow(num, key, n))

    return decrypted_data



if __name__ == '__main__':
    p = int(input(" - Enter a prime number (17, 19, 23, etc): "))
    q = int(input(" - Enter another prime number (Not one you entered above): "))
    
    print(" - Generating your public / private key-pairs now . . .")

    public, private = generate_key_pair(p, q)

    print(" - Your public key is ", public, " and your private key is ", private)

    file_path = input(" - Enter the path to the file to encrypt with your public key: ")
    file_dir, file_name = os.path.split(file_path)
    encrypted_file_path = os.path.join(file_dir, "encrypted_" + file_name + '.rsa')
    
    encrypted_data = encrypt(public, file_path)

    with open(encrypted_file_path, 'wb') as f:
        pickle.dump(encrypted_data, f)

    print(" - Your file has been encrypted and saved as:", encrypted_file_path)

    decryption_choice = input(" - Do you want to decrypt the file? (yes/no): ").lower()
    if decryption_choice == "yes":
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = pickle.load(f)
        decrypted_data = decrypt(private, encrypted_data)
        decrypted_file_path = input(" - Enter the path to save the decrypted file: ")

        with open(decrypted_file_path, 'wb') as f:
            for byte in decrypted_data:
                f.write(byte.to_bytes(1, byteorder='big'))

        print(" - Your file has been decrypted and saved as:", decrypted_file_path)
    else:
        print(" - Thank you. Exiting...")

    print(" ")
    print("============================================ END ==========================================================")
    print("===========================================================================================================")