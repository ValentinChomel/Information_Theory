#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import defaultdict
from fractions import Fraction

fichier = open("texte.txt", "r")
texte = fichier.read()
fichier.close()

# Construction de la distribution de proba en fonction d'un texte
#
# input : texte
# output : dictionnaire caracteres : fractions 

def const_prob(input_code):
	counts = defaultdict(int)

	for code in input_code:
		counts[code] += 1
	counts[256] = 1

	output = dict()
	length = len(input_code)
	cumulative = 0

	for code in sorted(counts, key=counts.get, reverse=True):
		current_count = counts[code]
		prob_pair = Fraction(cumulative, length), Fraction(current_count, length)
		output[code] = prob_pair
		cumulative += current_count

	return output

# Encodage fraction
def encode_fraction_range(input_code, input_prob):
    start = Fraction(0, 1) #0
    width = Fraction(1, 1) #1

    for code in input_code:
        d_start, d_width = input_prob[code]
        start += d_start * width
        width *= d_width

    return start, start + width

# Trouve le code binaire a partir des fractions
def find_binary_fraction(input_start, input_end):
    output_fraction = Fraction(0, 1)
    output_denominator = 1

    while not (input_start <= output_fraction < input_end):
        output_numerator = 1 + ((input_start.numerator * output_denominator) // input_start.denominator)
        output_fraction = Fraction(output_numerator, output_denominator)
        output_denominator *= 2

    return output_fraction

def decode_fraction(input_fraction, input_prob):
    output_codes = []
    code = 257

    while code != 256:
        for code, (start, width) in input_prob.items():
            if 0 <= (input_fraction - start) < width:
                input_fraction = (input_fraction - start) / width

                if code < 256:
                    output_codes.append(code)
                break

    return ''.join([chr(code) for code in output_codes])


#string = 'Ceci est un test'
string = texte.replace('\n', ' ')
codes = [ord(char) for char in string] + [256]

prob = const_prob(codes)
#print('probabilités:', repr(prob))
print('len(prob):', repr(len(prob)))

fraction_range = encode_fraction_range(codes, prob)
#print('fraction_range:', repr(fraction_range))

decoded_fraction = decode_fraction(fraction_range[0], prob)
#print('decoded_fraction:', repr(decoded_fraction))

binary_fraction = find_binary_fraction(fraction_range[0], fraction_range[1])
print('binary_fraction:', repr(binary_fraction))

print('binaire:', float(binary_fraction))

decoded_binary_fraction = decode_fraction(binary_fraction, prob)
print('decoded_binary_fraction:', repr(decoded_binary_fraction))

#Tests : 
#prob = const_prob(texte)
#print(prob)
#print(encode_fraction_range(texte, prob))



