class SHA1:
    def __init__(self, message: bytes):
        self.message = message
        self._prepare_message()

        # Inicjalizacja rejestrów
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0

        self.current_block = 0
        self.finished = False

    def _prepare_message(self):
        message = self.message.encode('utf-8')
        original_length = len(message) * 8
        message += b'\x80'
        while (len(message) * 8) % 512 != 448:
            message += b'\x00'
        message += original_length.to_bytes(8, 'big')
        self.blocks = [
            message[i:i+64]
            for i in range(0, len(message), 64)
        ]

    def _left_rotate(self, n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def run_iter(self):
        if self.current_block >= len(self.blocks):
            self.finished = True
            return

        block = self.blocks[self.current_block]
        w = list(int.from_bytes(block[i:i+4], 'big') for i in range(0, 64, 4))
        for i in range(16, 80):
            w.append(self._left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1))

        a, b, c, d, e = self.h0, self.h1, self.h2, self.h3, self.h4

        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (self._left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
            e = d
            d = c
            c = self._left_rotate(b, 30)
            b = a
            a = temp

        self.h0 = (self.h0 + a) & 0xFFFFFFFF
        self.h1 = (self.h1 + b) & 0xFFFFFFFF
        self.h2 = (self.h2 + c) & 0xFFFFFFFF
        self.h3 = (self.h3 + d) & 0xFFFFFFFF
        self.h4 = (self.h4 + e) & 0xFFFFFFFF

        self.current_block += 1

    def run_all(self, vis: bool = False):
        while not self.finished:
            if vis:
                print(self.get_registers(False))
            self.run_iter()

        digest = (self.h0.to_bytes(4, 'big') +
                  self.h1.to_bytes(4, 'big') +
                  self.h2.to_bytes(4, 'big') +
                  self.h3.to_bytes(4, 'big') +
                  self.h4.to_bytes(4, 'big'))
        return digest.hex()

    def get_registers(self, littleEndian: bool = True) -> str:
        endianess = 'little' if littleEndian else 'big'
        digest = (self.h0.to_bytes(4, endianess) +
                  self.h1.to_bytes(4, endianess) +
                  self.h2.to_bytes(4, endianess) +
                  self.h3.to_bytes(4, endianess) +
                  self.h4.to_bytes(4, endianess))
        return digest.hex()

    def get_h(self, littleEndian: bool = True) -> str:
        return self.get_registers(littleEndian)


# Example usage:
import hashlib
print(hashlib.new('sha1', 'a'.encode()).hexdigest())
print(SHA1('a').run_all())