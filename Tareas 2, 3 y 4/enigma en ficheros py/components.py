
from utils_data import ch_ind

class Rotor:
    def __init__(self, outputs: str, ringst_chr: str, notches: str):
        """
        Inicialización.
        Params:
            outputs: string con la salidas que efectúa el rotor a cada letra
             del alfabeto dispuestas en orden
            ringst_char: letra que queda en primer contacto del rotor por el
             deslizamiento por ringstellung
            notches: string con letras visibles en ventanilla cuando una muesca
             está sobre pawl ("el trinquete")
        """
        ringst_offset = ch_ind[ringst_chr] # a índice numérico
        # tupla con los índices numéricos de las salidas de las conexiones
        self.connections = tuple(ch_ind[c] for c in outputs)
        # tupla inversa de connections para la transmisión después de reflector
        inv_connects_l = [None] * 26
        for i, c in enumerate(self.connections):
            inv_connects_l[c] = i
        self.inv_connections = tuple(inv_connects_l)

        # posiciones del rotor en las que un "trinquete" enganchará notch
        # (posiciones "deshaciendo ringstellung")
        self.p_notches_pos = None if notches is None else \
        tuple(ch_ind[n] - ringst_offset for n in notches)

        self.ringstellung = ringst_offset
        self.pos = 0 # posición inicial

    def set_window_position(self, pos: int):
        """
        Coloca el rotor en posición que deje al índice de letra pos
        visible en la ventanilla
        """
        # colocamos rotor en posición real, "deshaciendo ringstellung"
        self.pos = (pos - self.ringstellung) % 26

    def transmit(self, contact: int, before_reflector: bool) -> int:
        """
        Transmite señal a través del rotor
        """
        # contacto receptor de la señal en su posición de rotación
        r_contact = (contact + self.pos) % 26
        # contacto transmitido, relativo a la rotación del rotor
        t_contact_rel = self.connections[r_contact] if before_reflector \
        else self.inv_connections[r_contact]

        # contacto transmitido en posición absoluta
        t_contact_abs = (t_contact_rel - self.pos) % 26

        return t_contact_abs

    def rotate(self):
        """
        Rota el rotor
        """
        self.pos = (self.pos + 1) % 26 # rota actualizando posición

    def pawl_drops_into_notch(self) -> bool:
        """
        Comprobueba si el notch (muesca) está sobre los "trinquetes" (pawls) y
        por tanto será enganchado al pulsar tecla
        """
        # devuelve si notch será enganchado al pulsar tecla
        return self.pos in self.p_notches_pos


class Reflector:
    def __init__(self, outputs: str):
        """
        Inicialización.
        Params:
            outputs: string con la salidas que efectúa el reflector a cada letra
             del alfabeto dispuestas en orden
        """
        # conexiones, tupla con los contactos de salida
        self.connections = tuple(ch_ind[c] for c in outputs)

    def transmit(self, contact: int) -> int:
        """
        Transmite señal a través del reflector
        """
        # devolvemos contacto al que transmite
        return self.connections[contact]


class Plugboard:
    def __init__(self, swaps: str):
        """
        Inicialización.
        Params:
            swaps: string con parejas de letras conectadas en Plugboard
        """
        # diccionario que realiza los intercambios correspondientes por las
        # conexiones dadas en swaps
        cable_swaps = {ch_ind[p[i]]: ch_ind[p[(i+1)%2]] for p in swaps.split() for i in range(2)}
        # tupla con las salidas tras el plugboard, salidas por intercambio por
        # cable conectado y salidas que quedan igual por no haber cable (más
        # eficiente que comprobar si hay intercambio en cable_swaps)
        self.swaps = tuple(cable_swaps[i] if i in cable_swaps else i for i in range(26))

    def swap(self, c: int) -> int:
        """
        Da la salida determinada por la configuración del plugboard
        """
        # devuelve salida correspondiente
        return self.swaps[c]
