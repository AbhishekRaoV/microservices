from cryptography.fernet import Fernet

encryption_key = b'your_encryption_key_here'

def decrypt_password(encrypted_password):
    try:
        cipher_suite = Fernet(encryption_key)
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
    except Exception as e:
        return None
    
encrypted_password = 'your_encrypted_password_here'
decrypted_password = decrypt_password(encrypted_password)

if decrypt_password:
    print(f'Decrypted Password: {decrypted_password}')
else:
    print('Decryption failed.')