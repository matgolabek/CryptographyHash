import numpy as np

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

class RIPEMD160:
    def __init__(self, message: str = None,  h1: str = '67452301', h2: str = 'efcdab89',  h5: str = 'c3d2e1f0',
                add_const0: str = '00000000', add_const1: str = '5a827999', add_const2: str = '6ed9eba1', add_const3: str = '8f1bbcdc', add_const4: str = '0953fd4e',
                add_const0r: str = '50a28be6', add_const1r: str = '5c4dd124', add_const2r: str = '6d703ef3', add_const3r: str = '7a6d76e9', add_const4r: str = '00000000',
                order_list0: list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                order_list1: list[int] = [7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8],
                order_list2: list[int] = [3,10,14, 4, 9,15, 8, 1, 2, 7, 0, 6,13,11, 5,12],
                order_list3: list[int] = [1, 9,11,10, 0, 8,12, 4,13, 3, 7,15,14, 5, 6, 2],
                order_list4: list[int] = [4, 0, 5, 9, 7,12, 2,10,14, 1, 3, 8,11, 6,15,13],
                order_list0r: list[int] = [5,14, 7, 0, 9, 2,11, 4,13, 6,15, 8, 1,10, 3,12],
                order_list1r: list[int] = [6,11, 3, 7, 0,13, 5,10,14,15, 8,12, 4, 9, 1, 2],
                order_list2r: list[int] = [15, 5, 1, 3, 7,14, 6, 9,11, 8,12, 2,10, 0, 4,13],
                order_list3r: list[int] = [8, 6, 4, 1, 3,11,15, 0, 5,12, 2,13, 9, 7,10,14],
                order_list4r: list[int] = [12,15,10, 4, 1, 5, 8, 7, 6, 2,13,14, 0, 3, 9,11],
                shift_list0: list[int] = [11,14,15,12, 5, 8, 7, 9,11,13,14,15, 6, 7, 9, 8],
                shift_list1: list[int] = [7, 6, 8,13,11, 9, 7,15, 7,12,15, 9,11, 7,13,12],
                shift_list2: list[int] = [11,13, 6, 7,14, 9,13,15,14, 8,13, 6, 5,12, 7, 5],
                shift_list3: list[int] = [11,12,14,15,14,15, 9, 8, 9,14, 5, 6, 8, 6, 5,12],
                shift_list4: list[int] = [9,15, 5,11, 6, 8,13,12, 5,12,13,14,11, 8, 5, 6],
                shift_list0r: list[int] = [8, 9, 9,11,13,15,15, 5, 7, 7, 8,11,14,14,12, 6],
                shift_list1r: list[int] = [9,13,15, 7,12, 8, 9,11, 7, 7,12, 7, 6,15,13,11],
                shift_list2r: list[int] = [9, 7,15,11, 8, 6, 6,14,12,13, 5,14,13,13, 7, 5],
                shift_list3r: list[int] = [15, 5, 8,11,14,14, 6,14, 6, 9,12, 9,12, 5,15, 8],
                shift_list4r: list[int] = [8, 5,12, 9,12, 5,14, 6, 8,13, 6, 5,15,13,11,11]):

        h3, h4 = chain_constraints(h1, h2)

        # Initial hash values (in hex, little-endian)
        self.h0 = int(h1, 16)
        self.h1 = int(h2, 16)
        self.h2 = int(h3, 16)
        self.h3 = int(h4, 16)
        self.h4 = int(h5, 16)

        # Working registers for left and right branches
        self.A = self.h0
        self.B = self.h1
        self.C = self.h2
        self.D = self.h3
        self.E = self.h4

        self.Ap = self.h0
        self.Bp = self.h1
        self.Cp = self.h2
        self.Dp = self.h3
        self.Ep = self.h4

        # Constants for each round
        self.K = [int(add_const0, 16), int(add_const1, 16), int(add_const2, 16), int(add_const3, 16), int(add_const4, 16)]
        self.Kp = [int(add_const0r, 16), int(add_const1r, 16), int(add_const2r, 16), int(add_const3r, 16), int(add_const4r, 16)]

        # Message word order for left line
        self.r = order_list0 + order_list1 + order_list2 + order_list3 + order_list4

        # Message word order for right line
        self.rp = order_list0r + order_list1r + order_list2r + order_list3r + order_list4r

        # Rotation amounts for left line
        self.s = shift_list0 + shift_list1 + shift_list2 + shift_list3 + shift_list4

        # Rotation amounts for right line
        self.sp = shift_list0r + shift_list1r + shift_list2r + shift_list3r + shift_list4r

        self.finished = False
        if message is None:
            self.message = None
            self.number_of_blocks = 0
        else:
            self.message, self.number_of_blocks = self.__preprocess(message)

        self.block_counter = 0
        self.step_counter = 0  # 0–79 for 80 steps total

    def __preprocess(self, message: str) -> tuple[bytes, int]:
        if len(message) == 0:
            raise ValueError("Message cannot be empty.")
        bit_length = len(message) * 8
        message = message.encode('utf-8') + b'\x80'
        while (len(message) * 8) % 512 != 448:
            message += b'\x00'
        message += bit_length.to_bytes(8, byteorder='little')
        return message, len(message) // 64

    def F(self, j, x, y, z):
        if 0 <= j <= 15:   return x ^ y ^ z
        elif 16 <= j <= 31: return (x & y) | (~x & z)
        elif 32 <= j <= 47: return (x | ~y) ^ z
        elif 48 <= j <= 63: return (x & z) | (y & ~z)
        elif 64 <= j <= 79: return x ^ (y | ~z)

    def rotate_left(self, x, n):
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def run_iter(self):
        if self.finished:
            return True

        block = self.message[self.block_counter * 64 : (self.block_counter + 1) * 64]
        X = [int.from_bytes(block[i*4:i*4+4], byteorder='little') for i in range(16)]

        j = self.step_counter

        # Left line
        f = self.F(j, self.B, self.C, self.D)
        T = (self.A + f + X[self.r[j]] + self.K[j // 16]) & 0xFFFFFFFF
        T = self.rotate_left(T, self.s[j]) + self.E & 0xFFFFFFFF
        self.A, self.E, self.D, self.C, self.B = self.E, self.D, self.rotate_left(self.C, 10), self.B, T

        # Right line (similar but with prime variables and Kp/rp/sp)
        f_p = self.F(79 - j, self.Bp, self.Cp, self.Dp)
        T_p = (self.Ap + f_p + X[self.rp[j]] + self.Kp[j // 16]) & 0xFFFFFFFF
        T_p = self.rotate_left(T_p, self.sp[j]) + self.Ep & 0xFFFFFFFF
        self.Ap, self.Ep, self.Dp, self.Cp, self.Bp = self.Ep, self.Dp, self.rotate_left(self.Cp, 10), self.Bp, T_p

        self.step_counter += 1

        if self.step_counter == 80:
            # Combine left and right results
            T = (self.h1 + self.C + self.Dp) & 0xFFFFFFFF
            self.h1 = (self.h2 + self.D + self.Ep) & 0xFFFFFFFF
            self.h2 = (self.h3 + self.E + self.Ap) & 0xFFFFFFFF
            self.h3 = (self.h4 + self.A + self.Bp) & 0xFFFFFFFF
            self.h4 = (self.h0 + self.B + self.Cp) & 0xFFFFFFFF
            self.h0 = T

            self.block_counter += 1
            self.step_counter = 0

            if self.block_counter == self.number_of_blocks:
                self.finished = True
            else:
                # Reset working registers for next block
                self.A = self.h0
                self.B = self.h1
                self.C = self.h2
                self.D = self.h3
                self.E = self.h4

                self.Ap = self.h0
                self.Bp = self.h1
                self.Cp = self.h2
                self.Dp = self.h3
                self.Ep = self.h4

        return self.finished


    def run_all(self, vis: bool = False):
        """
        Run the RIPEMD-160 algorithm on the given message.
        :param vis: Whether to print internal state at each iteration.
        :return: The RIPEMD-160 hash of the message as a hexadecimal string.
        """
        while not self.finished:
            if vis:
                print(self.get_registers(False))
            self.run_iter()

        # Convert the final hash to hexadecimal format
        endianess = 'little'
        digest = (self.h0.to_bytes(4, endianess) +
                self.h1.to_bytes(4, endianess) +
                self.h2.to_bytes(4, endianess) +
                self.h3.to_bytes(4, endianess) +
                self.h4.to_bytes(4, endianess))
        return digest.hex()


    def get_registers(self, littleEndian: bool = True) -> str:
        """
        Get the current values of the working registers.
        :return: Hex representation of the working state A-E.
        """
        endianess = 'little' if littleEndian else 'big'
        digest = (self.A.to_bytes(4, endianess) +
                self.B.to_bytes(4, endianess) +
                self.C.to_bytes(4, endianess) +
                self.D.to_bytes(4, endianess) +
                self.E.to_bytes(4, endianess))
        return digest.hex()


    def get_h(self, littleEndian: bool = True) -> str:
        """
        Get the current values of the hash registers h1-h5.
        :return: Hex representation of the current hash state.
        """
        endianess = 'little' if littleEndian else 'big'
        digest = (self.h0.to_bytes(4, endianess) +
                self.h1.to_bytes(4, endianess) +
                self.h2.to_bytes(4, endianess) +
                self.h3.to_bytes(4, endianess) +
                self.h4.to_bytes(4, endianess))
        return digest.hex()

    
# # Example usage:
# RIPEMD160_hash = RIPEMD160('a4567')
# print(RIPEMD160_hash.run_all(False))  # Example usage of the RIPEMD160 class
# import hashlib

# print(hashlib.new('ripemd160', b'a4567').hexdigest())  # Using hashlib for comparison