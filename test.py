def amenakudum(ziel, status):
    if status < ziel:
        print("Hallo")
        amenakudum(ziel, status + 1)


amenakudum(4, 2)
