# Rabin Signature Scheme Implementation

## 1. Introduction

This project was the final course project for the Applied Cryptography course offered by [Indraprastha Institute of Information Technology, Delhi](https://www.iiitd.ac.in/) during the monsoon semester of 2022. <br>
Rabin Signature scheme was one of the first methods of digital signature proposed by Michael O. Rabin in 1979. The difficulty to forge this signature is expressed in terms of the difficulty to factorize a large number. 


## 2. Quadratic Residue

Given two integers $x$ and $p$.

$X$ is called quadratic residue modulo $p$ if and only if there exists some integer y such that -

$$
\LARGE y^{2} \equiv x(\bmod p)
$$

## 3. Euler's Criterion

Given an odd prime $p$. And an integer $x$ coprime to $p$. Then, according to Euler's Criterion, $\mathrm{x}$ is a quadratic residue modulo $p$ if and only if -

$$
\LARGE x^{\frac{p-1}{2}} \equiv 1(\bmod p)
$$

## 4. Finding square root

Let $\mathrm{x}$ be a quadratic residue modulo $\mathrm{p}$. Such that,

$\LARGE y^{2} \equiv x(\bmod p)$, we want to find $\mathrm{y}$.

Suppose $p$ is an odd prime.

Case 1: $\LARGE \quad p \equiv 3(\bmod 4)$

In this case, there exists a polytime deterministic algorithm to find the square root of $x$ modulo $p$.

In this case $\mathrm{y}$ is simply $\LARGE \pm x^{\frac{p+1}{4}} \bmod p$

Proof -

$\LARGE y \equiv \pm x^{\frac{p+1}{4}}(\bmod p)$

$\LARGE \Rightarrow y^{2} \equiv x^{\frac{p+1}{2}}(\bmod p)$

$\LARGE \Rightarrow y^{2} \equiv x^{\frac{p-1}{2}} \cdot x(\bmod p)$

$\LARGE \Rightarrow y^{2} \equiv x(\bmod p) \quad$ by Euler's Criterion.

<br>

Case 2: &emsp; $\LARGE p \equiv 1(\bmod 4)$
<br>
In this case we can use complicated probabilistic algorithm like Berlekamp's root finding algorithm.

## 5. Algorithm to create the signature

We first take two odd primes of the form $4 k+3$. Let them be $p$ and q.

We then find $n=p^{*} q$ and $0 \leq b < n$.

The pair $(n, b)$ is public and can be used to verify the signature.

A hash function is also used to compress an intermediate string in the algorithm. This hash function ' $\mathrm{H}$ ' is also public.

The only private values are ' $p$ ' and ' $q$ ' which are used to create the signature.

First the message string is concatenated with a randomly generated string $U$ to get a new string $M+U$. This new string is then compressed using the hash function $\mathrm{H}$ to get an integer value $\mathrm{c}$ such that $c < n$.

Now we want to find the values of $x$ which satisfy the following congruence -

$$
\begin{aligned}
&\LARGE x *(x+b) \equiv c(\bmod n) \\
&\LARGE \Rightarrow x^{2}+b x \equiv c(\bmod n)
\end{aligned}
$$

Now let $\LARGE d \equiv b \cdot 2^{-1}(\bmod n)$, replace b by $\LARGE 2 \mathrm{~d}$ and add $d^{2}$ on both sides. The congruence becomes,

$$
\begin{gathered}
\LARGE x^{2}+2 d x+d^{2} \equiv c+d^{2}(\bmod n) \\
\LARGE \Rightarrow(\mathrm{x}+\mathrm{d})^{2} \equiv c+d^{2}(\bmod n)
\end{gathered}
$$

Now let $\LARGE y=(x+d)$ and $\LARGE m=c+d^{2}$. The equation becomes,

$$
\LARGE y^{2} \equiv m(\bmod n)
$$

But $n=p^{*} q$, both $p$ and $q$ are coprime. So, we can break the above equation into 2 parts -

$$
\begin{aligned}
& \LARGE y^{2} \equiv m(\bmod p) \\
& \LARGE y^{2} \equiv m(\bmod q)
\end{aligned}
$$

The above equations are of the same form as quadratic residue equations as seen above.

If $m$ is not a quadratic residue $\bmod p$ or $\bmod q$, then we do this entire process for a different randomly generated string $U$.

The expected value of doing this is 4 .

After that we can find the solution for $y$ using Chinese remainder theorem. Once we have ' $y$ ' we can find ' $x$ '.

The signature is then the pair $\LARGE (U, x)$

## 6. Verify algorithm

To verify whether a message $M$ is authentic. We can check if its signature is correct. To do that,

find $\LARGE c=H(M+U)$ and $\LARGE x *(x+b)$ And then return 1 (i.e., message is authentic) if and only if

$$
\LARGE x *(x+b) \equiv c(\bmod n)
$$

Else return 0 (i.e., message is not authentic)

## 7. Security

It is assumed that any adversary with high probability to forge the Rabin Signature can also with high probability find two values $y_{1}$ and $y_{2}$ such that $\LARGE \left.y_{1}^{2} \equiv y_{2}^{2} \equiv \bmod n\right)$ and $y_{1} \pm y_{2} \neq 0(\bmod n)$

This means $\LARGE n \mid\left(y_{1}^{2}-y_{2}^{2}\right)$ as $y_{1}^{2} \equiv y_{2}^{2}(\bmod n)$

But $n$ does not divide $\LARGE y_{1}-y_{2}$ or $\LARGE y_{1}+y_{2}$ as $\LARGE y_{1} \pm y_{2} \neq 0(\bmod n)$ <br>
This means $\LARGE \gcd\left(y_{1} \pm y_{2}, n\right)$ is a factor of $\mathrm{n}$ other than 1 and $\mathrm{n}$.

So, if some adversary A can forge Rabin signature, then A can also factor large number $n$. Factorization is assumed to be very difficult. The security of Rabin Signature depends on this fact.

## 8. Large Prime Number Generation

- We first calculate all prime numbers till $10^{7}$.
- Then we find random odd integers of 1024 bits. Such that their most significant bit (MSB) is 1 . This is to make sure that the integers generated in this manner are large.
- We check if this number is a prime with high probability by passing it into a modified miller-rabin test.
- The modified miller-rabin test is when we first check if the number is divisible by any precomputed primes and then apply normal miller rabin test to it.
- If the number passes this test, then we can say with high probability that this input number was a prime number. Otherwise we generate some other number and check again and again.


## 9. Modified Miller-rabin test

### a. Part 1: Check divisibility by small primes

We check if the input odd integer is divisible by any of the precomputed primes. If it is divisible by any of the primes then we are sure that this number is not prime and we return False.

Otherwise we apply the second part (Miller-rabin test) to this integer.

### b. Part 2: Miller rabin test

Input odd integer is $p$

We write $\LARGE (p-1)=2^{k} * m$, where $\mathrm{m}$ is odd. We then find random integers a $\LARGE (2 \leq a \leq p-2)$. And then check if $a$ is a 'witness' that $p$ is not prime or not. We do this for about 50 witnesses. Each test returns True with $3 / 4$ probability.

We find values

$\LARGE a^{m} \bmod p, a^{2 m} \bmod p, a^{4 m} \bmod p \ldots a^{\left(2^{k}-1\right) * m} \bmod p$

Then $\mathrm{p}$ is probable prime with base a if any of the following congruence holds.

$\LARGE a^{m} \equiv 1 \bmod p$

$\LARGE a^{2^{i} m} \equiv-1 \bmod p, 0 \leq i < k$

The logic of this test can be proved using two key facts

- Fermat's theorem $\LARGE \rightarrow a^{\left(2^{k}\right) * m} \equiv a^{p-1} \equiv 1(\bmod p)$, if $\mathrm{p}$ is prime
- Only square roots of $1 \bmod p$ are 1 and -1 .

We can say that $\LARGE a^{\left(2^{k}\right) * m} \equiv 1(\bmod p)$, this means $\LARGE a^{\left(2^{k-1}\right) * m} \equiv$ $1(\bmod p)$ or $\LARGE a^{\left(2^{k-1}\right) * m} \equiv-1(\bmod p)$. But if $\LARGE a^{\left(2^{k-1}\right) * m} \equiv$ $-1(\bmod p)$, then we would have returned that $p$ is prime. This means $\LARGE a^{\left(2^{k-1}\right) * m} \equiv 1(\bmod p)$. And we keep doing this till we reach $a^{m}$. This means if $\mathrm{p}$ is prime then we will never state it as a composite.




