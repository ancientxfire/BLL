import os

DATEIEN = ["schüler.json","projekte.json"]


def altesProjektLoeschen():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for datei in DATEIEN:
        path = dir_path+"/"+datei
        os.remove(path=path)


if __name__ == "__main__":
    altesProjektLoeschen()
