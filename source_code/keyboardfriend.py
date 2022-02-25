import keyboard
from bs4 import BeautifulSoup
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from farbprinter.farbprinter import Farbprinter
from unidecode import unidecode
from einfuehrung import einfuehrung

def datei_auswaehlen_mit_tkinter():
    Tk().withdraw()
    file = askopenfilename(filetypes=[("TXT/CSV File", "txt csv")])
    return txtdateien_lesen(file)


def txtdateien_lesen(file):
    with open(file, mode='rb') as f:
        text = f.read()
    try:
        dateiohnehtml = (
            b"""<!DOCTYPE html><html><body><p>""" + text + b"""</p></body></html>"""
        )
        soup = BeautifulSoup(dateiohnehtml, "html.parser")
        soup = soup.text
        return soup.strip()
    except Exception as Fehler:
        print(Fehler)

if __name__ == '__main__':
    einfuehrung('Keyboardfriend')
    drucker = Farbprinter()
    datei = datei_auswaehlen_mit_tkinter()
    datei = list(dict.fromkeys(datei.splitlines()))
    datei = [tuple(x.strip().split(',',maxsplit=1)) for x in datei]
    datei = [(unidecode(x[0].strip()), x[1].strip()) for x in datei]
    dateidict = {k:v for k,v in datei}
    datei = [k for k in dateidict.items()]
    prefix = ''
    while prefix == '':
        try:
            prefix = input(
                drucker.f.black.brightyellow.normal(
                    f'''\nWhat prefix should be used?\n\n\nExample:\n\nIf you entered @, you would have to write \n\n\n"@{datei[0][0]}"\n\nto get\n\n"{datei[0][1]}"\n'''
                )
            )
            prefix = str(prefix).lower().strip()
        except Exception as Fehler:
            print(Fehler)
    for ini, d in enumerate(datei):
        try:
            exec(f'''keyboard.add_abbreviation(\'\'\'{prefix}{d[0]}\'\'\', \'\'\'{d[1]}\'\'\')''')
            print(f'{str(ini).zfill(6)}. Added: {prefix}{d[0]} -> {d[1]}')

        except Exception as Fehler:
            print(drucker.f.brightred.black.normal(Fehler))
    userinput = ''
    while userinput != 'end':
        try:
            userinput = input(
                drucker.f.black.brightyellow.normal(
                    "\nWrite 'end' to end the app\n"
                )
            )
            userinput = str(userinput).lower().strip().strip('''"\'''')
        except Exception as Fehler:
            print(Fehler)