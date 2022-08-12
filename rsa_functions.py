from random import randint
from secret import *
#main goal : build both the encryption and decryption functions of rsa
'''
str1 = 'Mayank Parashar \n good boy'
res = ''.join(format(ord(i), '08b') for i in str1)
print(len(str1))
print(len(res))
print(len(res)//len(str1))
'''
#each character will take 8 (2^3) bits to represent
#let's say we are using 2^10 length block ciphers then we can decode/encode 2^7 bits in one time.


def test_integer_for_prime(p):                                               #(A1)
    '''
    returns 1 if prime
            0 if not prime (composite)
    p : number which is to be tested for primality
    p must be an integer > 0
    Complexity: O(t * log3(n)) -> (O(t * (log cube n))
    where t = number of probes : 7 in this case
    '''
    if p == 1: return 0                                                      #(A2)
    probes = [2,3,5,7,11,13,17]        #sufficient till 3e14                 #(A3)
    if p in probes: return 1                                                 #(A4)
    if any([p % a == 0 for a in probes]): return 0                           #(A5)
    k, q = 0, p-1        # need to represent p-1 as  q * 2^k                 #(A6)
    while not q&1:                                                           #(A7)
        q >>= 1                                                              #(A8)
        k += 1                                                               #(A9)
    for a in probes:                                                         #(A10)
        a_raised_to_q = pow(a, q, p)                                         #(A11)
        if a_raised_to_q == 1: continue                                      #(A12)
        if (a_raised_to_q == p-1) and (k > 0): continue                      #(A13)
        a_raised_to_jq = a_raised_to_q                                       #(A14)
        primeflag = 0                                                        #(A15)
        for j in range(k-1):                                                 #(A16)
            a_raised_to_jq = pow(a_raised_to_jq, 2, p)                       #(A17)
            if a_raised_to_jq == p-1:                                        #(A18)
                primeflag = 1                                                #(A19)
                break                                                        #(A20)
        if not primeflag: return 0                                           #(A21)
    return 1

def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid's Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = num // mod
        num, mod = mod, num % mod
        x, x_old = x_old - q * x, x
        y, y_old = y_old - q * y, y
    if num != 1:
        return -1
    else:
        MI = (x_old + MOD) % MOD
        return MI

def random_number_generator(length_of_binary):
    arr = ['-1' for j in range(length_of_binary)]
    arr[0] = '1'
    arr[1] = '1'
    arr[-1] = '1'
    for i in range(length_of_binary):
        if arr[i] == '-1':
            arr[i] = str(randint(0, 1))
    final = ''.join(arr)
    return final
counter = 0
while True:
    a = int(random_number_generator(512),2)
    if test_integer_for_prime(a):
        print(a)
        break


e = 65
phi_of_n = (p-1)*(q-1)
d = MI(e, phi_of_n)

#message is a string
def encrypt(message):
    res = ''.join(format(ord(i), '08b') for i in message)
    print(res)
    int_res = int(res, 2)
    encrypted_res = pow(int_res, e, n)
    return encrypted_res
    
message = None
a = encrypt('')
print(a)
'''
for i in range(0, len(res), 8):
    ascii_val = int(res[i:i+8], 2)
    print(chr(ascii_val), end = "")
'''

def decrypt(num):
    ans = []
    decrypted_val = pow(num, d, n)
    decrypted_val_binary = bin(decrypted_val)[2:]
    ascii_val = int(decrypted_val_binary[:len(decrypted_val_binary)%8], 2)
    ans.append(chr(ascii_val))
    for i in range(len(decrypted_val_binary)%8, len(decrypted_val_binary), 8):
        ascii_val = int(decrypted_val_binary[i:i+8], 2)
        ans.append(chr(ascii_val))
    return ''.join(ans)
    
ans = decrypt(a)
print(ans)

# def create_keys():
#     '''
#     #creates d and e for the user
#     #return (d, e)
#     '''
#     arr = ['-1' for j in range(12)]
#     while True:
#         arr[-1] = '1'
#         for i in range(11):
#             arr[i] = str(randint(0, 1))
#         final = int(''.join(arr), 2)
#         check = MI(final, phi_of_n)
#         if check > 0:
#             if final not in e_set:
#             #existing_d = User.query.filter_by(public_key = check).first()
#             #if existing_d == None:
#                 e_set.add(final)
#                 return (check, final)

# #d, e = create_keys()
# #print(d, e)

# e_set = set()
# for i in range(100):
#     d, e = create_keys()
#     str_d = str(d)
#     if len(str_d) == 1:
#         print(d, e) 
