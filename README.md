# zero-knowledge-proof-explorations
Code related to my exploration of zero-knowledge proofs/arguments/whatever I find is related. I find the concept of them very interesting and from this exploration I hope to learn the techniques that are used to achieve the concepts and where they are used.


Just following and trying to study ZK proofs, arguments, and whatever zSNARKS are
Link to blog post I'm following:
http://www.shirpeled.com/2018/09/a-hands-on-tutorial-for-zero-knowledge.html?m=1

Definitions:
    
    -ZK Proof: can be completely trusted even if prover has unlimited computational power to try to prove something false
   
    -ZK Argument: can be trusted with the assumption that the prover would be polynomial bound(?) if they try to prove something false
    
    -Prover: party that is trying to prove the claim to the verifier
    
    -Verifier: party that is being proved something and shouldn't know anything about the data or method being used by the prover unless given information
    
    -Partion Problem: given an array of integers, can you organize the elements into 2 groups such that they have the same sum (NP-complete problem?)
    
    -Process that doesn't give new information: if output appears random, or more precisely - if it is uniformly distributed over some appropriately chosen domain
