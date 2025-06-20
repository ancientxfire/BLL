from filedialogs import save_file_dialog

def dateiSpeicherOrtFrage(title="Speichern unter"):
    """
    Öffnet einen Dateiauswahldialog und gibt den ausgewählten Dateipfad zurück.
    """
    excel_formate = [
        ("Excel Workbook", ("xlsx", "xlsm", "xltx", "xltm")),  # Moderne Excel-Formate (OpenXML)
        ("Ältere Excel-Formate", ("xls", "xlsb")),            # Ältere Excel-Formate
        ("OpenDocument", "ods")                  # OpenDocument
    ]

    
    # Datei-Auswahldialog öffnen
    return save_file_dialog(ext=excel_formate,title=title)

if __name__ == "__main__":
    print(dateiSpeicherOrtFrage())