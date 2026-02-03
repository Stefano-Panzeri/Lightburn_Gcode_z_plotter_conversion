import re
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import os.path

# --------------------------------------------------------------------------------------
# Tekstovi za jezike (EN / HR)
# --------------------------------------------------------------------------------------

STRINGS = {
    "en": {
        "title": "LightBurn G-code → PEN converter",
        "btn_open": "Open G-code",
        "btn_convert": "Apply pen conversion",
        "btn_save": "Save as...",
        "lbl_pen_up": "Pen up Z:",
        "lbl_pen_down": "Pen down Z:",
        "lbl_pause": "Pause (s):",
        "chk_clean_end": "Remove M9 / G1 S0 / M2",
        "chk_keep_orig": "Keep original as comment",
        "lang_label": "Language:",
        "msg_no_content_title": "Warning",
        "msg_no_content": "There is no content to convert.",
        "msg_invalid_numbers_title": "Error",
        "msg_invalid_numbers": "Pen up/down and Pause must be numeric values.",
        "msg_convert_done_title": "Done",
        "msg_convert_done": "Pen conversion has been applied to the current text.",
        "msg_read_error_title": "Error",
        "msg_read_error": "Cannot read file:",
        "msg_write_error_title": "Error",
        "msg_write_error": "Cannot write file:",
        "msg_saved_title": "Saved",
        "msg_saved_prefix": "File has been saved as:",
        "insert_gcode_begin": "; Insert here the gcode you want to add at the beginning of the file.",
        "insert_gcode_end": "; Insert here the gcode you want to add at the end of the file.",
        "initial_help": (
            "; How to use this tool:\n"
            "; 1. Click 'Open G-code' and load a LightBurn G-code file (.gcode / .nc/ .gc / .ngc).\n"
            "; 2. Adjust Pen up Z, Pen down Z and Pause if needed.\n"
            "; 3. Optionally enable removing end commands (M9 / G1 S0 / M2)\n"
            ";    and/or keeping the original line as a comment.\n"
            "; 4. Click 'Apply pen conversion'.\n"
            "; 5. Click 'Save as...' to save the converted G-code for your pen plotter.\n\n"
        ),
    },
    "it": {
        "title": "Convertitore LightBurn G-code → PEN",
        "btn_open": "Apri G-code",
        "btn_convert": "Applica la conversione",
        "btn_save": "Salva come...",
        "lbl_pen_up": "Penna alzata Z:",
        "lbl_pen_down": "Pen abbassata Z:",
        "lbl_pause": "Pausa (s):",
        "chk_clean_end": "Rimuovi M9 / G1 S0 / M2",
        "chk_keep_orig": "Conserva l'originale come commento",
        "lang_label": "Lingua:",
        "msg_no_content_title": "Attenzione",
        "msg_no_content": "Non c'é contenuto da convertire.",
        "msg_invalid_numbers_title": "Errore",
        "msg_invalid_numbers": "Penna alzata/abbassata e Pausa devono avere valori numerici.",
        "msg_convert_done_title": "Fatto",
        "msg_convert_done": "La conversione alla penna è stata applicata al testo corrente.",
        "msg_read_error_title": "Errore",
        "msg_read_error": "Impossibile leggere il file:",
        "msg_write_error_title": "Errore",
        "msg_write_error": "Impossibile scrivere il file:",
        "msg_saved_title": "Salvato",
        "msg_saved_prefix": "Il file è stato salvato come:",
        "insert_gcode_begin": "; Inserisci qui il gcode che vuoi aggiungere all'inizio del file.",
        "insert_gcode_end": "; Inserisci qui il gcode che vuoi aggiungere alla fine del file.",
        "initial_help": (
            "; Come usare questo strumento:\n"
            "; 1. Clicca su 'Apri G-code' e carica un file G-code di LightBurn G-code (.gcode / .nc/ .gc / .ngc).\n"
            "; 2. Regola Penna alzata Z, Penna abbassata Z e Pause se necessario.\n"
            "; 3. Opzionalmente abilita la rimozione dei comandi di fine (M9 / G1 S0 / M2)\n"
            ";    e/o conserva la linea originale come commento.\n"
            "; 4. Clicca 'Applica la conversione'.\n"
            "; 5. Clicca 'Salva come...' per salvare il file G-code convertito per il tuo plotter a penna.\n\n"
        ),
    },
    "es": {
        "title": "Convertidor LightBurn G-code → PEN",
        "btn_open": "Abrir G-code",
        "btn_convert": "Aplicar conversión",
        "btn_save": "Guardar como...",
        "lbl_pen_up": "Boligrafo levantado Z:",
        "lbl_pen_down": "Boligrafo bajado Z:",
        "lbl_pause": "Pausa (s):",
        "chk_clean_end": "Eliminar M9 / G1 S0 / M2",
        "chk_keep_orig": "Conservar el original como comentario",
        "lang_label": "Idioma:",
        "msg_no_content_title": "Advertencia",
        "msg_no_content": "No hay contenido para convertir.",
        "msg_invalid_numbers_title": "Error",
        "msg_invalid_numbers": "Boligrafo levantado/bajado y Pausa deben tener valores numéricos.",
        "msg_convert_done_title": "Hecho",
        "msg_convert_done": "La conversión a boligrafo ha sido aplicada al texto actual.",
        "msg_read_error_title": "Error",
        "msg_read_error": "No se pudo leer el archivo:",
        "msg_write_error_title": "Error",
        "msg_write_error": "No se pudo escribir el archivo:",
        "msg_saved_title": "Guardado",
        "msg_saved_prefix": "El archivo ha sido guardado como:",
        "insert_gcode_begin": "; Inserta aquí el gcode que quieras añadir al inicio del archivo.",
        "insert_gcode_end": "; Inserta aquí el gcode que quieras añadir al final del archivo.",
        "initial_help": (
            "; Cómo usar esta herramienta:\n"
            "; 1. Haz clic en 'Abrir G-code' y carga un archivo G-code de LightBurn (.gcode / .nc / .gc / .ngc).\n"
            "; 2. Ajusta Boligrafo levantado Z, Boligrafo bajado Z y Pausa si es necesario.\n"
            "; 3. Opcionalmente habilita la eliminación de comandos de fin (M9 / G1 S0 / M2)\n"
            ";    y/o conserva la línea original como comentario.\n"
            "; 4. Haz clic en 'Aplicar conversión'.\n"
            "; 5. Haz clic en 'Guardar como...' para guardar el archivo G-code convertido para tu plotter de boligrafo.\n\n"
        ),
    },
    "hr": {
        "title": "LightBurn G-code → PEN konverter",
        "btn_open": "Otvori G-code",
        "btn_convert": "Primijeni pen konverziju",
        "btn_save": "Spremi kao...",
        "lbl_pen_up": "Pen up Z:",
        "lbl_pen_down": "Pen down Z:",
        "lbl_pause": "Pauza (s):",
        "chk_clean_end": "Izbriši M9 / G1 S0 / M2",
        "chk_keep_orig": "Sačuvaj original kao komentar",
        "lang_label": "Jezik:",
        "msg_no_content_title": "Upozorenje",
        "msg_no_content": "Nema sadržaja za konverziju.",
        "msg_invalid_numbers_title": "Greška",
        "msg_invalid_numbers": "Pen up/down i Pauza moraju biti brojčane vrijednosti.",
        "msg_convert_done_title": "Gotovo",
        "msg_convert_done": "Pen konverzija je primijenjena na trenutni tekst.",
        "msg_read_error_title": "Greška",
        "msg_read_error": "Ne mogu pročitati datoteku:",
        "msg_write_error_title": "Greška",
        "msg_write_error": "Ne mogu zapisati datoteku:",
        "msg_saved_title": "Spremljeno",
        "msg_saved_prefix": "Datoteka je spremljena kao:",
        "insert_gcode_begin": "; Ovdje umetnite gcode koji želite dodati na početak datoteke.",
        "insert_gcode_end": "; Ovdje umetnite gcode koji želite dodati na kraj datoteke.",
        "initial_help": (
            "; Kako koristiti ovaj alat:\n"
            "; 1. Klikni 'Otvori G-code' i učitaj LightBurn G-code datoteku (.gcode / .nc/ .gc / .ngc).\n"
            "; 2. Po potrebi prilagodi Pen up Z, Pen down Z i Pauzu.\n"
            "; 3. Opcionalno uključi brisanje završnih naredbi (M9 / G1 S0 / M2)\n"
            ";    i/ili čuvanje originalne linije kao komentar.\n"
            "; 4. Klikni 'Primijeni pen konverziju'.\n"
            "; 5. Klikni 'Spremi kao...' da spremiš konvertirani G-code za pen ploter.\n\n"
        ),
    },
}


def process_gcode(
    text: str,
    pen_up_z: float = 5.0,
    pen_down_z: float = 1.0,
    pause_s: float = 0.5,
    clean_end: bool = False,
    keep_original: bool = False,
) -> str:
    """
    Obrada G-codea:
    - po želji briše završne kodove (M9, G1 S0, M2) ako je clean_end=True
    - briše SXXXX (laser power) iz svih linija (čak i kad je zalijepljen: ...Y117.02S700F12000)
    - briše / komentira M3/M4/M5 linije (laser on/off)
    - PEN UP se dodaje samo kada prelazimo iz G1 (rezanje) u G0 (travel) s X ili Y
    - PEN DOWN se dodaje samo kada prelazimo iz G0 (travel) u G1 (rezanje) s X ili Y
    - ako je keep_original=True, prije svakog modificiranog reda doda se
      komentar: "; orig: <originalni red>"
    """

    lines = text.splitlines()
    out_lines = []

    z_up_str = f"{pen_up_z:g}"
    z_down_str = f"{pen_down_z:g}"
    pause_str = f"{pause_s:g}"

    prev_motion = None  # None, "G0", "G1"

    for line in lines:
        original = line
        stripped = line.strip()

        if stripped == "":
            out_lines.append("")
            continue

        if stripped.startswith(";"):
            out_lines.append(original)
            continue

        if clean_end:
            if re.match(r"^M9\b", stripped, flags=re.IGNORECASE):
                if keep_original:
                    out_lines.append(f"; orig (removed end cmd): {original}")
                continue
            if re.match(r"^M2\b", stripped, flags=re.IGNORECASE):
                if keep_original:
                    out_lines.append(f"; orig (removed end cmd): {original}")
                continue
            if re.match(r"^G1\b.*\bS0\b", stripped, flags=re.IGNORECASE):
                if keep_original:
                    out_lines.append(f"; orig (removed end cmd): {original}")
                continue

        # ukloni S vrijednosti (S700, S0, S1000...)
        no_s = re.sub(r"S\d+(\.\d+)?", "", stripped, flags=re.IGNORECASE)
        no_s = re.sub(r"\s+", " ", no_s).strip()

        # ukloni M3/M4/M5
        if re.match(r"^(M3|M4|M5)\b", no_s, flags=re.IGNORECASE):
            if keep_original:
                out_lines.append(f"; orig: {original}")
            out_lines.append(f"; removed laser cmd: {original}")
            continue

        # detekcija G0 / G1
        is_g0_cmd = re.match(r"^G0+(\s|[XYZFIJKS]|$)", no_s, flags=re.IGNORECASE) is not None
        is_g1_cmd = re.match(r"^G1+(\s|[XYZFIJKS]|$)", no_s, flags=re.IGNORECASE) is not None

        is_g0_xy = is_g0_cmd and ("X" in no_s or "Y" in no_s)
        is_g1_xy = is_g1_cmd and ("X" in no_s or "Y" in no_s)

        if keep_original:
            out_lines.append(f"; orig: {original}")

        if is_g0_xy:
            if prev_motion == "G1":
                out_lines.append(f"G0 Z{z_up_str}    ; pen up")
                out_lines.append(f"G4 P{pause_str}    ; wait {pause_str} s")

            out_lines.append(no_s + "    ; travel move")
            prev_motion = "G0"

        elif is_g1_xy:
            if prev_motion == "G0":
                out_lines.append(f"G0 Z{z_down_str}    ; pen down")
                out_lines.append(f"G4 P{pause_str}    ; wait {pause_str} s")

            out_lines.append(no_s + "    ; cutting move")
            prev_motion = "G1"

        else:
            if is_g0_cmd:
                prev_motion = "G0"
            elif is_g1_cmd:
                prev_motion = "G1"

            out_lines.append(no_s)

    return "\n".join(out_lines) + "\n"


class GCodePenApp:
    def __init__(self, root):
        self.root = root

        # default: engleski
        self.lang = "en"

        self.current_path = None

        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        # Gornja traka s gumbima
        top_bar = tk.Frame(frame)
        top_bar.pack(fill=tk.X, pady=5, padx=5)

        self.btn_open = tk.Button(top_bar, command=self.open_file)
        self.btn_open.pack(side=tk.LEFT, padx=2)

        self.btn_convert = tk.Button(top_bar, command=self.convert_current_text)
        self.btn_convert.pack(side=tk.LEFT, padx=2)

        self.btn_save = tk.Button(top_bar, command=self.save_file_as)
        self.btn_save.pack(side=tk.LEFT, padx=2)

        # Postavke
        settings_frame = tk.Frame(frame)
        settings_frame.pack(fill=tk.X, pady=5, padx=5)

        self.pen_up_var = tk.StringVar(value="5")
        self.pen_down_var = tk.StringVar(value="1")
        self.pause_var = tk.StringVar(value="0.5")

        self.clean_end_var = tk.IntVar(value=1)
        self.keep_orig_var = tk.IntVar(value=0)

        self.lbl_pen_up = tk.Label(settings_frame)
        self.entry_pen_up = tk.Entry(settings_frame, width=6, textvariable=self.pen_up_var)
        self.lbl_pen_up.pack(side=tk.LEFT)
        self.entry_pen_up.pack(side=tk.LEFT, padx=(2, 10))

        self.lbl_pen_down = tk.Label(settings_frame)
        self.entry_pen_down = tk.Entry(settings_frame, width=6, textvariable=self.pen_down_var)
        self.lbl_pen_down.pack(side=tk.LEFT)
        self.entry_pen_down.pack(side=tk.LEFT, padx=(2, 10))

        self.lbl_pause = tk.Label(settings_frame)
        self.entry_pause = tk.Entry(settings_frame, width=6, textvariable=self.pause_var)
        self.lbl_pause.pack(side=tk.LEFT)
        self.entry_pause.pack(side=tk.LEFT, padx=(2, 10))

        self.chk_clean_end = tk.Checkbutton(
            settings_frame,
            variable=self.clean_end_var,
        )
        self.chk_clean_end.pack(side=tk.LEFT, padx=(10, 5))

        self.chk_keep_orig = tk.Checkbutton(
            settings_frame,
            variable=self.keep_orig_var,
        )
        self.chk_keep_orig.pack(side=tk.LEFT, padx=(5, 5))

        # Jezik
        self.lbl_lang = tk.Label(settings_frame)
        self.lbl_lang.pack(side=tk.LEFT, padx=(15, 2))

        self.lang_var = tk.StringVar(value=self.lang)
        self.opt_lang = tk.OptionMenu(
            settings_frame,
            self.lang_var,
            "en",
            "it",
            "es",
            "hr",
            command=self.on_language_change,
        )
        self.opt_lang.pack(side=tk.LEFT)
        
        # Postavke
        append_gcode_frame = tk.Frame(frame)
        append_gcode_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.entry_gcode_begin = tk.Text(append_gcode_frame, wrap=tk.NONE, undo=True, height=8, width=30)
        self.entry_gcode_begin.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=5, pady=5)
        
        y_scroll_gcode_begin = tk.Scrollbar(append_gcode_frame, orient=tk.VERTICAL, command=self.entry_gcode_begin.yview)
        y_scroll_gcode_begin.pack(side=tk.LEFT, fill=tk.Y)
        self.entry_gcode_begin.configure(yscrollcommand=y_scroll_gcode_begin.set)
        
        self.entry_gcode_end = tk.Text(append_gcode_frame, wrap=tk.NONE, undo=True, height=8, width=30)
        self.entry_gcode_end.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=5, pady=5)
        
        y_scroll_gcode_end = tk.Scrollbar(append_gcode_frame, orient=tk.VERTICAL, command=self.entry_gcode_end.yview)
        y_scroll_gcode_end.pack(side=tk.LEFT, fill=tk.Y)
        self.entry_gcode_end.configure(yscrollcommand=y_scroll_gcode_end.set)
        
        
        self.entry_gcode_begin.insert("1.0", STRINGS[self.lang]["insert_gcode_begin"])
        self.entry_gcode_end.insert("1.0", STRINGS[self.lang]["insert_gcode_end"])

        # Tekst područje
        gcode_frame = tk.Frame(frame)
        gcode_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        
        
        self.text = tk.Text(gcode_frame, wrap=tk.NONE, undo=True, height=20)
        self.text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

        y_scroll = tk.Scrollbar(gcode_frame, orient=tk.VERTICAL, command=self.text.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.configure(yscrollcommand=y_scroll.set)

        gcode_scrollbar_frame = tk.Frame(frame)
        gcode_scrollbar_frame.pack(fill=tk.X, pady=0, padx=5) 
        x_scroll = tk.Scrollbar(gcode_scrollbar_frame, orient=tk.HORIZONTAL, command=self.text.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.configure(xscrollcommand=x_scroll.set)

        # inicijalni help za ENG
        self.text.insert("1.0", STRINGS[self.lang]["initial_help"])

        # primijeni tekstove za ENG
        self.update_language()
        self.load_config()

    # -------------------------------------------------------------------------
    # i18n helperi
    # -------------------------------------------------------------------------

    def tr(self, key: str) -> str:
        return STRINGS[self.lang].get(key, key)

    def update_window_title(self):
        base = self.tr("title")
        if self.current_path is not None:
            self.root.title(f"{base} - {self.current_path.name}")
        else:
            self.root.title(base)

    def update_language(self):
        self.update_window_title()
        self.btn_open.configure(text=self.tr("btn_open"))
        self.btn_convert.configure(text=self.tr("btn_convert"))
        self.btn_save.configure(text=self.tr("btn_save"))
        self.lbl_pen_up.configure(text=self.tr("lbl_pen_up"))
        self.lbl_pen_down.configure(text=self.tr("lbl_pen_down"))
        self.lbl_pause.configure(text=self.tr("lbl_pause"))
        self.chk_clean_end.configure(text=self.tr("chk_clean_end"))
        self.chk_keep_orig.configure(text=self.tr("chk_keep_orig"))
        self.lbl_lang.configure(text=self.tr("lang_label"))

    def on_language_change(self, value):
        """Promjena jezika + po potrebi promjena initial_help teksta."""
        if value in STRINGS:
            # zapamti stari jezik i njegov help
            old_lang = self.lang
            old_help = STRINGS[old_lang]["initial_help"].strip()
            old_gcode_begin_help = STRINGS[old_lang]["insert_gcode_begin"].strip()
            old_gcode_end_help = STRINGS[old_lang]["insert_gcode_end"].strip()

            current_text = self.text.get("1.0", tk.END)
            current_stripped = current_text.strip()
            
            current_gcode_begin = self.entry_gcode_begin.get("1.0", tk.END)
            current_gcode_begin_stripped = current_gcode_begin.strip()
            
            current_gcode_end = self.entry_gcode_end.get("1.0", tk.END)
            current_gcode_end_stripped = current_gcode_end.strip()

            # treba li zamijeniti help?
            # da ako je text prazan ili ako je samo stari help unutra
            should_replace_help = (
                current_stripped == "" or current_stripped == old_help
            )
            should_replace_gcode_begin_help = (
                current_gcode_begin_stripped == "" or current_gcode_begin_stripped == old_gcode_begin_help
            )
            should_replace_gcode_end_help = (
                current_gcode_end_stripped == "" or current_gcode_end_stripped == old_gcode_end_help
            )

            # promijeni jezik GUI-ja
            self.lang = value
            self.update_language()

            # ako smo do sada prikazivali samo help, zamijeni novim helpom
            if should_replace_help:
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", STRINGS[self.lang]["initial_help"])
            if should_replace_gcode_begin_help:
                self.entry_gcode_begin.delete("1.0", tk.END)
                self.entry_gcode_begin.insert("1.0", STRINGS[self.lang]["insert_gcode_begin"])
            if should_replace_gcode_end_help:
                self.entry_gcode_end.delete("1.0", tk.END)
                self.entry_gcode_end.insert("1.0", STRINGS[self.lang]["insert_gcode_end"])

    # -------------------------------------------------------------------------
    # GUI akcije
    # -------------------------------------------------------------------------

    def open_file(self):
        path = filedialog.askopenfilename(
            title=self.tr("btn_open"),
            filetypes=[
                ("G-code", "*.gcode *.nc *.ngc *.txt *.gc"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        try:
            p = Path(path)
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            messagebox.showerror(
                self.tr("msg_read_error_title"),
                f"{self.tr('msg_read_error')}\n{e}",
            )
            return

        self.current_path = p
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", text)
        self.update_window_title()

    def convert_current_text(self):
        content = self.text.get("1.0", tk.END)
        if not content.strip():
            messagebox.showwarning(
                self.tr("msg_no_content_title"),
                self.tr("msg_no_content"),
            )
            return

        try:
            pen_up_z = float(self.pen_up_var.get().replace(",", "."))
            pen_down_z = float(self.pen_down_var.get().replace(",", "."))
            pause_s = float(self.pause_var.get().replace(",", "."))
        except ValueError:
            messagebox.showerror(
                self.tr("msg_invalid_numbers_title"),
                self.tr("msg_invalid_numbers"),
            )
            return

        clean_end = bool(self.clean_end_var.get())
        keep_original = bool(self.keep_orig_var.get())

        try:
            converted = process_gcode(
                content,
                pen_up_z=pen_up_z,
                pen_down_z=pen_down_z,
                pause_s=pause_s,
                clean_end=clean_end,
                keep_original=keep_original,
            )
        except Exception as e:
            messagebox.showerror(
                self.tr("msg_invalid_numbers_title"),
                f"Error: {e}",
            )
            return
        gcode_begin_text=self.entry_gcode_begin.get('1.0', 'end')
        gcode_end_text=self.entry_gcode_end.get('1.0', 'end')
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", gcode_begin_text)
        self.text.insert(tk.END, converted)
        self.text.insert(tk.END, gcode_end_text)
        messagebox.showinfo(
            self.tr("msg_convert_done_title"),
            self.tr("msg_convert_done"),
        )
        
        
    def load_config(self):
        load_path = Path().resolve()
        name_of_file = "gcode_pen_gui"
        completeName = os.path.join(load_path, name_of_file+".cfg")

        try:
            with open(completeName, "r") as cfg:
                content = cfg.read()
                
                # Parse the content
                lines = content.split('\n')
                config_dict = {}
                
                for line in lines:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config_dict[key] = value
                
                # Set the values back to the interface
                if 'entry_gcode_begin' in config_dict:
                    self.entry_gcode_begin.delete("1.0", tk.END)
                    begin_lines=config_dict['entry_gcode_begin'].split('#')
                    for idx, line in enumerate(begin_lines):
                        self.entry_gcode_begin.insert(tk.END, line)
                        if(idx<len(begin_lines)-1):
                            self.entry_gcode_begin.insert(tk.END, '\n')
                
                if 'entry_gcode_end' in config_dict:
                    self.entry_gcode_end.delete("1.0", tk.END)
                    end_lines=config_dict['entry_gcode_end'].split('#')
                    for idx, line in enumerate(end_lines):   
                        self.entry_gcode_end.insert(tk.END, line)
                        if(idx<len(end_lines)-1):
                            self.entry_gcode_end.insert(tk.END, '\n')
                
                if 'pen_up_var' in config_dict:
                    self.pen_up_var.set(config_dict['pen_up_var'])
                
                if 'pen_down_var' in config_dict:
                    self.pen_down_var.set(config_dict['pen_down_var'])
                
                if 'pause_var' in config_dict:
                    self.pause_var.set(config_dict['pause_var'])
                    
        except FileNotFoundError:
            print(f"Config file not found: {completeName}")
        except Exception as e:
            print(f"Error loading config: {e}")
            
       
    def save_config(self):
        #save settings
       

        save_path = Path().resolve()
        name_of_file = "gcode_pen_gui"
        completeName = os.path.join(save_path, name_of_file+".cfg")         

        cfg = open(completeName, "w")
        toFile = self.entry_gcode_begin.get("1.0", tk.END).rstrip().replace("\n", "#")
        cfg.write("entry_gcode_begin=")
        cfg.write(toFile)
        cfg.write("\n");
        toFile = self.entry_gcode_end.get("1.0", tk.END).rstrip().replace("\n", "#")
        cfg.write("entry_gcode_end=")
        cfg.write(toFile)
        cfg.write("\n");
        toFile = self.pen_up_var.get()
        cfg.write("pen_up_var=")
        cfg.write(toFile)  
        toFile = self.pen_down_var.get()
        cfg.write("\npen_down_var=")
        cfg.write(toFile)
        toFile = self.pause_var.get()
        cfg.write("\npause_var=")
        cfg.write(toFile)         
        cfg.close()
        
    
    def save_file_as(self):
                
        #save file
        self.save_config()
        initial_name = "output.gcode"
        if self.current_path is not None:
            initial_name = self.current_path.with_name(
                self.current_path.stem + "_PEN" + self.current_path.suffix
            ).name

        path = filedialog.asksaveasfilename(
            title=self.tr("btn_save"),
            defaultextension=".gcode",
            initialfile=initial_name,
            filetypes=[
                ("G-code", "*.gcode *.nc *.ngc *.txt"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        try:
            text = self.text.get("1.0", tk.END)
            Path(path).write_text(text, encoding="utf-8")
        except Exception as e:
            messagebox.showerror(
                self.tr("msg_write_error_title"),
                f"{self.tr('msg_write_error')}\n{e}",
            )
            return

        messagebox.showinfo(
            self.tr("msg_saved_title"),
            f"{self.tr('msg_saved_prefix')}\n{path}",
        )


def main():
    root = tk.Tk()
    root.geometry("1400x600")
    app = GCodePenApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
