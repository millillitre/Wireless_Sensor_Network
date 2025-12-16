import struct
import zlib

def write_mac_frame(address, cow_id, latitude, longitude, altitude, filename="payload.bin"):
    # Header + Payload
    payload_bytes = struct.pack(">BIIII", address, cow_id, latitude, longitude, altitude)
    # Ajouter 1 octet de bourrage avant le CRC
    payload_bytes += b"\x00"
    # CRC-32 calculé sur tout sauf le CRC lui-même
    crc = zlib.crc32(payload_bytes) & 0xFFFFFFFF
    # Frame complète = payload + bourrage + CRC
    frame = payload_bytes + struct.pack(">I", crc)
    # Écriture binaire
    with open(filename, "ab") as f:
        f.write(frame)


write_mac_frame(
    address=0x2B,
    cow_id=2709,
    latitude=48512345,
    longitude=2156789,
    altitude=130,
    filename="mac_frame.bin"
)