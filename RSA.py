import random

class Rsa:

    def __init__(self, q=19, p=23, size_of_key=0):
        self.q = q
        self.p = p
        if size_of_key:
            self.q = self.gen_prime(size_of_key)
            self.p = self.gen_prime(size_of_key)
            while self.p == self.q : 
                self.p = self.gen_prime(size_of_key)
        self.public, self.private = self.generate_key_pair(self.q, self.p)

    def gen_prime(self, size_of_key):
        first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]

        def nBitRandom(n):
            return random.randrange(2**(n-1)+1, 2**n - 1)
                
        def getLowLevelPrime(n):
            '''Generate a prime candidate divisible
            by first primes'''
            while True:
                # Obtain a random number
                pc = nBitRandom(n)
        
                # Test divisibility by pre-generated
                # primes
                for divisor in first_primes_list:
                    if pc % divisor == 0 and divisor**2 <= pc:
                        break
                else: return pc
        
        def isMillerRabinPassed(mrc):
            '''Run 20 iterations of Rabin Miller Primality test'''
            maxDivisionsByTwo = 0
            ec = mrc-1
            while ec % 2 == 0:
                ec >>= 1
                maxDivisionsByTwo += 1
            assert(2**maxDivisionsByTwo * ec == mrc-1)
        
            def trialComposite(round_tester):
                if pow(round_tester, ec, mrc) == 1:
                    return False
                for i in range(maxDivisionsByTwo):
                    if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                        return False
                return True
        
            # Set number of trials here
            numberOfRabinTrials = 20
            for i in range(numberOfRabinTrials):
                round_tester = random.randrange(2, mrc)
                if trialComposite(round_tester):
                    return False
            return True

        while True:
            prime_candidate = getLowLevelPrime(size_of_key)
            if not isMillerRabinPassed(prime_candidate):
                continue
            else:
                print(size_of_key, "bit prime is: \n", prime_candidate)
                return prime_candidate

    def modInverse(self, e, phi):
        m0 = phi
        y = 0
        x = 1
    
        if (phi == 1):
            return 0
    
        while (e > 1):
    
            # q is quotient
            q = e // phi
    
            t = phi
    
            # m is remainder now, process
            # same as Euclid's algo
            phi = e % phi
            e = t
            t = y
    
            # Update x and y
            y = x - q * y
            x = t
    
        # Make x positive
        if (x < 0):
            x = x + m0
        return x

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

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def generate_key_pair(self, p, q):
        # if not (self.is_prime(p) and self.is_prime(q)):
        #     raise ValueError('Both numbers must be prime.')
        # elif p == q:
        #     raise ValueError('p and q cannot be equal')
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
        d = self.modInverse(e, phi)

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
#         x = Rsa(size_of_key=512)
#         print("Public Key :",x.public)
#         cipher = x.encrypt(input("Plain Text < "),x.public)
#         plain = x.decrypt(cipher)
#         print("Plain Text >",plain)
        