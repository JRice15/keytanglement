from bitarray import bitarray

def string_to_bits(message):
    b = bitarray()
    b.frombytes(message.encode("ASCII"))
    return b

def encrypt(message, key):
    return message ^ key[:len(message)]

def decrypt(message, key):
    return message ^ key[:len(message)]

def bits_to_string(bits):
    return bits.tobytes().decode("ASCII")
