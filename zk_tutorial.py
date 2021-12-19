import functools
import random
import math
import hashlib

"""
Just following and trying to study ZK proofs, arguments, and whatever zSNARKS are
Link to blog post I'm following:
http://www.shirpeled.com/2018/09/a-hands-on-tutorial-for-zero-knowledge.html?m=1

Definitions::
    -ZK Proof: can be completely trusted even if prover has unlimited computational power to try to prove something false

    -ZK Argument: can be trusted with the assumption that the prover would be polynomial bound(?) if they try to prove something false

    -Prover: party that is trying to prove the claim

    -Verifier: party that is being proved something and shouldn't know anything about the data or method

    -Partion Problem: given an array of integers, can you organize them into 2 groups such that they have the same sum? (NP-complete problem?)

    -Process that doesn't give new information: if output appears random, or more precisely - if it is uniformly distributed over some appropriately chosen domain
"""

def dot(a1: list, a2: list):
    assert(len(a1) == len(a2))
    return sum(a*b for a,b in zip(a1,a2))

#List of numbers
l = [4,11,8,1]

#Partioning of l1 numbers, 1 is for 'left' side and -1 for 'right' side so DP of l1 and m1 is 0 if Partitioning Problem is solvable
m = [1,-1,1,-1]

#Trying to prove knowing if a list (like l) is Partion Problem solvable would not be ZK if just reveals m

#So, maybe try to construct a list of partial sums so that the elements of p are able to prove that m is a solution to the PP of l
#1. p starts and ends with
#2. for i in [0,len(l)) then |l[i]|=|p[i+1]−p[i]|

def make_p(a1: list, a2: list):
    assert(len(a1)==len(a2))
    p_list = [0]
    for i in range(len(a1)):
        s = 0
        for j in range(i+1):
            s += a1[j] * a2[j]
        p_list.append(s)
    return p_list

p = make_p(l,m)

#Possible process: verifier gives a random i between 0 and len(l) and checks if |l[i]|=|p[i+1]−p[i]| enough times to be certain that prover is probably knowledgable
#A p made from an l and m could be used to verify to a verifier that the prover has knowledge of the PP but doesn't account for being ZK (as m could be revealed with enough 'checks of proof')
#Additionally, no accountability of prover to be giving the correct information and technically doesn't prove anything either

#Possible check algorithm with current information
def check_p(p1: list, l1: list):
    assert(len(p1) == (len(l1) + 1))
    num_checks = random.randint(1, int(math.sqrt(len(l1))))
    for check in range(num_checks):
        index = random.randint(0,len(p1)-2)
        if not index:
            return p1[0] == p1[-1]
        elif not l1[index] == abs(p1[index + 1] - p1[index]):
            return False
    return True

print(check_p(p,l))

#To help make it more ZK, we need to add randomness
#1. Instead of m as it was given to us, we flip a coin. If it shows heads, we leave m as it is, if it shows tails, we multiply all of m's elements by −1 Note that since its elmenets were initially −1 and 1 and its dot product with l was 0, this does not change its dot product with l at all.
#2. We choose a random number r and add it to all the elements of p This does not effect the second property of p but it changes the first property such that the first and last elements of p now may not be zero. However, they must still be identical to one another.

#Given implementation of a 'p' or witness creation function that uses randomness (from two previous statements) to create a random looking witness

def get_witness(problem, assignment):
    """
    Given an instance of a partition problem via a list of numbers (the problem) and a list of
    (-1, 1), we say that the assignment satisfies the problem if their dot product is 0.
    """
    #The sum
    sm = 0
    #The max partial sum before adding a baseline random value
    mx = 0
    #The flip of {1,-1}
    side_obfuscator = 1 - 2 * random.randint(0, 1)
    #The 'p' list
    witness = [sm]
    assert len(problem) == len(assignment)
    #for each l[i] & m[i] pair
    for num, side in zip(problem, assignment):
        assert side == 1 or side == -1
        #computing partial sum on the fly along with flip, really cool code and better than what I did
        sm += side * num * side_obfuscator
        witness += [sm]
        mx = max(mx, num)
    # make sure that it is a satisfying assignment
    assert sm == 0
    shift = random.randint(0, mx)
    #applying baseline random value
    witness = [x + shift for x in witness]
    return witness

given_p = get_witness(l,m)

#print(p) #original witness created
#print(check_p(p,l)) #witness check -> true
#print(given_p) #more random witness created
#print(check_p(given_p,l)) #witness check -> true, even with randomness

#Ok, this is good, but this doesn't provide any trust as a malivious prover could just forge some arbitrary values to create a false witness so we need to make some sort of trust mechanism
#We will use a Merkle Tree with the SHA256 hash to approach some trust mechanism for this

def hash_string(s):
    return hashlib.sha256(s.encode()).hexdigest()

