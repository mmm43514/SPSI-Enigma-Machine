
from components import Rotor, Reflector, Plugboard
from utils_data import ENIGMA_ALPHABET, ch_ind, ind_ch, ROTORS, REFLECTORS

class EnigmaMachine:
    def __init__(self, pb_settings: str, sorted_rotors: str, ringstellung: str,\
     reflector: str):
        """
        Inicialización.
        Params:
            pb_settings: parejas de letras conectadas en Plugboard
            sorted_rotors: nombres de los rotores a usar vistos de izqda a dcha
             en la máquina
            ringstellung: letras en primer contacto de cada rotor tras
             deslizamientos por ringstellung
            reflector: nombre del reflector a usar
        """
        rotors_t = tuple(sorted_rotors) # tupla con los rotores a usar

        # Se crea tupla con los rotores
        rotors = tuple( Rotor(r_data.outputs, rr[1], r_data.notches) for rr in \
        zip(rotors_t, ringstellung) if (r_data := ROTORS[rr[0]]) )

        self.plugboard = Plugboard(pb_settings)
        self.rotors = rotors
        self.reflector = Reflector(REFLECTORS[reflector].outputs)

    def _rotate_rotors(self):
        """
        Rota los rotores que correspondan
        """
        # Rotores candidatos a rotar (todos menos el cuarto rotor)
        cand_rotors = self.rotors[-3:]
        # Crearemos tupla booleana para rotores que rotarán, el primero siempre
        # rota. Para los otros dos comprobamos si notch es enganchado
        # - primer rotor rota siempre (no tiene rotor a dcha)
        # - segundo rotor rota si el segundo pawl engancha notch de primer rotor
        #   o si tercer pawl engancha notch de segundo rotor
        # - tercer rotor rota si tercer pawl engancha notch de segundo rotor
        to_rotate2 = cand_rotors[-2].pawl_drops_into_notch()
        rotates = \
        (to_rotate2, cand_rotors[-1].pawl_drops_into_notch() or to_rotate2, 1)
        # Rotamos los rotores que corresponden rotar
        for i, r in enumerate(cand_rotors):
            if rotates[i]:
                r.rotate()

    def _transmission(self, c: int) -> int:
        """
        Efectúa la transmisión del índice de letra c a través de la máquina
        """
        # Intercambiamos por plugboard
        contact = self.plugboard.swap(c)
        # Transmitimos por los contactos de rotores de "derecha a izquierda"
        for r in self.rotors[::-1]:
            contact = r.transmit(contact, True)
        # Transmitimos a reflector
        contact = self.reflector.transmit(contact)
        # Transmitimos de vuelta por los rotores
        for r in self.rotors:
            contact = r.transmit(contact, False)
        # Devolvemos el intercambio por plugboard
        return self.plugboard.swap(contact)

    def grundstellung(self, win_pos_list: str):
        """
        Se colocan rotores en las posiciones que dejan los caracteres de
        win_pos_list visibles en ventanilla
        """
        for rotor, pos in zip(self.rotors, win_pos_list):
            rotor.set_window_position(ch_ind[pos])

    def encipher_chr(self, chr: str) -> str:
        """
        Cifra una letra pulsada
        """
        # Se rotan los rotores que correspondan
        self._rotate_rotors()
        # Se devuelve caracter cifrado
        return ind_ch[self._transmission(ch_ind[chr])]

    def encipher_text(self, text: str) -> str:
        """
        Cifra un texto letra a letra
        """
        enciphered_text = ''
        # Se cifra el texto letra a letra
        for c in text:
            enciphered_text += self.encipher_chr(c)
        # Se devuelve el texto cifrado
        return enciphered_text
