# coding: UTF-8
import scipy
#Dico.py - construit l'arbre du code du Huffman de la source
#1.1 (corr) : H = 3.9

texte = '''il y avait en vestphalie dans le chateau de monsieur le baron de
thunder ten tronckh un jeune garcon a qui la nature avait donne les
moeurs les plus douces sa physionomie annoncait son ame il avait le
jugement assez droit avec l esprit le plus simple c est je crois pour
cette raison qu on le nommait candide les anciens domestiques de la
maison soupconnaient qu il etait fils de la soeur de monsieur le baron
et d un bon et honnete gentilhomme du voisinage que cette demoiselle
ne voulut jamais epouser parce qu il n avait pu prouver que soixante
et onze quartiers et que le reste de son arbre genealogique avait ete
perdu par l injure du temps monsieur le baron etait un des plus
puissants seigneurs de la vestphalie car son chateau avait une porte
et des fenetres sa grande salle meme etait ornee d une tapisserie tous
les chiens de ses basses cours composaient une meute dans le besoin
ses palefreniers etaient ses piqueurs le vicaire du village etait son
grand aumonier ils l appelaient tous monseigneur et ils riaient quand
il faisait des contes madame la baronne qui pesait environ trois cent
cinquante livres s attirait par la une tres grande consideration et
faisait les honneurs de la maison avec une dignite qui la rendait
encore plus respectable sa fille cunegonde agee de dix sept ans etait
haute en couleur fraiche grasse appetissante le fils du baron
paraissait en tout digne de son pere le precepteur pangloss etait l
oracle de la maison et le petit candide ecoutait ses lecons avec toute
la bonne foi de son age et de son caractere pangloss enseignait la
metaphysico theologo cosmolonigologie il prouvait admirablement qu il
n y a point d effet sans cause et que dans ce meilleur des mondes
possibles le chateau de monseigneur le baron etait le plus beau des
chateaux et madame la meilleure des baronnes possibles'''


# Construction d'une table de frequences
#
# Entree: alphabet et frequences associees
# Sortie: un dictionnaire qui associe chaque symbole present a sa frequence

alph = [' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z']
prob = [0.1836, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0001, 0.0031, 0.0021, 0.0008]


def table_frequences_part (alphabet, loi):
	table = {}
	for i, char in enumerate(alphabet):
		table[char] = prob[i]
	return table

# Construction d'un arbre de Huffman
#
# Entree: un dictionnaire qui associe chaque symbole a sa frequence
# Sortie: un arbre binaire portant les symboles aux feuilles
import heapq

def huffman_arbre (frequences):
	#Construction d'un tas de feuilles avec les lettres :
	tas = [(freq, {'val': lettre}) for (lettre, freq) in frequences.items()]
	heapq.heapify(tas)

	#aggregation des arbres : 
	while len(tas) >= 2:
		freq1, gauche = heapq.heappop(tas)
		freq2, droite = heapq.heappop(tas)
		heapq.heappush(tas, (freq1 + freq2, {'gauche': gauche, 'droite': droite}))

	#Renvoi de l'arbre construit : 
	_, arbre = heapq.heappop(tas)
	return arbre


# Transformation d'un arbre binaire en code.
#
# Entree: un arbre binaire portant des symboles aux feuilles
# Sortie: un dictionnaire qui associe a  chaque valeur de feuille le code
#   correspondant, comme liste d'entiers (0 ou 1)
#
# La methode employee est recursive, on utilise une fonction auxiliaire qui
# etablit le code de chaque valeur d'un sous-arbre en connaissant le prefixe
# commun des codes de ce sous-arbre.

def table_codage (arbre):
    code = {}

    def code_sous_arbre (prefixe, noeud):
        if 'gauche' in noeud:
            # cas d'un noeud interne : 
            code_sous_arbre(prefixe + [0], noeud['gauche'])
            code_sous_arbre(prefixe + [1], noeud['droite'])
        else:
            # cas d'une feuille : 
            code[noeud['val']] = prefixe

    code_sous_arbre([], arbre)
    return code

#Codage et decodage de suites de bits :
 
## Fonctions auxiliaires: codage des entiers en base 2
# Transcrit un nombre décimal en base 2
#
# Entree : nombre base 10 et nombre bits souhaites
# Sortie : Liste de bits - nombre en base 2
def code_base2 (nombre, taille):
    bits = []
    for i in range(taille):
        bits.insert(0, nombre % 2)
        nombre = nombre / 2
    return bits

# Transcrit un nombre binaire en base 10
#
# Entree : nombre base 2
# Sortie : (int) nombre en base 10
def decode_base2 (bits):
    nombre = 0
    for bit in bits:
        nombre = 2 * nombre + bit
    return nombre

# Gestion de l'ecriture de bits dans une chaine de characteres

# L'etat est un dictionnaire comportant les champs suivants:
# - sortie : la sortie produite jusque la  (suite d'octets sous forme de chaine de caracteres)
# - tampon : une suite de bits, de longueur au plus 7, qui contient les
#   premiers bits a ecrire dans le prochain octet

# Creation de l'etat initial : 
def init_sortie():
	return {'sortie': '', 'tampon': []}

#Ecriture d'un bit
def ecrire_bit (etat, bit):
	bits = etat['tampon'] + [bit]
	if len(bits) == 8:
		etat['sortie'] = etat['sortie'] + chr(decode_base2(bits))
		etat['tampon'] = []
	else:
		etat['tampon'] = bits

#Ecriture d'une suite de bits
def ecrire_bits (etat, bits):
	for bit in bits:
		ecrire_bit(etat, bit)


#Ecriture des derniers bits restant dans le tampon lors de l'extraction du resultat : 
def sortie_finale (etat):
	if len(etat['tampon']) > 0:
		ecrire_bits(etat, [0]*(8 - len(etat['tampon'])))
	return etat['sortie']

##Lecture de suites de bits dans une chaine de characteres
# Ici, l'etat est un dictionnaire comportant les champs suivants:
# - entree : le texte a decomposer
# - position : la position du prochain caractere a lire
# - tampon : un suite de bits a lire avant le prochain caractere (de longueur au plus 7)

#Initialisation
def init_entree (entree):
	return {'entree': entree, 'position': 0, 'tampon': []}

#Lecture d'un bit
def lire_bit (etat):
	suite = etat['tampon']
	#Lire le prochain char si besoin : 
	if suite == []:
		caractere = etat['entree'][etat['position']]
		etat['position'] = etat['position'] + 1
		suite = code_base2(ord(caractere), 8)

	#Extraire le premier bit : 
	etat['tampon'] = suite[1:]
	return suite[0]

#Lecture d'une suite de bits : 
def lire_bits (etat, taille):
    bits = []
    for i in range(taille):
        bits.append(lire_bit(etat))
    return bits

#Codage des arbres binaires : 
## Codage des arbres binaires

# NOTE : Le codage d'une feuille est un bit 0 suivi du code
# du caractere, le codage d'un arbre non reduit a une feuille est un bit 1
# suivi des codages des sous-arbres gauche et droit.

def ecrire_arbre (etat, arbre):
    if 'gauche' in arbre:
        ecrire_bit(etat, 1)
        ecrire_arbre(etat, arbre['gauche'])
        ecrire_arbre(etat, arbre['droite'])
    else:
        ecrire_bit(etat, 0)
        ecrire_bits(etat, code_base2(ord(arbre['val']), 8))

def lire_arbre (etat):
    bit = lire_bit(etat)
    if bit == 1:
        gauche = lire_arbre(etat)
        droite = lire_arbre(etat)
        return {'gauche': gauche, 'droite': droite}
    else:
        code = decode_base2(lire_bits(etat, 8))
        return {'val': chr(code)}

### Codage de Huffman complet : 
def code_huffman (texte):
	texte = texte.replace('\n', ' ') 
	#print(texte)
	#print(len(texte)) => 1830
	etat = init_sortie()
	ecrire_bits(etat, code_base2(len(texte), 32))
	if len(texte) != 0:
		table = table_frequences_part(alph, prob)
		arbre = huffman_arbre (table)
		ecrire_arbre(etat, arbre)
	
	if 'val' not in arbre:
		code = table_codage(arbre)
		for caractere in texte:
			ecrire_bits(etat, code[caractere])

	return sortie_finale(etat)

def decode_huffman (chaine):
    entree = init_entree(chaine)
    taille = decode_base2(lire_bits(entree, 32))

    if taille == 0:
        return ''

    arbre = lire_arbre(entree)
    if 'val' in arbre:
        return arbre['val'] * taille

    texte = ''
    etat = arbre
    while taille > 0:
        if lire_bit(entree) == 0:
            etat = etat['gauche']
        else:
            etat = etat['droite']
        if 'val' in etat:
            texte = texte + etat['val']
            taille = taille - 1
            etat = arbre

    return texte

#tests : 
#print(table_frequences_part(alph, prob)) #--> success
#print(huffman_arbre (table_frequences_part(alph, prob))) #--> success
#print(table_codage (huffman_arbre (table_frequences_part(alph, prob)))) #--> success
print("Le texte a coder est : " + texte + "\n\n")
code = code_huffman(texte)
print("Le texte code est : " + code + "\n\n")
#print(code) #--> success
decode = decode_huffman (code)
print("Le texte decode est : " + decode + "\n\n")
#print (decode_huffman (code))

