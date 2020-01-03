"""
miinaharava - ohjelmoinnin alkeet -kurssin lopputyö 

@author: Reeta Siira

Miinaharava on toteutettu käyttäen haravastoa, opettajan luomaa graafista käyttöliitymää, 
joka toimii pygletin päällä. Muutamia pelin funktioita on myös toteutettu käyttäen suoraan 
pygletin funktioita.
"""

import random
import math
import time
import pyglet
import haravasto

PER_SIVU = 5        # Tilastojen tulostuksessa tulosten lukumäärä per sivu
MAX_TULOSTUKSET = 2 # Tulostusten lukumäärä

# Kaikki pelissä tarvittavat muuttujat tallennetaan tähän sanakirjaan, 
# jotta niitä voidaan helposti käsitellä kaikissa funktioissa.

tila = {
    "pelaajan_nimi": "",
    "peli_kentta": [],
    "pelaajan_kentta": [],
    "leveys": 0, 
    "korkeus": 0,
    "hiiren_klikkaukset": {
        "x_indeksi": 0,
        "y_indeksi": 0,
        "nappi": 0
        },
    "miinojen_lkm": 0,
    "miinoja_jäljellä": 0,
    "taso": 0,
    "tulos": "",
    "päivämäärä": "",
    "aika": {
        "reaali_aika": 0,
        "aloitus_aika": 0,
        "lopetus_aika": 0,
        "kesto": 0
        },
    "tulostus_ikkuna": None, 
    "tulostus_ikkuna_tausta": None
}

#Tilastojen tallentamiseen ja tulostukseen liittyvät funktiot:
def tallenna_pelitiedot(tiedosto):
    """
    Tallentaa pelin tiedot: pelaaja, tulos, kesto, taso ja päivämäärä.
    Tallentaminen tapahtuu lisäämällä pelin tiedot jo olemassa olevaan tideostoon.
    Mikäli tiedostoa ei ole olemassa, se luodaan sillä hetkellä kun funktiota
    kutsutaan.
    :param str tiedosto: tiedoston nimi, johon pelin tiedot lisätään
    """
    try:
        with open(tiedosto, "a") as kohde:
                kohde.write("{pelaaja}, {tulos}, {kesto}, {taso}, {päivämäärä}\n".format(
                    pelaaja=tila["pelaajan_nimi"],
                    tulos=tila["tulos"],
                    kesto=tila["aika"]["kesto"],
                    taso=tila["taso"],
                    päivämäärä=tila["päivämäärä"]
                ))
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tallennus epäonnistui")
  
def lataa_tilastot(tiedosto):
    """
    Lataa tilastot tiedostosta ohjelman sisään listaksi, joka sisältää sanakirjoja. 
    :param str tiedosto: tiedoston nimi, johon pelin tiedot on tallennettu
    """
    tulokset = []    
    try:
        with open(tiedosto) as lahde:
            for rivi in lahde.readlines():
                lue_rivi(rivi, tulokset)
    except IOError:
        print("Tilastoissa ei ole vielä tuloksia")
    
    return tulokset
    
def lue_rivi(rivi, tulokset):
    """
    Lukee yhden rivin tiedot sanakirjaksi, sekä poistaa ylimääräiset välilyönnit
    muuttujista.
    
    :param str rivi: ladattavan tiedoston yksi rivi
    :param list tulokset: lista, johon rivejä lisätään sanakirjan muodossa
    """
    # Rivillä oleva järjestys vastaa seuraavia sanakirjan avaimia:
    # 1. "pelaaja" - pelaajan nimi
    # 2. "tulos" - pelitulos 
    # 3. "kesto" - pelin kesto
    # 4. "taso" - pelin taso(miinojen lukumäärä)
    # 5. "päivämäärä" - päivämäärä
    try:
        pelaaja, tulos, kesto, taso, päivämäärä = rivi.split(",")
        pelin_tiedot = {
            "pelaaja": pelaaja.strip(),
            "tulos": tulos.strip(),
            "kesto": kesto.strip(),
            "taso": taso.strip(),
            "päivämäärä": päivämäärä.strip()
        }
        tulokset.append(pelin_tiedot)
    except ValueError:
        print("Riviä ei saatu luettua: {}".format(rivi))
        
def muotoile_sivu(rivit, sivu):
    """
    Muotoilee tulostettavan sivun.
    
    :param list rivit: lista muotoiltavista riveistä
    :param int sivu: tulostettavan sivun numero, tulosta_tilastot funktion i
    """
    for i, rivi in enumerate(rivit, sivu * PER_SIVU + 1): #enumeraten toinen argumentti kertoo mistä numerosta numerointi alkaa
        print("{i}. {pelaaja}, Taso: {taso}, Kesto: {kesto}, {päivämäärä}\n".format(
            i=i,
            pelaaja=rivi["pelaaja"],
            #tulos=rivi["tulos"], #jätetään pois koska vain voitot tallennetaan
            kesto=rivi["kesto"],
            taso=rivi["taso"],
            päivämäärä=rivi["päivämäärä"]
        ))
    
def palauta_kesto(rivi):
    return rivi["kesto"]
        
def tulosta_tilastot(tulokset):
    """
    Tallentaa tarvittavien tulostusten määrän tulostusten_maara-muuttujaan.
    Tulostaa tuloksia sivu kerrallaan. Seuraava sivu tulostuu painamalla enteriä.
    
    :param list tulokset: lista, joka sisältää tuloksia sanakirjan muodossa
    """
    tulostusten_maara = math.ceil(len(tulokset) / PER_SIVU) 
    for i in range(min(tulostusten_maara, MAX_TULOSTUKSET)):
        alku = i * PER_SIVU                                     # esim. i = 0 ja PER_SIVU = 5, 0 * 5 = 0
        loppu = (i + 1) * PER_SIVU                              # (0 + 1) * 5 = 5
        muotoile_sivu(tulokset[alku:loppu], i)                  # tulokset[0:5]
        if i < min(tulostusten_maara - 1, MAX_TULOSTUKSET - 1): #toteutuu jos tulostuksia on jäljellä
            input("   -- paina enter jatkaaksesi tulostusta --")

# Käsitteljäfunktiot:
def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for y, rivi in enumerate(tila["pelaajan_kentta"]):
        for x, avain in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(avain, x * 40, y *40)
    haravasto.piirra_ruudut()
    taso = ("Taso {}".format(tila["taso"]))
    miinat = ("Miinat: {}".format(tila["miinoja_jäljellä"]))
    aika = ("Aika: {}".format(tila["aika"]["reaali_aika"]))

    haravasto.piirra_tekstia(taso, 0, 40 * tila["korkeus"], vari=(0, 0, 0, 255), fontti="serif", koko=15)
    haravasto.piirra_tekstia(miinat, 100, 40 * tila["korkeus"], vari=(0, 0, 0, 255), fontti="serif", koko=15)
    haravasto.piirra_tekstia(aika, 220, 40 * tila["korkeus"], vari=(0, 0, 0, 255), fontti="serif", koko=15)
    
def piirra_ikkuna():
    """
    Käsittelijäfunktio, joka piirtää tulos-ikkunan.
    Funktiota kutsutaan kun peli päättyy.
    """
    if tila["tulos"] == "voitto":
        tulos = "Voitit pelin!"   
    elif tila["tulos"] == "häviö":
        tulos = "Hävisit pelin."
    taso = ("Taso: {}".format(tila["taso"]))
    kesto = ("Pelin kesto: {}".format(tila["aika"]["kesto"]))
        
    tila["tulos_ikkuna"].clear()
    tila["tulos_ikkuna_tausta"].draw()
    haravasto.piirra_tekstia(tulos, 80, 110)
    haravasto.piirra_tekstia(taso, 80, 70, koko=15)
    haravasto.piirra_tekstia(kesto, 80, 40, koko=15)
    
def kasittele_hiiri(x, y, nappi, muokkausnappain):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Funktio tallentaa klikatun ruudun x- ja y-koordinaatin sekä klikkauksen 
    napin tila-sanakirjaan. Lisäksi kutsutaan avaa_ruutu-funktiota, jotta pelaajan kenttä
    päivittyy hiiren klikkauksen yhteydessä. Lisäksi tarkistetaan,
    voitetaanko peli kyseisellä klikkauksella. Jos näin on,
    tila-sanakirjaan tallennetaan tulokseksi "voitto". Tällöin myös
    pelin lopetus-aika, kesto ja päivämäärä tallennetaan. Toistuva käsittelijä irroitetaan. 
    Hiiren käsittelijäksi asetetaan kasittele_hiiri_lopussa, ja pelin tiedot tulostetaan erillisessä ikkunassa.
    """

    try: 
        y_indeksi, x_indeksi = maarita_ruutu(x, y)
    except TypeError:
        print("Klikkaus on ruudun ulkopuolella.")
    else:
        tila["hiiren_klikkaukset"]["x_indeksi"] = x_indeksi
        tila["hiiren_klikkaukset"]["y_indeksi"] = y_indeksi
        tila["hiiren_klikkaukset"]["nappi"] = nappi
 
        avaa_ruutu()
        if tarkista_voitto() == tila["miinojen_lkm"]:
            tila["tulos"] = "voitto"
            tila["aika"]["lopetus_aika"] = time.perf_counter()
            pyglet.clock.unschedule(paivitys_kasittelija)
            tallenna_peliaika()
            tallenna_paivamaara()
            haravasto.aseta_hiiri_kasittelija(kasittele_hiiri_lopussa)
            luo_tulos_ikkuna()
            
def kasittele_hiiri_lopussa(x, y, nappi, muokkausnappain):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä pelin lopussa.
    Sulkee peli_ikkunan klikkauksesta. Peli-ikkuna suljetaan vasta kun tulos_ikkuna on suljettu ensin.
    """
    if tila["tulos_ikkuna"] == None:
        haravasto.lopeta()
    else:
        print("Sulje ensin tulosikkuna.")
    
def kasittele_hiiri_tulos_ikkuna(x, y, nappi, muokkausnappain):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa tulosikkunaa hiirellä pelin lopussa.
    """
    tila["tulos_ikkuna"].close()
    tila["tulos_ikkuna"] = None

def paivitys_kasittelija(kulunut_aika):
    """
    Käsittelijäfunktio, jota kutsutaan periodisesti, ja joka päivittää
    pelin reaaliaikaa ts. kuluvaa aikaa.
    """
    tallenna_reaaliaika()

# Pelilogiikan funktiot:
def tarkista_voitto():
    """
    Tarkistaa montako tyhjää ruutua pelikentällä on, ja palauttaa tyhjien 
    ruutujen lukumäärän.
    """
    testi_lista = []
    for y, rivi in enumerate(tila["pelaajan_kentta"]):
        for x, merkki in enumerate(rivi):
            if tila["pelaajan_kentta"][y][x] == " " or tila["pelaajan_kentta"][y][x] == "f":
                testi_lista.append(1) 
    tyhjat_ruudut = testi_lista.count(1)           
    return tyhjat_ruudut
    
def luo_tulos_ikkuna(leveys=400, korkeus=200, taustavari=(240, 240, 240, 255)):
    tila["tulos_ikkuna"] = pyglet.window.Window(leveys, korkeus)
    tila["tulos_ikkuna_tausta"] = pyglet.sprite.Sprite(
        pyglet.image.SolidColorImagePattern(taustavari).create_image(leveys, korkeus)
    )
    tila["tulos_ikkuna"].on_draw = piirra_ikkuna
    tila["tulos_ikkuna"].on_mouse_press = kasittele_hiiri_tulos_ikkuna
    
def tallenna_paivamaara():
    tila["päivämäärä"] = time.asctime()
    
def tallenna_peliaika(): 
    kesto_sekuntteina = tila["aika"]["lopetus_aika"] - tila["aika"]["aloitus_aika"]
    tila["aika"]["kesto"] = time.strftime("%Mmin %Ss", time.gmtime(kesto_sekuntteina))
    
def tallenna_reaaliaika():
    """
    Tallentaa reaaliajan tilaan muodossa 00min 00s.
    """
    kesto_sekuntteina = time.perf_counter()
    tila["aika"]["reaali_aika"] = time.strftime("%Mmin %Ss", 
        time.gmtime(kesto_sekuntteina - tila["aika"]["aloitus_aika"]
    ))
    
def avaa_ruutu():
    """
    Avaa ruudun pelaajan kentällä riippuen pelikentän sisällöstä ja hiiren painikkesta.
    Jos pelikentällä on miina eli pelikentän merrki kyseisessä koordinaatissa on "x",
    tila-sanakirjaan tallennetaan tulokseksi "häviö". Tällöin myös
    pelin lopetus-aika, kesto ja päivämäärä tallennetaan. Toistuva käsittelijä irroitetaan. 
    Hiiren käsittelijäksi asetetaan kasittele_hiiri_lopussa, ja pelin tiedot tulostetaan erillisessä ikkunassa.
    """
    nappi = tila["hiiren_klikkaukset"]["nappi"]
    x = tila["hiiren_klikkaukset"]["x_indeksi"]
    y = tila["hiiren_klikkaukset"]["y_indeksi"]
    
    if nappi == haravasto.HIIRI_OIKEA and tila["pelaajan_kentta"][y][x] == " ":
        tila["pelaajan_kentta"][y][x] = "f" 
        tila["miinoja_jäljellä"] -= 1 
    elif nappi == haravasto.HIIRI_OIKEA and tila["pelaajan_kentta"][y][x] == "f":
        tila["pelaajan_kentta"][y][x] = " "
        tila["miinoja_jäljellä"] += 1
    elif nappi == haravasto.HIIRI_VASEN and tila["peli_kentta"][y][x] == " " and not tila["pelaajan_kentta"][y][x] == "f":
        tulvataytto(x, y)   
    elif nappi == haravasto.HIIRI_VASEN and tila["peli_kentta"][y][x] == "x" and not tila["pelaajan_kentta"][y][x] == "f":
        tila["pelaajan_kentta"][y][x] = tila["peli_kentta"][y][x]
        tila["tulos"] = "häviö" 
        tila["aika"]["lopetus_aika"] = time.perf_counter()
        pyglet.clock.unschedule(paivitys_kasittelija)
        tallenna_peliaika()
        tallenna_paivamaara()
        haravasto.aseta_hiiri_kasittelija(kasittele_hiiri_lopussa)
        luo_tulos_ikkuna()
    elif nappi == haravasto.HIIRI_VASEN and not tila["pelaajan_kentta"][y][x] == "f":
        tila["pelaajan_kentta"][y][x] = tila["peli_kentta"][y][x]

def maarita_ruutu(x, y):
    """
    Tarkistaa, että hiiren klikkaus on ruudun sisällä,
    ja palauttaa klikkausta vastaavan ruudun koordinaattiparin (listan indeksit).
    :param int x: klikkauksen x-koordinaatti
    :param int y: klikkauksen y-koordinaatti
    """
    x_indeksi, y_jakojaannos = divmod(x, 40)
    y_indeksi, x_jakojaannos = divmod(y, 40)
        
    if y_jakojaannos > 2 and y_jakojaannos < 38:
        if x_jakojaannos > 2 and x_jakojaannos < 38:
            return(y_indeksi, x_indeksi)

def tulvataytto(x_koordinaatti, y_koordinaatti): 
    """
    Merkitsee pelikentällä olevat tuntemattomat (" ") alueet turvalliseksi ("0") siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    :param int x-koordinaatti: ruudun x-koordinaatti
    :param int y-koordinaatti: ruudun y-koordinaatti
    """
    tutkittavat_koordinaatit = [(x_koordinaatti, y_koordinaatti)]
    
    while tutkittavat_koordinaatit:
        x, y = tutkittavat_koordinaatit.pop(-1)
        tila["pelaajan_kentta"][y][x] = tila["peli_kentta"][y][x]
        
        if tila["peli_kentta"][y][x] == " ":
            tila["peli_kentta"][y][x] = "0"
            for j, rivi in enumerate(tila["peli_kentta"][(max(0, (y - 1))):(y + 2)], start=(max(0, (y - 1)))):
                for i, merkki in enumerate((rivi[(max(0, (x - 1))):(x + 2)]), start=(max(0, (x - 1)))):
                    tutkittavat_koordinaatit.append((i, j))
                    
def aseta_numerot():
    """
    Asettaa pelikentällä numerot miinojen ympärille.
    """
    for y, rivi in enumerate(tila["peli_kentta"]):
        for x, merkki in enumerate(rivi):
            if tila["peli_kentta"][y][x] != "x" and laske_miinat(x, y) != 0:
                tila["peli_kentta"][y][x] = laske_miinat(x, y)
                
def laske_miinat(x, y):
    """
    Laskee annetun ruudun ympärillä olevat miinat ja palauttaa
    niiden lukumäärän. Funktio toimii sillä oletuksella, että valitussa ruudussa ei
    ole ninjaa - jos on, sekin lasketaan mukaan.
    
    :param int x: ruudun x-koordinaatti
    :param int y: ruudun y-koordinaatti
    """
    miinat = []
    
    for sarake in tila["peli_kentta"][(max(0, (y - 1))):(y + 2)]:
        for miina in sarake[(max(0, x - 1)):(x + 2)]:
            miinat.append(miina)
            
    return miinat.count("x")
                
def miinoita(kentta, vapaat_ruudut, n):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    
    :param list kentta: kaksiulotteisesta listasta muodostuva kenttä
    :param list vapaat_ruudut: lista vapaista ruuduista
    :param int n: miinojen lukumäärä
    """
    for luku in range(n):
        y, x = random.choice(vapaat_ruudut)
        vapaat_ruudut.remove((y, x))
        kentta[y][x] = "x"
        
def luo_kentta(leveys, korkeus):
    """
    Luo kaksiulotteisen kentän, joka muodostuu sisäkkäisistä listoista.
    
    :param int leveys: kentän leveys
    :param int korkeus: kentän korkeus
    """
    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")
            
    return kentta

def luo_vapaat_ruudut(leveys, korkeus):
    """
    Luo listan vapaista ruuduista tyhjällä kentällä, jonka leveys
    ja korkeus on annettu. Tallentaa ruudun x ja y koordinaatit monikkona.
    
    :param int leveys: kentän leveys
    :param int korkeus: kentän korkeus
    """
    jaljella = []
    for x in range(korkeus):
        for y in range(leveys):
            jaljella.append((x, y))
    return jaljella
        
def kysy_taso():
    """
    Kysyy käyttäjältä pelin tason. Palauttaa tason, tasolla olevien miinojen lukumäärän,
    sekä pelikentän leveyden ja korkeuden kyseisellä tasolla.
    """
    print("Pelitasolla 1 on 10 miinaa, pelitasolla 2 on 20 miinaa ja pelitasolla 3 on 50 miinaa.")
    while True: 
        taso = input("Pelin taso: ").strip()
        if taso == "1":
            n = 10
            taso = 1
            leveys = 10
            korkeus = 10
            return taso, n, leveys, korkeus
        elif taso == "2":
            n = 20
            taso = 2
            leveys = 13
            korkeus = 12
            return taso, n, leveys, korkeus
        elif taso == "3":
            n = 50
            taso = 3
            leveys = 20
            korkeus = 15
            return taso, n, leveys, korkeus            
        else:
            print("Valitsemaasi toimintoa ei ole olemassa")
            
def alusta_tila():
    """
    Alustaa tilan tyhjäksi eli luo uuden pelin.
    """
    tila["pelaajan_nimi"] = None
    tila["peli_kentta"] = None
    tila["pelaajan_kentta"] = None
    tila["hiiren_klikkaukset"]["x_indeksi"] = None
    tila["hiiren_klikkaukset"]["y_indeksi"] = None
    tila["hiiren_klikkaukset"]["nappi"] = None
    tila["miinojen_lkm"] = None
    tila["miinoja_jäljellä"] = None
    tila["taso"] = None
    tila["tulos"] = None
    tila["päivämäärä"] = None
    tila["aika"]["reaali_aika"] = 0
    tila["aika"]["aloitus_aika"] = 0
    tila["aika"]["lopetus_aika"] = None
    tila["aika"]["kesto"] = None
    tila["tulos_ikkuna"] = None 
    tila["tulos_ikkuna_tausta"] = None

def aloita_uusi_peli():
    """
    Alustaa tila-sanakirjan tyhjäksi.
    Tallentaa pelaajan valitseman tason, tasoa vastaavan miinojen lukumäärän
    sekä pelikentän leveyden ja korkeuden tila-sanakirjaan.     
    Luo erikseen tyhjän pelikentän ja tyhjän pelaajankentän, jotka tallenetaan 
    tila-sanakirjaan. Luo listan vapaista ruuduista, miinoittaa pelikentän ja 
    asettaa numerot miinojen ympärille pelikentällä.
    Lataa ohjelman käyttämät kuvat, luo peli_ikkunan, asettaa piirtokäsittelijän
    ja hiirenkäsittelijän. Aloittaa pelin. Tallentaa pelin aloitusajan.
    """
    alusta_tila()
    tila["taso"], tila["miinojen_lkm"], tila["leveys"], tila["korkeus"] = kysy_taso() 
    tila["miinoja_jäljellä"] = tila["miinojen_lkm"]
    tila["peli_kentta"] = luo_kentta(tila["leveys"], tila["korkeus"])
    tila["pelaajan_kentta"] = luo_kentta(tila["leveys"], tila["korkeus"])
    vapaat_ruudut = luo_vapaat_ruudut(tila["leveys"], tila["korkeus"])
    miinoita(tila["peli_kentta"], vapaat_ruudut, tila["miinojen_lkm"])
    aseta_numerot()
    
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(40 * tila["leveys"], 40 * tila["korkeus"] + 30) #säädetään ikkunan koko
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    tila["aika"]["aloitus_aika"] = time.perf_counter()
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_toistuva_kasittelija(paivitys_kasittelija, 1/10)
    haravasto.aloita()            
            
def valikko():
    """
    Tulostaa käyttäjälle mahdolliset valinnat. Kysyy käyttäjältä syötteen, joka tallenetaan valinta-muutujaan. 
    Käyttäjän valinnan mukaan joko aloitetaan uusi peli, tulostetaan tilastot tai lopetetaan peli.
    Valinnan ollessa "lopeta" tarkisetaan vielä onko käyttäjä varma.
    """
  
    valinta = ""
    varmistus_valinta = ""
    while varmistus_valinta != "k" and varmistus_valinta != "kyllä":
        print("Valinnat: ")
        print("(A)loita uusi peli")
        print("(T)ulosta tilastot")
        print("(L)opeta")
        valinta = input("Tee valintasi: ").strip().lower()
        if valinta == "a" or valinta == "aloita":
            aloita_uusi_peli()
            #kun peli loppuu, palataan tähän
            if tila["tulos"] == "voitto":
                tila["pelaajan_nimi"] = input("Pelaaja: ")
                tallenna_pelitiedot("pelitulokset.txt")
        elif valinta == "t" or valinta == "tulosta":
            tilasto = lataa_tilastot("pelitulokset.txt")
            tilasto.sort(key=palauta_kesto)
            tulosta_tilastot(tilasto)
        elif valinta == "l" or valinta == "lopeta":
            while True:
                varmistus_valinta = input("Oletko varma? (kyllä/ei) \n").strip().lower()
                if varmistus_valinta == "k" or varmistus_valinta == "kyllä":
                    print("Peli lopetettu.")
                    break
                elif varmistus_valinta == "e" or varmistus_valinta == "ei":
                    break
                else:
                    print("Valitsemaasi toimintoa ei ole olemassa")              
        else:
            print("Valitsemaasi toimintoa ei ole olemassa.")
    
if __name__ == "__main__":
    valikko()