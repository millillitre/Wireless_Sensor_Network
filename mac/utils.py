import os

# -------------------- Conversion Functions --------------------

def binary_to_ascii(binary_string):

    ascii_text=""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        ascii_text += chr(int(byte,2))
    return ascii_text

def ascii_to_binary(ascii_text):

    binary_string= ""
    for char in ascii_text:
        binary_string += f"{ord(char):08b}"
    #binary = string_to_binary(binary_string)
    return binary_string

def string_to_binary(input_string):
    output_binary = b''
    for bit in input_string:
        output_binary += b'0' if bit=='0' else b'1'
    return output_binary


# -------------------- CRC Functions --------------------      
def xor(a, b):
 
    # initialize result
    result = []
 
    # Traverse all bits, if bits are
    # same, then XOR is 0, else 1
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
 
    return (''.join(result))

def mod2div(dividend, divisor):
 
    # Number of bits to be XORed at a time.
    pick = len(divisor)
 
    # Slicing the dividend to appropriate
    # length for particular step
    tmp = dividend[0 : pick]
 
    while pick < len(dividend):
 
        if tmp[0] == '1':
 
            # replace the dividend by the result
            # of XOR and pull 1 bit down
            tmp = xor(divisor, tmp) + dividend[pick]
 
        else: # If leftmost bit is '0'
 
            # If the leftmost bit of the dividend (or the
            # part used in each step) is 0, the step cannot
            # use the regular divisor; we need to use an
            # all-0s divisor.
            tmp = xor('0'*pick, tmp) + dividend[pick]
 
        # increment pick to move further
        pick += 1
 
    # For the last n bits, we have to carry it out
    # normally as increased value of pick will cause
    # Index Out of Bounds.
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
 
    checkword = tmp
    return checkword

def encoder(data, key):
 
    l_key = len(key)
 
    # Appends n-1 zeroes at end of data
    appended_data = data + '0'*(l_key-1)
    remainder = mod2div(appended_data, key)
 
    # Append remainder in the original data
    return data + remainder

def check_crc(trame_string, cle):
    reste = mod2div(trame_string,cle)
    a_comparer = '0'*(len(cle)-1)
    if reste == a_comparer:
        print("Trame correcte !")
        trame_sans_crc = trame_string[:-3]
        return(trame_sans_crc)
    else:
        print("Erreur bit sur la trame recue : rest = " + reste)
        return(None)


# -------------------- Payoad Functions --------------------
def decoder(trame_sans_crc):
    type_trame_recu = trame_sans_crc[:5]
    add_dest_recu = trame_sans_crc[5:53]
    add_src_recu = trame_sans_crc[53:101]
    data_recu = trame_sans_crc[101:]
    return type_trame_recu, add_dest_recu, add_src_recu, data_recu

def creer_trame(type_trame, add_dest, add_src, data):
    trame = type_trame + add_dest + add_src + data
    #print("trame construite : ")
    #print(trame)
    #print(type(trame))
    #print('\n')
    return(trame)

# -------------------- File Functions --------------------
def read_and_delete(fichier, supp):
	#lire la ligne
	f = open(fichier, "r")
	lignes = f.readlines()
	data=""
	if len(lignes)>0:
		data_bin = lignes[0]

		f.close()

		#supprimer la ligne
		g = open(fichier, "w")
		i = 0
		for ligne_boucle in lignes:
			if i != 0:
				g.write(ligne_boucle)
			else:
				i += 1
		g.close()

		#formater la ligne pour renvoi
		#data = data_bin.decode('utf-8')
		
		#if supp!=0:
		#data = data[:-1] #supprimer le retour à la ligne #si ça bug peut etre ici 10/01
		data = ascii_to_binary(data_bin)

	return(data)

def write_line(fichier, ligne):
    f = open(fichier, "a")
    ligne_bin = string_to_binary(ligne)
    ligne_ascii = binary_to_ascii(ligne_bin)
    if(os.stat(fichier).st_size != 0):
        f.write("\n")
    f.write(ligne_ascii)
    f.close()
   
def read_all(fichier):
    f = open(fichier)
    lines = f.readlines()
    f.close()
    return(lines)

def reset_fichier(fichier):
    os.remove(fichier)
    f = open(fichier,"w")
    print("reset")


