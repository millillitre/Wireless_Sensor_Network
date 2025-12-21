import numpy as np
import struct
import zlib
import random
from gnuradio import gr
import pmt

# taille d'une trame (1 byte address + 4*4 bytes data + 1 byte padding + 4 bytes CRC)
FRAME_LEN = 1 + 4 * 4 + 1 + 4 

class blk(gr.sync_block):
    def __init__(self, address=0x2B, cow_id=2709, min_lat=48000000, max_lat=49000000, min_lon=1500000, max_lon=2500000, min_alt=100, max_alt=200):
        """Arguments de la fonction qui apparaissent comme paramètres dans GRC"""
        gr.sync_block.__init__(
            self,
            name='Random MAC Frame Generator',
            in_sig=None,
            out_sig=[np.byte]
        )
        
        # initialisation des paramètres
        self.address = int(address)
        self.cow_id = int(cow_id)
        self.min_lat = int(min_lat)
        self.max_lat = int(max_lat)
        self.min_lon = int(min_lon)
        self.max_lon = int(max_lon)
        self.min_alt = int(min_alt)
        self.max_alt = int(max_alt)

        self.frame_len = FRAME_LEN

    def generate_random_frame(self):
        # genere des valeurs aléatoires
        latitude = random.randint(self.min_lat, self.max_lat)
        longitude = random.randint(self.min_lon, self.max_lon)
        altitude = random.randint(self.min_alt, self.max_alt)
        
        # payload (header + données)
        # Format: >BIIII (Big-endian: 1 byte + 4 * 4 bytes)
        payload_bytes = struct.pack(">BIIII", self.address, self.cow_id, latitude, longitude, altitude)
        
        # ajoute 1 octet de bourrage
        payload_bytes += b"\x00"
        
        # calcule le CRC (sur tout sauf le CRC lui-même)
        # & 0xFFFFFFFF est pour assurer une valeur non signée de 32 bits
        crc = zlib.crc32(payload_bytes) & 0xFFFFFFFF
        
        # trame complète = payload + bourrage + CRC
        # Format pour le CRC: >I (Big-endian: 4 bytes)
        frame = payload_bytes + struct.pack(">I", crc)
        
        return frame

    def work(self, input_items, output_items):

        out = output_items[0]
        frame_len = FRAME_LEN
        if len(out) < frame_len:
             return 0
             
        frame_bytes = self.generate_random_frame()
        frame_np = np.frombuffer(frame_bytes, dtype=np.byte)

        out[:frame_len] = frame_np

        self.add_item_tag(0,
                          self.nitems_written(0),
                          pmt.intern("packet_len"),
                          pmt.from_long(frame_len))
        
        return frame_len
