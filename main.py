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

    wielkosc_komorki = 10
    rozmiar_planszy = 50

    # Tworzenie siatki
    # Przykład pustej siadki 3x3, 0 odpowiada białej komórce, a 1 czarnej.
    # Na tej siatkce czarna komórka ma kordynaty [0][1]

    # 0 0 0
    # 1 0 0
    # 0 0 0

    siatka = [[0 for x in range(rozmiar_planszy)] for y in range(rozmiar_planszy)]
    
    #przykladowy przypadek:
    siatka[27][27] = 1
    siatka[26][27] = 1
    siatka[25][27] = 1

    screen = pygame.display.set_mode((wielkosc_komorki*rozmiar_planszy,wielkosc_komorki*rozmiar_planszy))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        
        # Sekcja logiki

        #############################################


        temp_siatka = copy.deepcopy(siatka)

        # przejście przez każdą komórkę i zadecydowanie czy żyje czy jest martwa
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

        for x in range(rozmiar_planszy):
            for y in range(rozmiar_planszy):
                if siatka[x][y] == 1:
                    pygame.draw.rect(screen, "black", pygame.Rect(x*wielkosc_komorki, y*wielkosc_komorki, wielkosc_komorki, wielkosc_komorki))


        pygame.display.flip()  # Refresh on-screen display

        ##############################################

        clock.tick(5)         # wait until next frame (at 60 FPS
main()
