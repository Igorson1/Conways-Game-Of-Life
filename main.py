import math
import pygame
import copy

def liczba_zywych_sasiadow(siatka, x, y, rozmiar):
    """
    funkcja sprawdza 8 sąsiednich komórek dla komórki (x; y) - zwraca liczbę żywych
    funkcja nie sprawdza pól poza granicą siatki
    """
    suma = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue # bez uwzględniania aktualnie sprawdzanej komórki
            
            nx, ny = x + i, y + j
            
            # warunek żeby nie wyjść poza listę
            if 0 <= nx < rozmiar and 0 <= ny < rozmiar:
                suma += siatka[nx][ny]
    return suma

def main():

    pygame.init()
    fps = 100

    szybkosc = 4 # najlepiej od 1 - 10, tak można też zrobić że użytkownik podaje w argumencie szybkosc od 1 do 10

    wielkosc_komorki = 10
    rozmiar_planszy = 50 # rozmiar planszy (szerokośc i wysokość w komórkach) też może być do ustawienia przez użytkownika

    offset = math.floor(1.4 * rozmiar_planszy)

    # Tworzenie siatki
    # Przykład pustej siadki 3x3, 0 odpowiada białej komórce, a 1 czarnej.
    # Na tej siatkce czarna komórka ma kordynaty [0][1]

    # 0 0 0
    # 1 0 0
    # 0 0 0

    siatka = [[0 for x in range(rozmiar_planszy)] for y in range(rozmiar_planszy)]
    
    #przykladowy przypadek:
    #siatka[27][27] = 1
    #siatka[26][27] = 1
    #siatka[25][27] = 1

    screen = pygame.display.set_mode((wielkosc_komorki*rozmiar_planszy,wielkosc_komorki*rozmiar_planszy + offset))
    clock = pygame.time.Clock()

    pauza = False

    count = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pauza = not pauza
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pauza:
                    if event.button == 1:
                        x, y = event.pos
                        y -= offset
                        
                        x = math.floor(x/wielkosc_komorki)
                        y = math.floor(y/wielkosc_komorki)


                        if 0 <= x < rozmiar_planszy and 0 <= y < rozmiar_planszy:
                            siatka[x][y] = (siatka[x][y] + 1) % 2

        
        # Sekcja logiki

        #############################################


        temp_siatka = copy.deepcopy(siatka)

        # przejście przez każdą komórkę i zadecydowanie czy żyje czy jest martwa

        if (szybkosc*count) % fps == 0:
            count = 0
            if not pauza:
                for x in range(rozmiar_planszy):
                    for y in range(rozmiar_planszy):
                        sasiedzi = liczba_zywych_sasiadow(siatka, x, y, rozmiar_planszy)

                        if siatka[x][y] == 1: # jesli żyje
                            if sasiedzi < 2 or sasiedzi > 3:
                                temp_siatka[x][y] = 0 # umiera gdy ma mniej niż 2 i więcej niż 3 sąsiadów
                        else: # jeśli jest martwa
                            if sasiedzi == 3:
                                temp_siatka[x][y] = 1 # rodzi się dla 3 sąsiadów

        # nadpisanie starej siatki nową
        siatka = copy.deepcopy(temp_siatka)


        #############################################



        # Sekcja renderowania grafiki
        ##############################################

        screen.fill("white")

        pygame.draw.rect(screen, "black", pygame.Rect(0, offset - 1, wielkosc_komorki*rozmiar_planszy, 1))

        pygame.font.init()
        my_font = pygame.font.SysFont('Arial', 30 * rozmiar_planszy // 50)

        if pauza:
            text1 = my_font.render('Gra zapuazowana (można zmieniać komórki)', False, (0, 0, 0))
            text2 = my_font.render('Naciśnij spacje aby wznowić', False, (0, 0, 0))
        else:
            text1 = my_font.render('Naciśnij spacje aby zapauzować gre', False, (0, 0, 0))
            text2 = my_font.render('i móc zmieniać komórki', False, (0, 0, 0))

        screen.blit(text1, (3,0))
        screen.blit(text2, (3,30 * rozmiar_planszy // 50))


        for x in range(rozmiar_planszy):
            for y in range(rozmiar_planszy):
                if siatka[x][y] == 1:
                    pygame.draw.rect(screen, "black", pygame.Rect(x*wielkosc_komorki, y*wielkosc_komorki + offset, wielkosc_komorki, wielkosc_komorki))

        mX, mY = pygame.mouse.get_pos()

        mY = mY - offset

        #print(offset)
        #print(mX, mYSiatka)

        mX = math.floor(mX/wielkosc_komorki)
        mY = math.floor(mY/wielkosc_komorki)


        if pauza and 0 <= mX < rozmiar_planszy and 0 <= mY < rozmiar_planszy:
            print(mX, mY)

            if siatka[mX][mY] == 0:
                pygame.draw.rect(screen, pygame.Color(230, 230, 230),
                                 pygame.Rect(mX * wielkosc_komorki, mY * wielkosc_komorki + offset, wielkosc_komorki, wielkosc_komorki))
            else:
                pygame.draw.rect(screen, pygame.Color(89, 89, 89),
                                 pygame.Rect(mX * wielkosc_komorki, mY * wielkosc_komorki + offset, wielkosc_komorki, wielkosc_komorki))
                
        pygame.display.flip()  # Refresh on-screen display

        ##############################################
        count += 1
        clock.tick(fps)
main()
