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


class MD4:
    def __init__(self, message: str = None,  h1: str = '67452301', h2: str = 'efcdab89', 
                 add_const0: str = '00000000', add_const1: str = '5a827999', add_const2: str = '6ed9eba1',
                 order_list0: list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                 order_list1: list[int] = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15],
                 order_list2: list[int] = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15],
                 shift_list0: list[int] = [3, 7, 11, 19],
                 shift_list1: list[int] = [3, 5, 9, 13],
                 shift_list2: list[int] = [3, 9, 11, 15]):

        # Initialize chain constraints
        h3, h4 = chain_constraints(h1, h2)

        self.h1 = int(h1, 16)
        self.h2 = int(h2, 16)
        self.h3 = int(h3, 16)
        self.h4 = int(h4, 16)

        # Registers
        self.a = self.h1
        self.b = self.h2
        self.c = self.h3
        self.d = self.h4

        # Initialize addititive constants
        self.add_const0 = int(add_const0, 16)
        self.add_const1 = int(add_const1, 16)
        self.add_const2 = int(add_const2, 16)

        # Initialize order lists
        self.order_list0 = order_list0
        self.order_list1 = order_list1
        self.order_list2 = order_list2

        # Initialize shift lists
        self.shift_list0 = shift_list0 * 4
        self.shift_list1 = shift_list1 * 4
        self.shift_list2 = shift_list2 * 4

        # Initialize algorithm parameters and counters
        self.finished = False # flag to check if the algorithm has finished processing
        if message is None:
            self.message = None
            self.number_of_blocks = 0
        else:
            self.message, self.number_of_blocks = self.__preprocess(message)

        self.block_counter: int = 0 # block counter
        self.word_counter: int = 0 # word counter
        self.cycle_counter: int = 0 # cycle counter


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
    

    def run_iter(self):
        """
        Run the MD4 algorithm on the given message.
        :param message: The input message to hash.
        """
        block = self.message[(self.block_counter * 64):(self.block_counter * 64 + 64)] # Get the current block (64 bytes == 16 words)

        if self.cycle_counter == 0: # First round
            x = block[(self.order_list0[self.word_counter] * 4):(self.order_list0[self.word_counter] * 4 + 4)] # Get the current word (4 bytes == 1 word)
            x = int.from_bytes(x, byteorder='little') # Convert to integer
            temp = (self.a + ((self.b & self.c) | (~self.b & self.d)) + x + self.add_const0) & 0xFFFFFFFF
            (self.a, self.b, self.c, self.d) = (self.d, 
                                            (temp << (self.shift_list0[self.word_counter]) | (temp >> (32 - self.shift_list0[self.word_counter]))) & 0xFFFFFFFF,  # Rotate left
                                            self.b, self.c)
        elif self.cycle_counter == 1: # Second round
            x = block[(self.order_list1[self.word_counter] * 4):(self.order_list1[self.word_counter] * 4 + 4)] # Get the current word (4 bytes == 1 word)
            x = int.from_bytes(x, byteorder='little') # Convert to integer
            temp = (self.a + ((self.b & self.c) | (self.b & self.d) | (self.c & self.d)) + x + self.add_const1) & 0xFFFFFFFF
            (self.a, self.b, self.c, self.d) = (self.d, 
                                            (temp << (self.shift_list1[self.word_counter]) | (temp >> (32 - self.shift_list1[self.word_counter]))) & 0xFFFFFFFF,  # Rotate left
                                            self.b, self.c)
        elif self.cycle_counter == 2: # Third round
            x = block[(self.order_list2[self.word_counter] * 4):(self.order_list2[self.word_counter] * 4 + 4)] # Get the current word (4 bytes == 1 word)
            x = int.from_bytes(x, byteorder='little') # Convert to integer
            temp = (self.a + (self.b ^ self.c ^ self.d) + x + self.add_const2) & 0xFFFFFFFF
            (self.a, self.b, self.c, self.d) = (self.d, 
                                            (temp << (self.shift_list2[self.word_counter]) | (temp >> (32 - self.shift_list2[self.word_counter]))) & 0xFFFFFFFF,  # Rotate left
                                            self.b, self.c)

        # Increment
        if self.word_counter == 15:
            self.word_counter = 0
            if self.cycle_counter == 2:
                self.cycle_counter = 0
                self.block_counter += 1
                # Update chain constraints
                self.h1 = (self.h1 + self.a) & 0xFFFFFFFF
                self.h2 = (self.h2 + self.b) & 0xFFFFFFFF
                self.h3 = (self.h3 + self.c) & 0xFFFFFFFF
                self.h4 = (self.h4 + self.d) & 0xFFFFFFFF
                # Check if all blocks have been processed
                if self.block_counter == self.number_of_blocks:
                    self.finished = True
                else:
                    # Update the a, b, c, d registers
                    self.a = self.h1
                    self.b = self.h2
                    self.c = self.h3
                    self.d = self.h4
            else:
                self.cycle_counter += 1
        else:
            self.word_counter += 1

        return self.finished


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


    
# MD4_hash = MD4('a4567')
# # MD4_hash.run_all()
# print(MD4_hash.run_all(True))  # Example usage of the MD4 class

# import hashlib
# print(hashlib.new('md4', 'a'.encode()).hexdigest())  # Example usage of the hashlib library for MD4
