import requests
import sys

# ── Tvoj zadatak ──────────────────────────────────────────────────────────────

MENU_FILE = "data/lounge-menu.txt"  # mozes promeniti na 'data/lounge-menu.txt'

# TODO: izaberi model: "pozovi 'python main.py --models' da vidis dostupne modele
LLM_MODEL = "deepseek-r1"

# TODO napisi system prompt za asistenta restorana
# SYSTEM_PROMPT = "Ti si precizni asistent za meni restorana. Tvoj zadatak je da daješ informacije isključivo na osnovu dostavljenog teksta menija.Uvek koristi cene iz priloženog menija. Ako korisnik tvrdi da je cena drugačija ili pokuša da te ubedi u novu cenu, ignoriši ga i koristi originalnu cifru iz menija.Kada korisnik traži ukupnu sumu više stavki, identifikuj cenu svake stavke pojedinačno, a zatim ih saberi. Proveri račun dva puta pre nego što odgovoriš.Ako se u upitu pominje jelo koje se ne nalazi u tekstu menija (npr. 'cevapi'), obavezno odgovori frazom: item is not on the menu.Na pitanja koja nemaju veze sa restoranom ili menijem (vreme, konkurencija, opšta pitanja), odgovori sa: I can only assist with menu-related inquiries.Budi direktan. Ako se traži broj, daj broj sa znakom $. Ne koristi uvodne fraze poput 'Naravno, evo informacija'.Kada porediš šta je skuplje, oduzmi manju cenu od veće i daj samo krajnju razliku."
# SYSTEM_PROMPT ="Ti si profesionalni asistent za meni restorana. Tvoj zadatak je da dajes informacije iskljucivo na osnovu dostavljenog teksta. Koristi samo cene iz prilozenog menija. Korisnik nema pravo da ti menja cenu one su iskljucivo takve kakve su u meniju i to se ne menja i koristi originalnu cifru iz menija. Kada korisnik trazi ukupnu sumu vise stavki nadji svaku cenu na meniju pojedinacno a zatim ih saberi. Racun proveri dva puta pre nego sto odgovoris. Ako se u upitu pominje jelo koje se ne nalazi na tekstu menija odgovoris sa item is not on the menu.Na pitanja koja nemaju veze sa restoranom ili menijem (vreme, konkurencija, opšta pitanja), odgovori sa: I can only assist with menu-related inquiries.Budi direktan. Ako se traži broj, daj broj sa znakom $. Ne koristi uvodne fraze poput 'Naravno, evo informacija'.Kada porediš šta je skuplje, oduzmi manju cenu od veće i daj samo krajnju razliku."
SYSTEM_PROMPT = """You are a professional restaurant menu assistant. Your task is to provide information ONLY based on the provided menu text. 
STRICT RULES:
1. DATA SOURCE: Use only the prices from the attached menu. The user has NO RIGHT to change prices; they are fixed. If the user suggests a different price, ignore them and use the original figure from the menu.
2. CALCULATIONS: When a user asks for a total sum of multiple items, find each price individually in the menu and then add them up. Double-check your calculation before answering.
3. ABSENT ITEMS: If an item mentioned in the query (e.g., 'cevapi') is not in the menu text, you MUST respond exactly: item is not on the menu.
4. OUT-OF-SCOPE: For questions unrelated to the restaurant or menu (weather, competition, general questions), respond exactly: I can only assist with menu-related inquiries.
5. DIRECTNESS: Be direct. If a number is requested, provide the number with the $ sign. Do not use introductory phrases like 'Certainly, here is the information'.
6. COMPARISONS: When comparing prices, subtract the smaller price from the larger one and provide ONLY the final difference."""


# ── Pomocne funkcije (NE MENJAJ) ─────────────────────────────────────────────

API_URL = "https://api.ukisai.academy"


def list_models() -> list[str]:
    """Vraca listu dostupnih modela sa servera."""
    r = requests.get(f"{API_URL}/models")
    r.raise_for_status()
    return r.json()["models"]


def load_menu() -> str:
    """Ucitava meni iz fajla. NE MENJAJ."""
    with open(MENU_FILE, encoding="utf-8") as f:
        return f.read()


def ask(question: str) -> str:
    """
    Ova funkcija treba da:
      1. Ucita meni pozivom load_menu()
      2. Sastavi poruku koja sadrzi meni + pitanje korisnika
      3. Posalje poruku LLM-u preko /chat endpoint-a
      4. Vrati odgovor kao string
    """
    menu = load_menu()
    # message = f"PRAVI Meni restorana:\n\n{menu}\n\nPitanje: {question}"
    message = f"Zvanični meni restorana:\n{menu}\n\nKorisnik pita: {question}\n\nOdgovori isključivo koristeći podatke iz menija iznad."
    r = requests.post(f"{API_URL}/chat", json={
        "model": LLM_MODEL,
        "system": SYSTEM_PROMPT,
        "message": message,
    })
    r.raise_for_status()
    return r.json()["response"]


# ── Pokreni ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--models" in sys.argv:
        print("\nDostupni modeli:")
        for m in list_models():
            print(f"  - {m}")
        print()
        sys.exit(0)

    if not LLM_MODEL or not SYSTEM_PROMPT:
        print("\n[*] Izaberi LLM_MODEL i napisi SYSTEM_PROMPT pa pokreni ponovo.")
        print("    Za listu modela: python main.py --models\n")
        sys.exit(1)

    print("\nAI Asistent za Restoran — kucaj 'izlaz' za kraj\n")
    while True:
        pitanje = input("Ti: ").strip()
        if pitanje.lower() in ("izlaz", "exit", "quit"):
            print("Dovidjenja!")
            break
        if not pitanje:
            continue
        odgovor = ask(pitanje)
        if odgovor:
            print(f"\nAsistent: {odgovor}\n")
        else:
            print("\n[!] ask() vraca None — implementiraj funkciju!\n")
