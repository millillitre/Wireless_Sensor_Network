from utils import *
import struct
import zlib

addr_gateway = "11010010"
TRAME_SIZE = 22  # 1(addr) + 16(payload) + 1(padding) + 4(crc)
cle_crc = "100000100110000010001110110110111"

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
    # recuperation de la trame et application de l'algorithme 
    reste = mod2div(trame_string,cle)
    a_comparer = '0'*(len(cle)-1)
    
    if reste == a_comparer: # comparaion du reste avec la valeur attendue
        print("Trame correcte !")
        verified_payload = trame_string[:-32]
        return(verified_payload) # renvoi de la charge utile
    else: # sinon erreur crc
        print("Erreur bit sur la trame recue : rest = " + reste)
        return(None)

def decoder(verified_payload):
    adr_dest = verified_payload[0:8]
    adr_sender = verified_payload[8:16]
    data = verified_payload[16:]
    return adr_dest, adr_sender, data

def decode_mac_frame_to_text(filename, output_txt):
    with open(filename, "rb") as f:
        data = f.read()

    n_trames = len(data) // TRAME_SIZE
    print(f"Nombre de trames : {n_trames}\n")

    with open(output_txt, "w") as out:
        out.write("Trame\tAddress\tCowID\tLatitude\tLongitude\tAltitude\tCRC_OK\n")
        for i in range(n_trames):
            trame = data[i*TRAME_SIZE:(i+1)*TRAME_SIZE]

            if len(trame) < TRAME_SIZE:
                print(f"Trame {i+1} trop courte, skipped")
                continue

            # Décodage : Header(1) + Payload(16) + Bourrage(1) + CRC(4)
            address, cow_id, latitude, longitude, altitude, padding, crc_rx = struct.unpack(">BIIII B I", trame)

            # CRC calculé sur tout sauf les 4 derniers octets (CRC)
            # crc_calc = zlib.crc32(trame[:-4]) & 0xFFFFFFFF
            crc_ok = crc_rx == cle_crc

            out.write(f"{i+1}\t{hex(address)}\t{cow_id}\t{latitude}\t{longitude}\t{altitude}\t{crc_ok}\n")

    print(f"Données enregistrées dans {output_txt}")

def main(filename_in="payload.bin", filename_out="app.bin"):
    with open(filename_in, "rb") as f:
        payload_bytes = f.read()
    
    # Convertir les bytes en string binaire pour traitement
    payload = ''.join(format(byte, '08b') for byte in payload_bytes)
    
    if len(payload) != 0:
        verified_payload = check_crc(payload, cle_crc)
        if verified_payload != None:
            adr_dest, adr_sender, data = decoder(verified_payload)
            if adr_dest == addr_gateway:
                # Convertir data (string binaire) en bytes et écrire en binaire
                data_bytes = bytes(int(data[i:i+8], 2) for i in range(0, len(data), 8))
                with open(filename_out, "ab") as f:
                    f.write(data_bytes)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        filename_in = sys.argv[1]
        filename_out = sys.argv[2]
    elif len(sys.argv) > 1:
        filename_in = sys.argv[1]
        filename_out = "app.bin"
    else:
        filename_in = "payload.bin"
        filename_out = "app.bin"
    main(filename_in, filename_out)
				