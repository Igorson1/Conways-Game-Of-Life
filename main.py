import math
import pygame
import copy
import argparse
import sys


def liczba_zywych_sasiadow(siatka, x, y, rozmiar):
    """
    funkcja sprawdza 8 sąsiednich komórek dla komórki (x; y) - zwraca liczbę żywych
    funkcja nie sprawdza pól poza granicą siatki
    """
    suma = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # bez uwzględniania aktualnie sprawdzanej komórki

            nx, ny = x + i, y + j

            # warunek żeby nie wyjść poza listę
            if 0 <= nx < rozmiar and 0 <= ny < rozmiar:
                suma += siatka[nx][ny]
    return suma


def ustawienie_przypadku(siatka, nazwa, rozmiar):
    """
    funkcja wypełnia siatkę już zdefiniowanymi ustawieniami komórek (ciekawe przypadki) wg wyboru
    """
    mid = rozmiar // 2
    if nazwa == "szybowiec":  # glider
        coords = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        for dx, dy in coords:
            siatka[mid + dx][mid + dy] = 1
    elif nazwa == "oscylator":  # 4 oscylujące prostokąty 3x1
        siatka[mid][mid - 1], siatka[mid][mid], siatka[mid][mid + 1], siatka[mid + 1][mid], siatka[mid - 1][
            mid] = 1, 1, 1, 1, 1
    elif nazwa == "generator_szybowcow":  # generator szybowców (Gosper Glider Gun)
        gen_coords = [
            (24, 0), (22, 1), (24, 1), (12, 2), (13, 2), (20, 2), (21, 2), (34, 2), (35, 2),
            (11, 3), (15, 3), (20, 3), (21, 3), (34, 3), (35, 3), (0, 4), (1, 4), (10, 4),
            (16, 4), (20, 4), (21, 4), (0, 5), (1, 5), (10, 5), (14, 5), (16, 5), (17, 5),
            (22, 5), (24, 5), (10, 6), (16, 6), (24, 6), (11, 7), (15, 7), (12, 8), (13, 8)
        ]

        przesuniecie_x, przesuniecie_y = 5, 5

        for dx, dy in gen_coords:
            nx, ny = przesuniecie_x + dx, przesuniecie_y + dy
            if 0 <= nx < rozmiar and 0 <= ny < rozmiar:
                siatka[nx][ny] = 1
    elif nazwa == "diament":  # diament - tworzy 4 szybowce

        for x in range(mid - 2, mid + 2):
            siatka[x][mid - 4] = 1

        for x in range(mid - 4, mid + 4):
            siatka[x][mid - 2] = 1

        for x in range(mid - 6, mid + 6):
            siatka[x][mid] = 1

        for x in range(mid - 4, mid + 4):
            siatka[x][mid + 2] = 1

        for x in range(mid - 2, mid + 2):
            siatka[x][mid + 4] = 1


def pobieranie_argumentow():
    """
    funkcja obsługuje argumenty z linii poleceń i ustawia dane wejściowe oraz sprawdza ich poprawność
    """
    parser = argparse.ArgumentParser(description="Conway's Game of Life", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--szybkosc", type=int, default=4, help="szybko ć symulacji (1-50). domyślnie: 4")
    parser.add_argument("--rozmiar", type=int, default=50,
                        help="rozmiar siatki (10-75) (liczba komórek w rzędzie/kolumnie). domyślnie: 50")
    parser.add_argument("--przypadek", type=str, choices=["szybowiec", "oscylator", "generator_szybowcow", "diament"],
                        help="wybierz początkowy wzór")

    args = parser.parse_args()

    # sprawdzenie poprawności danych
    if not (1 <= args.szybkosc <= 50):
        print("błąd: szybkość musi być w przedziale 1-50")
        sys.exit(1)
    if not (10 <= args.rozmiar <= 75):
        print("błąd: rozmiar planszy musi być w przedziale 10-75")
        sys.exit(1)

    return args


def main():
    # pobranie argumentów
    args = pobieranie_argumentow()

    # inicjalizacja parametrów gry
    pygame.init()
    fps = 100
    szybkosc = args.szybkosc
    rozmiar_planszy = args.rozmiar
    wielkosc_komorki = 10

    # offset robi miejsce na UI nad planszą
    offset = math.floor(1.3 * rozmiar_planszy)

    # Tworzenie siatki
    # Przykład pustej siadki 3x3, 0 odpowiada białej komórce, a 1 czarnej.
    # Na tej siatkce czarna komórka ma kordynaty [0][1]

    # 0 0 0
    # 1 0 0
    # 0 0 0

    siatka = [[0 for x in range(rozmiar_planszy)] for y in range(rozmiar_planszy)]

    if args.przypadek:
        ustawienie_przypadku(siatka, args.przypadek, rozmiar_planszy)

    screen = pygame.display.set_mode((wielkosc_komorki * rozmiar_planszy,
                                      wielkosc_komorki * rozmiar_planszy + offset))
    clock = pygame.time.Clock()

    pauza = True
    count = 0

    while True:

        # zarządzanie eventami z pygame
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            # obsługa zatrzymywania gry spacją
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pauza = not pauza

            # obsługa wybierania komórek myszką
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pauza:
                    if event.button == 1:
                        x, y = event.pos
                        y -= offset  # korekta Y przez UI

                        x = math.floor(x / wielkosc_komorki)
                        y = math.floor(y / wielkosc_komorki)

                        if 0 <= x < rozmiar_planszy and 0 <= y < rozmiar_planszy:
                            siatka[x][y] = (siatka[x][y] + 1) % 2

        # Sekcja logiki
        #############################################

        temp_siatka = copy.deepcopy(siatka)
        # kopiujemy siatkę, żeby zmiany nie wpływały na bieżące obliczenia sąsiadów

        # sterowanie szybkością symulacji niezależnie od FPS
        if (szybkosc * count) % fps == 0:
            count = 0
            if not pauza:
                for x in range(rozmiar_planszy):
                    for y in range(rozmiar_planszy):
                        sasiedzi = liczba_zywych_sasiadow(temp_siatka, x, y, rozmiar_planszy)

                        if temp_siatka[x][y] == 1:  # jesli żyje
                            # umiera przy samotności lub przeludnieniu
                            if sasiedzi < 2 or sasiedzi > 3:
                                siatka[x][y] = 0
                        else:  # jeśli jest martwa
                            # rodzi się dokładnie przy 3 sąsiadach
                            if sasiedzi == 3:
                                siatka[x][y] = 1

        #############################################

        # Sekcja renderowania grafiki
        ##############################################

        # rysowanie białej pustej planszy
        screen.fill("white")
        pygame.draw.rect(screen, "black", pygame.Rect(0, offset - 1,
                                                      wielkosc_komorki * rozmiar_planszy, 1))

        # rysowanie tekstu nad planszą
        pygame.font.init()
        my_font = pygame.font.SysFont('Arial', offset // 3)

        if pauza:
            text1 = my_font.render('Gra zapuazowana (można zmieniać komórki)', False, (0, 0, 0))
            text2 = my_font.render('Naciśnij spacje aby wznowić', False, (0, 0, 0))
        else:
            text1 = my_font.render('Naciśnij spacje aby zapauzować gre', False, (0, 0, 0))
            text2 = my_font.render('i móc zmieniać komórki', False, (0, 0, 0))

        screen.blit(text1, (10, 5))
        screen.blit(text2, (10, offset // 2))

        # rysownie komórek na planszy
        for x in range(rozmiar_planszy):
            for y in range(rozmiar_planszy):
                if siatka[x][y] == 1:
                    pygame.draw.rect(screen, "black",
                                     pygame.Rect(x * wielkosc_komorki,
                                                 y * wielkosc_komorki + offset,
                                                 wielkosc_komorki, wielkosc_komorki))

        mX, mY = pygame.mouse.get_pos()
        mY -= offset

        mX = math.floor(mX / wielkosc_komorki)
        mY = math.floor(mY / wielkosc_komorki)

        if pauza and 0 <= mX < rozmiar_planszy and 0 <= mY < rozmiar_planszy:
            # wizualny podgląd komórki pod kursorem
            if siatka[mX][mY] == 0:
                pygame.draw.rect(screen, pygame.Color(230, 230, 230),
                                 pygame.Rect(mX * wielkosc_komorki,
                                             mY * wielkosc_komorki + offset,
                                             wielkosc_komorki, wielkosc_komorki))
            else:
                pygame.draw.rect(screen, pygame.Color(89, 89, 89),
                                 pygame.Rect(mX * wielkosc_komorki,
                                             mY * wielkosc_komorki + offset,
                                             wielkosc_komorki, wielkosc_komorki))

        pygame.display.flip()

        ##############################################

        count += 1
        clock.tick(fps)


main()
