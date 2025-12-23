import numpy as np
from gnuradio import gr
import struct
import zlib

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='MAC Decoder & Display',
            in_sig=[np.uint8],
            out_sig=None
        )
        self.trame_size = 22
        self.buffer = bytearray()
        
        print("\n" + "="*60)
        print(f"{'Trame':<8} | {'Addr':<6} | {'CowID':<8} | {'Lat':<10} | {'Long':<10} | {'Alt':<10} | {'CRC':<6}")
        print("-" * 60)

    def work(self, input_items, output_items):
        in_data = input_items[0]
        
        self.buffer.extend(in_data.tobytes())

        # tant qu'on a assez de données pour au moins une trame
        while len(self.buffer) >= self.trame_size:
            trame = self.buffer[:self.trame_size]
            self.buffer = self.buffer[self.trame_size:] # On vide ce qu'on a lu

            try:
                res = struct.unpack(">BIIIIBI", trame)
                address, cow_id, lat, lon, alt, padding, crc_rx = res

                # vérification CRC
                crc_calc = zlib.crc32(trame[:-4]) & 0xFFFFFFFF
                crc_ok = "OK" if crc_rx == crc_calc else "BAD"

                print(f"RECUE    | {hex(address):<6} | {cow_id:<8} | {lat:<10} | {lon:<10} | {alt:<10} | {crc_ok:<6}")
                
            except Exception as e:
                print(f"Erreur décodage: {e}")

        return len(in_data)
