import random
import hashlib
import math


#  return binary string of length size
def get_random_string(size):
    res = ""
    for i in range(size):
        res+=str((random.randint(0,1)))
    return res


# Return the integer value of hash digest
def get_hash_value(str):
    return int.from_bytes(hashlib.sha256(str.encode()).digest(), 'big')

# returns true if val is quadratic residue mod pr
def is_quadratic_residue(val,pr):
    return 1==pow(val,(pr-1)//2,pr)

# returns the signature of message M
def get_signature(M):
    U = get_random_string(60)
    c = get_hash_value(M + U)
    m = c + d*d

    while(not (is_quadratic_residue(m,p) and is_quadratic_residue(m,q))):
        U = get_random_string(60)
        c = get_hash_value(M + U)
        m = c + d*d


    # x * (x + b)  = c   mod(n)
    #simplifying congruence
    # (x + d)^2 = c + d^2  mod(n)
    # y^2 = m  mod(n)
    # using chinese remainder theorem

    v1 = pow(m,(p + 1)//4,p) * q * pow(q,p-2,p)
    v2 = pow(m,(q + 1)//4,q) * p * pow(p,q-2,q)
    y = (v1 + v2)%n
    x = (y - d)%n
    return (U,x)


def verify(signature, M):
    c = get_hash_value(M + signature[0])
    x = signature[1]
    l_side = x * (x + b)
    r_side = c
    if(l_side%n==r_side%n):
        return 1
    return 0

# return true if a is a witness, false otherwise
def witness(a,k,m,p):
    b = pow(a, m, p)
    if b == 1:
        return False
    
    for i in range(k):
        if((-1%p)==(b%p)):
            return False
        b = (b*b)%p
    return True


# return False if prime_candidate is divisible by any pre computed prime, True otherwise
def initial_check(prime_candidate):
    for prime in primes:
        if prime_candidate%prime==0:
            return False
    return True

# returns true if prime_candidate passes miller_rabin_test, false otherwise
def miller_rabin_test(prime_candidate):
    if not initial_check(prime_candidate):
        return False

    temp = prime_candidate - 1
    k = 0
    while temp%2==0:
        temp//=2
        k+=1
    m = temp

    # testing for 50 witnesses
    for j in range(70):
        a = random.randint(2,prime_candidate-2)
        if witness(a,k,m,prime_candidate):
            return False
    return True        


# returns a random odd integer of 'bits' bitlength.
def get_prime_candidate(bits):
        prime_candidate = random.randint(2**(bits-1),(2**bits) - 1)
        if(prime_candidate%2==0):
            prime_candidate+=1
        return prime_candidate

# returns a probable prime of 'bits' bitlength using miller-rabin test
def get_prime(bits):
    prime_candidate = get_prime_candidate(bits)
    while not miller_rabin_test(prime_candidate):
        prime_candidate = get_prime_candidate(bits)
    return prime_candidate


# find all primes which are not more than limit, using Sieve of Eratosthenes.
def generate_primes(limit):
    global primes
    is_prime = []
    for i in range(limit + 1):
        is_prime.append(True)
    
    for i in range(2,limit + 1):
        if(is_prime[i]):
            j = (i*i)
            while j<=limit:
                is_prime[j] = False
                j+=i
    
    for i in range(2,limit + 1):
        if(is_prime[i]):
            primes.append(i)


primes = []
generate_primes(10**7)
random.seed(117)
p = get_prime(1024)
q = get_prime(1024)
print("p ->\n",p)
print("\nq ->\n",q)

# p = 187837245733959530296768935983
# q = 850303114765709315608946810539

n = p * q
b = 10**9 + 7
d = b * pow(2,(p-1)*(q-1) - 1, n)

msg = get_random_string(128)

print("\nmessage ->\n",msg)

signature = get_signature(msg)

print("\nsignature -> (U,x)\n",signature)

if(1==verify(signature,msg)):
    print("message is authentic")
else:
    print("message is not authentic")


