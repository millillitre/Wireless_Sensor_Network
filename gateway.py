from utils import *

addr_gateway = "11010010"
cle_crc = "1001"

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
        verified_payload = trame_string[:-3]
        return(verified_payload)
    else:
        print("Erreur bit sur la trame recue : rest = " + reste)
        return(None)

def decoder(verified_payload):
    adr_dest = verified_payload[0:8]
    data = verified_payload[9:]
    return adr_dest, data


while True:
		payload = read_and_delete("payload.txt", supp)
		supp+=1
		if len(payload)!=0:
			verified_payload = check_crc(payload, cle_crc)
			if verified_payload != None:
				adr_dest, data = decoder(verified_payload)
				if adr_dest == addr_gateway:
				    write_line("app.txt", data) 
				