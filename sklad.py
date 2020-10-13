from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import sqlite3

root = Tk()
root.title("Sklad v Pythonu")
root.geometry("500x500")

# Vytvoření/napojení databáze
conn = sqlite3.connect('sklad.db')

# Vytvoření kurzoru
c = conn.cursor()

# Vytvoření tabulky
'''
c.execute("""CREATE TABLE alba (
        nazev_alba text,
        umelec text,
        datum_vydani integer,
        cover blob
        )""")
'''

# Vytvoření Submit funkce pro databázi
def submit():
        # Vytvoření/napojení databáze
        conn = sqlite3.connect('sklad.db')
        # Vytvoření kurzoru
        c = conn.cursor()

        # Vložení do tabulky
        c.execute("INSERT INTO alba VALUES (:nazev_alba, :umelec, :datum_vydani, :cover)",
                {
                        'nazev_alba': nazev_alba.get(),
                        'umelec': umelec.get(),
                        'datum_vydani': datum_vydani.get(),
                        'cover': root.filename
                })        

        # Potvrzení změn
        conn.commit()

        # Ukončení spojení
        conn.close()

        nazev_alba.delete(0, END)
        umelec.delete(0, END)
        datum_vydani.delete(0, END)

# Vytvoření Query funkce
def query():
        # Vytvoření/napojení databáze
        conn = sqlite3.connect('sklad.db')
        # Vytvoření kurzoru
        c = conn.cursor()

        # Dotaz na databázi
        c.execute("SELECT *,oid FROM alba")
        zaznamy = c.fetchall()
        #print(zaznamy)

        # Loop
        print_zaznamy = ''
        for zaznam in zaznamy:
                print_zaznamy += str(zaznam[0]) + " - " + str(zaznam[1]) + " - " + str(zaznam[2]) + " " + "\n" 
        
        query_label = Label(root, text=print_zaznamy)
        query_label.grid(row=6, column=0, columnspan=2)

        # cover_image = ImageTk.PhotoImage(Image.open(str(zaznam[3])))
        # image_label = Label(image=cover_image)
        # image_label.grid(row=7, column=0)

        # Potvrzení změn
        conn.commit()

        # Ukončení spojení
        conn.close()

def open():
        root.filename = filedialog.askopenfilename(initialdir="/sources", title="Vyberte soubor", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
        my_label = Label(root, text=root.filename).grid()
        my_image = ImageTk.PhotoImage(Image.open(root.filename))
        my_image_label = Label(image=my_image).grid()

# Vytvoření textových polí
nazev_alba = Entry(root, width=30)
nazev_alba.grid(row=0, column=1, padx=20)
umelec = Entry(root, width=30)
umelec.grid(row=1, column=1)
datum_vydani = Entry(root, width=30)
datum_vydani.grid(row=2, column=1)
cover = Button(root, text="Nahrát soubor", command=open)
cover.grid(row=3, column=1)

# Vytvoření popisků
nazev_alba_label = Label(root, text="Název alba")
nazev_alba_label.grid(row=0, column=0)
umelec_label = Label(root, text="Umělec")
umelec_label.grid(row=1, column=0)
datum_vydani_label = Label(root, text="Datum vydání")
datum_vydani_label.grid(row=2, column=0)
cover_label = Label(root, text="Cover alba")
cover_label.grid(row=3, column=0)

# Vytvoření Submit tlačítka
submit_btn = Button(root, text="Přidat záznam do databáze", command=submit)
submit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Vytvoření Query tlačítka
query_btn = Button(root, text="Zobrazit záznamy", command=query)
query_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# Potvrzení změn
conn.commit()

# Ukončení spojení
conn.close()

root.mainloop()