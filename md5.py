import hashlib
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

def _left_rotate(x: int, amount: int) -> int:
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

class MD5:
    def __init__(self,
                 message: str = None,
                 h1: str = '67452301',
                 h2: str = 'efcdab89',
                 add_const: str = 'sin',
                 order_list0: list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                 order_list1: list[int] = [1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12],
                 order_list2: list[int] = [5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2],
                 order_list3: list[int] = [0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9],
                 shift_list0: list[int] = [7, 12, 17, 22],
                 shift_list1: list[int] = [5, 9, 14, 20],
                 shift_list2: list[int] = [4, 11, 16, 23],
                 shift_list3: list[int] = [6, 10, 15, 21]):
        

        # Initialize chain constraints
        h3, h4 = chain_constraints(h1, h2)

        self.h1 = int(h1, 16)
        self.h2 = int(h2, 16)
        self.h3 = int(h3, 16)
        self.h4 = int(h4, 16)

        self.a = self.h1
        self.b = self.h2
        self.c = self.h3
        self.d = self.h4

        # Additive constraint
        if add_const == 'sin':
            self.T = [int((1 << 32) * abs(np.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
        elif add_const == 'cos':
            self.T = [int((1 << 32) * abs(np.cos(i + 1))) & 0xFFFFFFFF for i in range(64)]
        elif add_const == 'tan':
            self.T = [int((1 << 32) * abs(np.tan(i + 1))) & 0xFFFFFFFF for i in range(64)]
        else:
            self.T = [int((1 << 32) * abs(np.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

        # List shift
        self.shifts = (
            shift_list0 * 4
            + shift_list1 * 4
            + shift_list2 * 4
            + shift_list3 * 4
        )

        # List order
        self.indexes = order_list0 + order_list1 + order_list2 + order_list3

        self.block_counter = 0
        self.word_counter = 0
        self.op_counter = 0 

        self.finished = False

        if message is None:
            self.message = None
            self.number_of_blocks = 0
        else:
            self.message, self.number_of_blocks = self.__preprocess(message)

    def ack_message(self, message: str):
        self.message, self.number_of_blocks = self.__preprocess(message)

    def __preprocess(self, message: str) -> tuple[bytes, int]:
        """Pre-process the input message for MD4 hashing."""
        if len(message) == 0:
            raise ValueError("Message cannot be empty.")
        original_byte_len = np.clip(len(message), 1, 2**64)
        original_bit_len = original_byte_len * 8

        # Convert the message to bytes
        message = message.encode('utf-8')

        # Append the bit '1' to the message
        message += b'\x80'

        # Append zeros until the length is congruent to 448 modulo 512
        while (len(message) * 8) % 512 != 448:
            message += b'\x00'

        # Append the original length as a 64-bit integer
        message += original_bit_len.to_bytes(8, byteorder='little')
        
        return message, len(message) // 64

    def run_iter(self) -> bool:
        """
        Wykonuje jedną operację (z 64) w ramach bieżącego 512-bitowego bloku.
        Zwraca True, gdy wszystkie bloki zostały przerobione (i można odebrać digest).
        """
        if self.finished:
            return True

        start = self.block_counter * 64
        block = self.message[start : start + 64]

        M = [int.from_bytes(block[i*4:(i*4+4)], byteorder='little') for i in range(16)]

        i = self.op_counter

        if 0 <= i <= 15:
            F = (self.b & self.c) | ((~self.b) & self.d)
            g = self.indexes[i]  # g = i
        elif 16 <= i <= 31:
            F = (self.b & self.d) | (self.c & (~self.d))
            g = self.indexes[i]  # = (5*i +1) mod 16
        elif 32 <= i <= 47:
            F = self.b ^ self.c ^ self.d
            g = self.indexes[i]  # = (3*i + 5) mod 16
        else:
            F = self.c ^ (self.b | (~self.d))
            g = self.indexes[i]  # = (7*i) mod 16

        temp = (self.a + F + self.T[i] + M[g]) & 0xFFFFFFFF
        temp = _left_rotate(temp, self.shifts[i])

        self.a, self.b, self.c, self.d = self.d, (self.b + temp) & 0xFFFFFFFF, self.b, self.c

        if self.op_counter == 63:
            self.h1 = (self.h1 + self.a) & 0xFFFFFFFF
            self.h2 = (self.h2 + self.b) & 0xFFFFFFFF
            self.h3 = (self.h3 + self.c) & 0xFFFFFFFF
            self.h4 = (self.h4 + self.d) & 0xFFFFFFFF

            self.block_counter += 1

            if self.block_counter == self.number_of_blocks:
                self.finished = True
                return True
            else:
                self.a, self.b, self.c, self.d = self.h1, self.h2, self.h3, self.h4
                self.op_counter = 0
                self.word_counter = 0
                return False
        else:
            self.op_counter += 1
            self.word_counter = (self.word_counter + 1) % 16
            return False


    def run_all(self, vis: bool = False):
        """
        Run the MD4 algorithm on the given message.
        :param message: The input message to hash.
        :return: The MD4 hash of the message as a hexadecimal string.
        """
        while not self.finished:
            if vis:
                print(self.get_registers(False))
            self.run_iter()


        # Convert the final hash to hexadecimal format
        digest = (self.h1.to_bytes(4, 'little') +
                  self.h2.to_bytes(4, 'little') +
                  self.h3.to_bytes(4, 'little') +
                  self.h4.to_bytes(4, 'little'))
        return digest.hex()
    

    def get_registers(self, littleEndian: bool = True) -> str:
        """
        Get the current values of the registers.
        :return: A tuple containing the current values of the registers.
        """
        if littleEndian:
            endianess = 'little'
        else:
            endianess = 'big'
        digest = (self.a.to_bytes(4, endianess) +
                  self.b.to_bytes(4, endianess) +
                  self.c.to_bytes(4, endianess) +
                  self.d.to_bytes(4, endianess))
        return digest.hex()
    
    def get_h(self, littleEndian: bool = True) -> str:
        """
        Get the current values of the registers.
        :return: A tuple containing the current values of the registers.
        """
        if littleEndian:
            endianess = 'little'
        else:
            endianess = 'big'
        digest = (self.h1.to_bytes(4, 'little') +
                  self.h2.to_bytes(4, 'little') +
                  self.h3.to_bytes(4, 'little') +
                  self.h4.to_bytes(4, 'little'))
        return digest.hex()

    def __repr__(self):
        return f'MD4(h1={self.h1:#x}, h2={self.h2:#x}, h3={self.h3:#x}, h4={self.h4:#x}, add_const0={self.add_const0:#x}, add_const1={self.add_const1:#x}, add_const2={self.add_const2:#x})'




# if __name__ == "__main__":
#     msg = "a"
#     md5 = MD5(msg)
#     while not md5.run_iter():
#         pass
#     print("MD5 digest:", md5.digest())

# MD4_hash = MD5('a')
# print(MD4_hash.run_all())
