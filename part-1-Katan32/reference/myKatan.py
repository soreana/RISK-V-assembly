from time import time
IR = (
    1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1,
    0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0,
    1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0,
    0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
    0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1,
    1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1,
    0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0,
    1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1,
    0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1,
    1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
    1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1,
    0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1,
    1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0,
    0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1,
    0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1,
    1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
    )



def num2bits(num, bitlength):
    bits = []
    for i in range(bitlength):
        bits.append(num & 1)
        num >>= 1
    return bits

def bits2num(bits):
    num = 0
    for i, x in enumerate(bits):
        assert x == 0 or x == 1
        num += (x << i)
    return num


class KATAN():
    def __init__(self,  version,master_key = 0):
        assert version in (32, 48, 64)
        self.version = version

        if 32 == self.version:
            self.LEN_L1 = 13
            self.LEN_L2 = 19
            self.X = (None, 12, 7, 8, 5, 3) # starting from 1
            self.Y = (None, 18, 7, 12, 10, 8, 3)
        elif 48 == self.version:
            self.LEN_L1 = 19
            self.LEN_L2 = 29
            self.X = (None, 18, 12, 15, 7, 6)
            self.Y = (None, 28, 19, 21, 13, 15, 6)
        else:
            self.LEN_L1 = 25
            self.LEN_L2 = 39
            self.X = (None, 24, 15, 20, 11, 9)
            self.Y = (None, 38, 25, 33, 21, 14, 9)

        self.key = num2bits(master_key, 80)

        for i in range(80, 2*254):
            self.key.append(self.key[i-80] ^ self.key[i-60] ^ self.key[i-50] ^ self.key[i-13])

    def only_one_round_enc(self, plaintext, IR, ka, kb):
        self.plaintext_bits = num2bits(plaintext, self.version)
        self.L2 = self.plaintext_bits[:self.LEN_L2]
        self.L1 = self.plaintext_bits[self.LEN_L2:]

        self.f_a = self.L1[self.X[1]] ^ self.L1[self.X[2]]\
                   ^ (self.L1[self.X[3]] & self.L1[self.X[4]])\
                   ^ (self.L1[self.X[5]] & IR) ^ ka

        self.f_b = self.L2[self.Y[1]] ^ self.L2[self.Y[2]]\
                   ^ (self.L2[self.Y[3]] & self.L2[self.Y[4]])\
                   ^ (self.L2[self.Y[5]] & self.L2[self.Y[6]]) ^ kb

        self.L1.pop()
        self.L1.insert(0, self.f_b)

        self.L2.pop()
        self.L2.insert(0, self.f_a)

    def one_round_enc(self, round):
        self.f_a = self.L1[self.X[1]] ^ self.L1[self.X[2]]\
                   ^ (self.L1[self.X[3]] & self.L1[self.X[4]])\
                   ^ (self.L1[self.X[5]] & IR[round])\
        ^ self.key[2*round]

        self.f_b = self.L2[self.Y[1]] ^ self.L2[self.Y[2]]\
                   ^ (self.L2[self.Y[3]] & self.L2[self.Y[4]])\
                   ^ (self.L2[self.Y[5]] & self.L2[self.Y[6]])\
        ^ self.key[2*round+1]

        self.L1.pop()
        self.L1.insert(0, self.f_b)

        self.L2.pop()
        self.L2.insert(0, self.f_a)


    def enc(self, plaintext, from_round = 0, to_round = 253):
        self.plaintext_bits = num2bits(plaintext, self.version)
        self.L2 = self.plaintext_bits[:self.LEN_L2]
        self.L1 = self.plaintext_bits[self.LEN_L2:]

        for round in range(from_round, to_round + 1):
            self.one_round_enc(round)
            if self.version > 32:
                self.one_round_enc(round)
                if self.version > 48:
                    self.one_round_enc(round)
        return bits2num(self.L2 + self.L1)


    def one_round_dec(self, round):
        self.f_a = self.L2[0] ^ self.L1[self.X[2] + 1]\
                   ^ (self.L1[self.X[3] + 1] & self.L1[self.X[4] + 1])\
                   ^ (self.L1[self.X[5] + 1] & IR[round])\
        ^ self.key[2*round]

        self.f_b = self.L1[0] ^ self.L2[self.Y[2] + 1]\
                   ^ (self.L2[self.Y[3] + 1] & self.L2[self.Y[4] + 1])\
                   ^ (self.L2[self.Y[5] + 1] & self.L2[self.Y[6] + 1])\
        ^ self.key[2*round+1]

        self.L1.pop(0)
        self.L1.append(self.f_a)

        self.L2.pop(0)
        self.L2.append(self.f_b)


    def dec(self, ciphertext, from_round = 253, to_round = 0):
        self.ciphertext_bits = num2bits(ciphertext, self.version)
        self.L2 = self.ciphertext_bits[:self.LEN_L2]
        self.L1 = self.ciphertext_bits[self.LEN_L2:]

        for round in range(from_round, to_round - 1, -1):
            self.one_round_dec(round)
            if self.version > 32:
                self.one_round_dec(round)
                if self.version > 48:
                    self.one_round_dec(round)
        return bits2num(self.L2 + self.L1)

def bits_to_hex(bits, total_bits):

    bits_reversed = bits[::-1]

    bit_str = ''.join(str(b) for b in bits_reversed)
    value = int(bit_str, 2)

    hex_digits = (total_bits + 3) // 4

    hex_value = f'0x{value:0{hex_digits}x}'

    return hex_value

if __name__ == '__main__':
    key = 0x2b7e151628aed2a6abf7158809cf4f3c # This key doesn't have any effect
    ver=32
    myKATAN = KATAN(ver,key)

    print('Enter the data (hex number)')
    data = int(input(), 16)

    print('DATA BEFORE ENCRYPTION')
    print('plain =',data)
    myKATAN.only_one_round_enc(data, 1, 0, 1)
    print('L1 after one round = ', myKATAN.L1, ' in hex= ', bits_to_hex(myKATAN.L1, 13))
    print('L2 after one round = ', myKATAN.L2, ' in hex= ', bits_to_hex(myKATAN.L2, 19))
