import struct
import zlib

def write_mac_frame(filename, address, cow_id, latitude, longitude, altitude):
    # Header + Payload
    payload_bytes = struct.pack(">BIIII", address, cow_id, latitude, longitude, altitude)
    # Ajouter 1 octet de bourrage avant le CRC
    payload_bytes += b"\x00"
    # CRC-32 calculé sur tout sauf le CRC lui-même
    crc = zlib.crc32(payload_bytes) & 0xFFFFFFFF
    # Frame complète = payload + bourrage + CRC
    frame = payload_bytes + struct.pack(">I", crc)
    # Écriture binaire
    with open(filename, "wb") as f:
        f.write(frame)
