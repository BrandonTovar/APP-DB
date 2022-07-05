import base64

from itsdangerous import base64_decode, base64_encode

alphabet = {"A":"0001",
    "a":"1001",
    "B":"0011",
    "b":"1011",
    "C":"0003",
    "c":"1003",
    "D":"0023",
    "d":"1023",
    "E":"0021",
    "e":"1021",
    "F":"0023",
    "f":"1023",
    "G":"0033",
    "g":"1033",
    "H":"0031",
    "h":"1031",
    "I":"0012",
    "i":"1012",
    "J":"0021",
    "j":"1021",
    "K":"0102",
    "k":"1102",
    "L":"0111",
    "l":"1111",
    "M":"0103",
    "m":"1103",
    "N":"0123",
    "n":"1123",
    "O":"0121",
    "o":"1121",
    "P":"0113",
    "p":"1113",
    "Q":"0133",
    "q":"1133",
    "R":"0131",
    "r":"1131",
    "S":"0112",
    "s":"1112",
    "T":"0132",
    "t":"1132",
    "U":"0301",
    "u":"1301",
    "V":"0311",
    "v":"1311",
    "W":"0232",
    "w":"1232",
    "X":"0303",
    "x":"1303",
    "Y":"0323",
    "y":"1323",
    "Z":"0321",
    "z":"1321"}

# Numeros

numbers = {
    "0":"2032",
    "1":"2001",
    "2":"2011",
    "3":"2003",
    "4":"2023",
    "5":"2021",
    "6":"2013",
    "7":"2033",
    "8":"2031",
    "9":"2012"
}



#Simbolos

simbols = {
    " ":"3000",
    ".":"3001",
    ",":"3002",
    ";":"3003",
    ":":"3004",
    "!":"3005",
    "?":"3006",
    "¿":"3007",
    "¡":"3008",
    "\"":"3009",
    "'":"3010",
    "(":"3011",
    ")":"3012",
    "[":"3013",
    "]":"3014",
    "{":"3015",
    "}":"3016",
    "*":"3017",
    "+":"3018",
    "-":"3019",
    "/":"3020",
    "\\":"3021",
    "|":"3022",
    "=":"3023",
    "&":"3024",
    "%":"3025",
    "$":"3026",
    "#":"3027",
    "@":"3028",
    "^":"3029",
    "~":"3030",
    "`":"3031",
    "¬":"3032",
    "¦":"3033",
    "¨":"3034",
    "ª":"3035",
    "º":"3036",
    "µ":"3037",
    "·":"3038",
    "¹":"3039",
    "²":"3040",
    "³":"3041",
    "¼":"3042",
    "½":"3043",
    "¾":"3044",
    "÷":"3045",
    "x":"3046",
    "Ø":"3047",
    "Å":"3048",
    "Æ":"3049",
    "Ä":"3050",
    "Ö":"3051",
    "Ñ":"3052",
    "Ü":"3053",
    "Ú":"3054",
    "Ù":"3055",
    "Û":"3056",
    "Þ":"3057",
    "ß":"3058",
    "æ":"3059",
    "ä":"3060",
    "ö":"3061",
    "ñ":"3062",
    "ü":"3063",
    "ú":"3064",
    "ù":"3065",
    "û":"3066",
    "þ":"3067",
    "¥":"3068",
    "¤":"3069"}


# Funciones 
def get_Number(v):
    return list(numbers.keys())[list(numbers.values()).index(v)]
def get_Simbol(v):
    return list(simbols.keys())[list(simbols.values()).index(v)]
def get_Alphabet(v):
    return list(alphabet.keys())[list(alphabet.values()).index(v)]

def split_4b(c):
    cadena = []
    # Bucle que convertira la cadena en una lista de 4 bits
    for i in range(0, len(c), 4):
        cadena.append(c[i:i+4])
    return cadena


def decode_ble(cadena):
    if type(cadena) == str:
        cadena = cadena.replace("b'","").replace("'","")
    cadena = base64_decode(cadena)
    cadena = cadena.decode("ascii")
    desofuscado = ""
    cadena = split_4b(cadena)
    for i in cadena:
        try:
            desofuscado += get_Number(i)
        except:
            try:
                desofuscado += get_Simbol(i)
            except:
                try:
                    desofuscado += get_Alphabet(i)
                except:
                    desofuscado += " "
    return desofuscado



def encode_ble(cadena):
    ofuscado = ""
    for i in cadena:
        if numbers.get(i) != None:
            ofuscado += numbers.get(i)
        elif simbols.get(i) != None:
            ofuscado += simbols.get(i)
        elif alphabet.get(i) != None:
            ofuscado += alphabet.get(i)

    ofuscado = ofuscado.encode("ascii")
    ofuscado = base64_encode(ofuscado)
    return ofuscado

