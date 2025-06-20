from filedialogs import  open_file_dialog

def dateiAuswahl():
    """
    Öffnet einen Dateiauswahldialog und gibt den ausgewählten Dateipfad zurück.
    """
    excel_formate = [
        ("Excel Workbook", ("xlsx", "xlsm", "xltx", "xltm")),  # Moderne Excel-Formate (OpenXML)
        ("Ältere Excel-Formate", ("xls", "xlsb")),            # Ältere Excel-Formate
        ("OpenDocument", "ods")                  # OpenDocument
    ]

    
    # Datei-Auswahldialog öffnen
    return open_file_dialog(ext=excel_formate)

