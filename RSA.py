import random

class Rsa:

    def __init__(self,q = 19 ,p = 23):
        self.q = q
        self.p = p
        self.public, self.private = self.generate_key_pair(p, q)

    '''
    Euclid's algorithm for determining the greatest common divisor
    Use iteration to make it faster for larger integers
    '''
    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    '''
    Euclid's extended algorithm for finding the multiplicative inverse of two numbers
    '''
    def multiplicative_inverse(self, e, phi):
        d = 0
        x1 = 0
        x2 = 1
        y1 = 1
        temp_phi = phi

        while e > 0:
            temp1 = temp_phi//e
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

    '''
    Tests to see if a number is prime.
    '''
    def is_prime(self, num):
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for n in range(3, int(num**0.5)+2, 2):
            if num % n == 0:
                return False 
        return True


    def generate_key_pair(self, p, q):
        if not (self.is_prime(p) and self.is_prime(q)):
            raise ValueError('Both numbers must be prime.')
        elif p == q:
            raise ValueError('p and q cannot be equal')
        # n = pq
        n = p * q

        # Phi is the totient of n
        phi = (p-1) * (q-1)

        # Choose an integer e such that e and phi(n) are coprime
        e = random.randrange(1, phi)

        # Use Euclid's Algorithm to verify that e and phi(n) are coprime
        g = self.gcd(e, phi)
        while g != 1:
            e = random.randrange(1, phi)
            g = self.gcd(e, phi)

        # Use Extended Euclid's Algorithm to generate the private key
        d = self.multiplicative_inverse(e, phi)

        # Return public and private key_pair
        # Public key is (e, n) and private key is (d, n)
        return ((e, n), (d, n))

                #def encrypt(self, plaintext, public_key):
    def encrypt(self, plaintext , pub_key):
        # Unpack the key into it's components
                #key , n = public_key
        key , n = pub_key
        # Convert each letter in the plaintext to numbers based on the character using a^b mod m
        cipher = [pow(ord(char), key , n) for char in plaintext]
        # Return the array of bytes
        return cipher
    # 15afff?
    # [49, 53, 97, 102, 102, 102, 63]
    def decrypt(self, ciphertext):
        # Unpack the key into its components
        key, n = self.private
        ciphertext = ciphertext.split('\/')
        ciphertext.pop()
        ciphertext = ciphertext
        # Generate the plaintext based on the ciphertext and key using a^b mod m
        aux = [str(pow(int(char), key, n)) for char in ciphertext]
        # Return the array of bytes as a string
        plain = [chr(int(char2)) for char2 in aux]
        return ''.join(plain)


# if __name__ == '__main__':
#     while True:
#         print("------------------")
#         x = Rsa()
#         print("Public Key :",x.public)
#         cipher = x.encrypt(input("Plain Text < "),x.public)
#         plain = x.decrypt(cipher)
#         print("Plain Text >",plain)
        