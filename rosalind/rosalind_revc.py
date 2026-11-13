# Rosalind Problem 3: Complementing a Strand of DNA

dna="AAAACCCGGT"

complement = dna.replace("A","t").replace("T","a").replace("C","g").replace("G","c").upper()
reverse_complement = complement[::-1]

print(reverse_complement)