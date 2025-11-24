import re
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

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
        "initial_help": (
            "; How to use this tool:\n"
            "; 1. Click 'Open G-code' and load a LightBurn G-code file (.gcode / .nc / .ngc).\n"
            "; 2. Adjust Pen up Z, Pen down Z and Pause if needed.\n"
            "; 3. Optionally enable removing end commands (M9 / G1 S0 / M2)\n"
            ";    and/or keeping the original line as a comment.\n"
            "; 4. Click 'Apply pen conversion'.\n"
            "; 5. Click 'Save as...' to save the converted G-code for your pen plotter.\n\n"
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
        "initial_help": (
            "; Kako koristiti ovaj alat:\n"
            "; 1. Klikni 'Otvori G-code' i učitaj LightBurn G-code datoteku (.gcode / .nc / .ngc).\n"
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
    pen_up_z: float = -35.0,
    pen_down_z: float = -38.0,
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

        self.pen_up_var = tk.StringVar(value="-35")
        self.pen_down_var = tk.StringVar(value="-38")
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
            "hr",
            command=self.on_language_change,
        )
        self.opt_lang.pack(side=tk.LEFT)

        # Tekst područje
        self.text = tk.Text(frame, wrap=tk.NONE, undo=True)
        self.text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

        y_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.text.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.configure(yscrollcommand=y_scroll.set)

        x_scroll = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.text.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.configure(xscrollcommand=x_scroll.set)

        # inicijalni help za ENG
        self.text.insert("1.0", STRINGS[self.lang]["initial_help"])

        # primijeni tekstove za ENG
        self.update_language()

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

            current_text = self.text.get("1.0", tk.END)
            current_stripped = current_text.strip()

            # treba li zamijeniti help?
            # da ako je text prazan ili ako je samo stari help unutra
            should_replace_help = (
                current_stripped == "" or current_stripped == old_help
            )

            # promijeni jezik GUI-ja
            self.lang = value
            self.update_language()

            # ako smo do sada prikazivali samo help, zamijeni novim helpom
            if should_replace_help:
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", STRINGS[self.lang]["initial_help"])

    # -------------------------------------------------------------------------
    # GUI akcije
    # -------------------------------------------------------------------------

    def open_file(self):
        path = filedialog.askopenfilename(
            title=self.tr("btn_open"),
            filetypes=[
                ("G-code", "*.gcode *.nc *.ngc *.txt"),
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

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", converted)
        messagebox.showinfo(
            self.tr("msg_convert_done_title"),
            self.tr("msg_convert_done"),
        )

    def save_file_as(self):
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
    root.geometry("1000x650")
    app = GCodePenApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
