
ENIGMA_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # alfabeto
# diccionario, letra del alfabeto -> índice numérico del alfabeto
ch_ind = {ENIGMA_ALPHABET[i]: i for i in range(26)}
# tupla, índice numérico del alfabeto -> letra del alfabeto
ind_ch = tuple(ENIGMA_ALPHABET[i] for i in range(26))

# notches indicará las letras que se ven en la ventana antes de que al pulsar
# tecla pawl engache un notch, notches se usará en caso de los rotores
class CompData:
    def __init__(self, outputs, notches = None):
        self.outputs = outputs
        self.notches = notches

# Datos de rotores
ROTORS = {
    # 5 rotores extendidos en 1939, con un único notch
    '1': CompData('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
    '2': CompData('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
    '3': CompData('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
    '4': CompData('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
    '5': CompData('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
    # 3 rotores adicionales añadidos por Kriegsmarine, tienen dos notches
    '6': CompData('JPGVOUMFYQBENHZRDKASXLICTW', 'ZM'),
    '7': CompData('NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM'),
    '8': CompData('FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM'),
    # Cuarto rotor (1942), usados exclusivamente por M4 con reflectores delgados
    'b': CompData('LEYJVCNIXWPBQMDRTAKZGFUHOS', None),
    'g': CompData('FSOKANUERHMBTIYCWLQPZXVGJD', None)
}

# Datos de reflectores
REFLECTORS = {
    # Reflectores iniciales Enigma I
    'B': CompData('YRUHQSLDPXNGOKMIEBFZCWVJAT'),
    'C': CompData('FVPJIAOYEDRZXWGCTKUQSBNMHL'),
    # Reflectores añadidos por Kriegsmarine que permiten espacio para
    # el cuarto rotor:
    'B Thin': CompData('ENKQAUYWJICOPBLMDXZVFTHRGS'),
    'C Thin': CompData('RDOBJNTKVEHMLFCWZAXGYIPSUQ')
}
