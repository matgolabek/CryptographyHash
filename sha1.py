def chain_constraints(h1: str = '67452301', h2: str = 'efcdab89') -> tuple[str, str]:
    """
    Create all 4 chain constraints for MD4 hash function from 2 given numbers.
    h1 : str : first number in hex format (without 0x prefix)
    h2 : str : second number in hex format (without 0x prefix)
    Returns: tuple[str, str] : 2 chain constraints in hex format (without 0x prefix)
    """
    h3 = ''.join(list(h2)[::-1])
    h4 = ''.join(list(h1)[::-1])
    return h3, h4


class SHA1:
    def __init__(self, message: bytes = None, h1: str = '67452301', h2: str = 'efcdab89', h5: str = 'c3d2e1f0', y1: str = '5a827999',
                 y2: str = '6ed9eba1', y3: str = '8f1bbcdc', y4: str = 'ca62c1d6'):
        if message is None:
            self.message = None
        else:
            self.message = message
            self._prepare_message()

        h3, h4 = chain_constraints(h1, h2)

        # Inicjalizacja rejestrów
        self.h0 = int(h1, 16)
        self.h1 = int(h2, 16)
        self.h2 = int(h3, 16)
        self.h3 = int(h4, 16)
        self.h4 = int(h5, 16)

        self.y1 = int(y1, 16)
        self.y2 = int(y2, 16)
        self.y3 = int(y3, 16)
        self.y4 = int(y4, 16)

        self.a = self.h0
        self.b = self.h1
        self.c = self.h2
        self.d = self.h3
        self.e = self.h4

        self.current_block = 0
        self.i = 0
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
            return self.finished

        block = self.blocks[self.current_block]
        w = list(int.from_bytes(block[i:i+4], 'big') for i in range(0, 64, 4))
        for i in range(16, 80):
            w.append(self._left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1))


        if self.i < 80:
            if 0 <= self.i <= 19:
                f = (self.b & self.c) | ((~self.b) & self.d)
                k = self.y1
            elif 20 <= self.i <= 39:
                f = self.b ^ self.c ^ self.d
                k = self.y2
            elif 40 <= self.i <= 59:
                f = (self.b & self.c) | (self.b & self.d) | (self.c & self.d)
                k = self.y3
            else:
                f = self.b ^ self.c ^ self.d
                k = self.y4

            temp = (self._left_rotate(self.a, 5) + f + self.e + k + w[i]) & 0xFFFFFFFF
            self.e = self.d
            self.d = self.c
            self.c = self._left_rotate(self.b, 30)
            self.b = self.a
            self.a = temp
        else:
            self.current_block += 1
            self.i = 0

            self.h0 = (self.h0 + self.a) & 0xFFFFFFFF
            self.h1 = (self.h1 + self.b) & 0xFFFFFFFF
            self.h2 = (self.h2 + self.c) & 0xFFFFFFFF
            self.h3 = (self.h3 + self.d) & 0xFFFFFFFF
            self.h4 = (self.h4 + self.e) & 0xFFFFFFFF

        self.i += 1
        return self.finished

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
# import hashlib
# print(hashlib.new('sha1', 'a'.encode()).hexdigest())
# print(SHA1('a').run_all())