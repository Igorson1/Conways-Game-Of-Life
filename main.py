import pygame
import copy

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
    siatka[27][27] = 1


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

        #tu pisz logike programu

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

        clock.tick(30)         # wait until next frame (at 60 FPS
main()
