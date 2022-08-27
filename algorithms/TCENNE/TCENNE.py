# 1: Phe                5: Val      9: Ala        13: Gln       17: Glu
# 2: Leu                6: Ser      10: Tyr       14: Asn       18: Cys
# 3: Ile                7: Pro      11: Stop      15: Lys       19: Trp
# 4: Met | Start        8: Thr      12: His       16: Asp       20: Arg
# 21: Gly
codon_mapping: dict = {
    'TTT': 1,      'TCT': 6,      'TAT': 10,      'TGT': 18,    'CTT': 2,      'CCT': 7,      'CAT': 12,      'CGT': 20,
    'TTC': 1,      'TCC': 6,      'TAC': 10,      'TGC': 18,    'CTC': 2,      'CCC': 7,      'CAC': 12,      'CGC': 20,
    'TTA': 2,      'TCA': 6,      'TAA': 11,      'TGA': 11,    'CTA': 2,      'CCA': 7,      'CAA': 13,      'CGA': 20,
    'TTG': 2,      'TCG': 6,      'TAG': 11,      'TGG': 19,    'CTG': 2,      'CCG': 7,      'CAG': 13,      'CGG': 20,
    
    'ATT': 3,      'ACT': 8,      'AAT': 14,      'AGT': 6,     'GTT': 5,      'GCT': 9,      'GAT': 16,      'GGT': 21,
    'ATC': 3,      'ACC': 8,      'AAC': 14,      'AGC': 6,     'GTC': 5,      'GCC': 9,      'GAC': 16,      'GGC': 21,
    'ATA': 3,      'ACA': 8,      'AAA': 15,      'AGA': 20,    'GTA': 5,      'GCA': 9,      'GAA': 17,      'GGA': 21,
    'ATG': 4,      'ACG': 8,      'AAG': 15,      'AGG': 20,    'GTG': 5,      'GCG': 9,      'GAG': 17,      'GGG': 21,
}


def split_into_components(codons: list) -> list:
        pass


def split_into_codons(chromosome: str) -> list:
    codons, codon = [], []
    span = len(chromosome)
    for i in range(span):
        place = i % 3
        if place == 0:
            codon = [chromosome[i]]
        elif place == 1:
            codon.append(chromosome[i])
        else:
            codon.append(chromosome[i])
            codons.append("".join(codon))
        if i == span - 1:
            codons.append("".join(codon))
    return codons



class DNA():
    def __init__(self) -> None:
        self.chromosome = ''



