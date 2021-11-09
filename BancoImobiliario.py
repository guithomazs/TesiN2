# casas = 20.
# saldo inicial = 300 (100 ao completar a volta).
# 4 jogadores, impulsivo, exigente, cauteloso, aleatório.
# 1000 rodadas acaba, maior saldo, desempate é a ordem de jogada.
# 4x{saldos}; 4x{n° jogador}; {numero de players positivos}; {numero de rodadas}; 4x{posição}
# {partidas timeout}; {media de turnos por partida}; {porcentagem de vitórias de cada jogador};
# {comportamento q mais vence}
from random import randint, seed
from config import *


# seed(381283491023813121)

casas = [
    [
        randint(*range_valor_venda),
        randint(*range_valor_aluguel),
        DISPONIVEL
    ] for i in range(qtd_casas)
]

jogadores = [
    [
        0, valor_inicial_jogadores
    ] for i in range(qtd_jogadores)
]

vitórias = [0 for i in range(4)]
vitórias[0] = 0
vitórias[1] = 0
vitórias[2] = 0
vitórias[3] = 0

jogoFinalizado = 0

for JOGOS in range(0, 300):
    RODADAS = 0
    print(JOGOS + 1)
    POSITIVOS = 4
    jogadores[jog1][Saldo] = 300
    jogadores[jog2][Saldo] = 300
    jogadores[jog3][Saldo] = 300
    jogadores[jog4][Saldo] = 300
    CasasPlayer1 = 0
    CasasPlayer2 = 0
    CasasPlayer3 = 0
    CasasPlayer4 = 0

    while POSITIVOS > 1:
        if jogadores[jog1][Saldo] > 0:
            numero_dado = randint(1, 6)
            jogadores[jog1][POSIÇÃO] += numero_dado

            if jogadores[jog1][POSIÇÃO] >= 20:
                jogadores[jog1][POSIÇÃO] -= 20
                jogadores[jog1][Saldo] += 100

            if casas[jogadores[jog1][POSIÇÃO]][disponivel] == 0:
                if jogadores[jog1][Saldo] > casas[jogadores[jog1][POSIÇÃO]][vvenda]:
                    jogadores[jog1][Saldo] -= casas[jogadores[jog1][POSIÇÃO]][0]
                    casas[jogadores[jog1][POSIÇÃO]][disponivel] = 1

            elif casas[jogadores[jog1][POSIÇÃO]][disponivel] == 2:
                jogadores[jog1][Saldo] -= casas[jogadores[jog1][POSIÇÃO]][valuguel]
                jogadores[jog2][Saldo] += casas[jogadores[jog1][POSIÇÃO]][valuguel]

            elif casas[jogadores[jog1][POSIÇÃO]][disponivel] == 3:
                jogadores[jog1][Saldo] -= casas[jogadores[jog1][POSIÇÃO]][valuguel]
                jogadores[jog3][Saldo] += casas[jogadores[jog1][POSIÇÃO]][valuguel]

            elif casas[jogadores[jog1][POSIÇÃO]][disponivel] == 4:
                jogadores[jog1][Saldo] -= casas[jogadores[jog1][POSIÇÃO]][valuguel]
                jogadores[jog4][Saldo] += casas[jogadores[jog1][POSIÇÃO]][valuguel]
            if jogadores[jog1][Saldo] <= 0:
                POSITIVOS -= 1
                for i in range(20):
                    if casas[i][disponivel] == 1:
                        casas[i][disponivel] = 0
            RODADAS += 1
            if RODADAS >= 1000:
                timeout += 1
                break
# -------------------------------------------------------------------------------------------------------------------
        if jogadores[jog2][Saldo] > 0:
            numero_dado = randint(1, 6)
            jogadores[jog2][POSIÇÃO] += numero_dado

            if jogadores[jog2][POSIÇÃO] >= 20:
                jogadores[jog2][POSIÇÃO] -= 20
                jogadores[jog2][Saldo] += 100

            if casas[jogadores[jog2][POSIÇÃO]][disponivel] == 0:
                if casas[jogadores[jog2][POSIÇÃO]][valuguel] > 50:
                    if jogadores[jog2][Saldo] > casas[jogadores[jog2][POSIÇÃO]][vvenda]:
                        jogadores[jog2][Saldo] -= casas[jogadores[jog2][POSIÇÃO]][vvenda]
                        casas[jogadores[jog2][POSIÇÃO]][disponivel] = 2

            elif casas[jogadores[jog2][POSIÇÃO]][disponivel] == 1:
                jogadores[jog2][Saldo] -= casas[jogadores[jog2][POSIÇÃO]][valuguel]
                jogadores[jog1][Saldo] += casas[jogadores[jog2][POSIÇÃO]][valuguel]

            elif casas[jogadores[jog2][POSIÇÃO]][disponivel] == 3:
                jogadores[jog2][Saldo] -= casas[jogadores[jog2][POSIÇÃO]][valuguel]
                jogadores[jog3][Saldo] += casas[jogadores[jog2][POSIÇÃO]][valuguel]

            elif casas[jogadores[jog2][POSIÇÃO]][disponivel] == 4:
                jogadores[jog2][Saldo] -= casas[jogadores[jog2][POSIÇÃO]][valuguel]
                jogadores[jog4][Saldo] += casas[jogadores[jog2][POSIÇÃO]][valuguel]

            if jogadores[jog2][Saldo] <= 0:
                POSITIVOS -= 1
                for i in range(20):
                    if casas[i][disponivel] == 2:
                        casas[i][disponivel] = 0
            RODADAS += 1
            if RODADAS >= 1000:
                timeout += 1
                break
# --------------------------------------------------------------------------------------------------------------------
        if jogadores[jog3][Saldo] > 0:
            numero_dado = randint(1, 6)
            jogadores[jog3][POSIÇÃO] += numero_dado

            if jogadores[jog3][POSIÇÃO] >= 20:
                jogadores[jog3][POSIÇÃO] -= 20
                jogadores[jog3][Saldo] += 100

            if casas[jogadores[jog3][POSIÇÃO]][disponivel] == 0:
                if jogadores[jog3][Saldo] - casas[jogadores[jog3][POSIÇÃO]][vvenda] >= 80:
                    if jogadores[jog3][Saldo] > casas[jogadores[jog3][POSIÇÃO]][vvenda]:
                        jogadores[jog3][Saldo] -= casas[jogadores[jog3][POSIÇÃO]][vvenda]
                        casas[jogadores[jog3][POSIÇÃO]][disponivel] = 3

            elif casas[jogadores[jog3][POSIÇÃO]][disponivel] == 1:
                jogadores[jog3][Saldo] -= casas[jogadores[jog3][POSIÇÃO]][valuguel]
                jogadores[jog1][Saldo] += casas[jogadores[jog3][POSIÇÃO]][valuguel]

            elif casas[jogadores[jog3][POSIÇÃO]][disponivel] == 2:
                jogadores[jog3][Saldo] -= casas[jogadores[jog3][POSIÇÃO]][valuguel]
                jogadores[jog2][Saldo] += casas[jogadores[jog3][POSIÇÃO]][valuguel]

            elif casas[jogadores[jog3][POSIÇÃO]][disponivel] == 4:
                jogadores[jog3][Saldo] -= casas[jogadores[jog3][POSIÇÃO]][valuguel]
                jogadores[jog4][Saldo] += casas[jogadores[jog3][POSIÇÃO]][valuguel]

            if jogadores[jog3][Saldo] <= 0:
                POSITIVOS -= 1
                for i in range(20):
                    if casas[i][disponivel] == 3:
                        casas[i][disponivel] = 0
            RODADAS += 1
            if RODADAS >= 1000:
                timeout += 1
                break
# --------------------------------------------------------------------------------------------------------------------
        if jogadores[jog4][Saldo] > 0:
            numero_dado = randint(1, 6)
            jogadores[jog4][POSIÇÃO] += numero_dado

            if jogadores[jog4][POSIÇÃO] >= 20:
                jogadores[jog4][POSIÇÃO] -= 20
                jogadores[jog4][Saldo] += 100

            if casas[jogadores[jog4][POSIÇÃO]][disponivel] == 0:
                if jogadores[jog4][Saldo] > casas[jogadores[jog4][POSIÇÃO]][vvenda]:
                    CHANCE = randint(1, 2)
                    if CHANCE == 1:
                        jogadores[jog4][Saldo] -= casas[jogadores[jog4][POSIÇÃO]][vvenda]
                        casas[jogadores[jog4][POSIÇÃO]][disponivel] = 4

            elif casas[jogadores[jog4][POSIÇÃO]][disponivel] == 1:
                jogadores[jog4][Saldo] -= casas[jogadores[jog4][POSIÇÃO]][valuguel]
                jogadores[jog1][Saldo] += casas[jogadores[jog4][POSIÇÃO]][valuguel]

            elif casas[jogadores[jog4][POSIÇÃO]][disponivel] == 2:
                jogadores[jog4][Saldo] -= casas[jogadores[jog4][POSIÇÃO]][valuguel]
                jogadores[jog2][Saldo] += casas[jogadores[jog4][POSIÇÃO]][valuguel]

            elif casas[jogadores[jog4][POSIÇÃO]][disponivel] == 3:
                jogadores[jog4][Saldo] -= casas[jogadores[jog4][POSIÇÃO]][valuguel]
                jogadores[jog3][Saldo] += casas[jogadores[jog4][POSIÇÃO]][valuguel]

            if jogadores[jog4][Saldo] <= 0:
                POSITIVOS -= 1
                for i in range(20):
                    if casas[i][disponivel] == 4:
                        casas[i][disponivel] = 0
            RODADAS += 1
            if RODADAS >= 1000:
                timeout += 1
                break
# --------------------------------------------------------------------------------------------------------------------
    if RODADAS < 1000:
        for i in range(4):
            if jogadores[i][Saldo] > 0:
                vitórias[i] += 1
    else:
        for i in range(20):
            jogoFinalizado += 1
            if casas[i][disponivel] == 1:
                CasasPlayer1 += 1
            elif casas[i][disponivel] == 2:
                CasasPlayer2 += 1
            elif casas[i][disponivel] == 3:
                CasasPlayer3 += 1
            elif casas[i][disponivel] == 4:
                CasasPlayer4 += 1
        if CasasPlayer1 >= CasasPlayer2 and CasasPlayer1 >= CasasPlayer3 and CasasPlayer1 >= CasasPlayer4:
            vitórias[0] += 1
        elif CasasPlayer2 >= CasasPlayer3 and CasasPlayer2 >= CasasPlayer4:
            vitórias[1] += 1
        elif CasasPlayer3 >= CasasPlayer4:
            vitórias[2] += 1
        else:
            vitórias[3] += 1

    media += RODADAS

print("Timeout = ", timeout)

for i in range(4):
    for j in range(4):
        if vitórias[i] > vitórias[j]:
            maior = i

nome = ["nenhum", "impulsivo", "exigente", "cauteloso", "aleatório"]

print("Maior número de vitórias: Jogador", nome[maior + 1])

media = media/300

print("Rodadas por jogo em media: ", media)

porcentagemPlayer1 = vitórias[0]*100 / 300
porcentagemPlayer2 = vitórias[1]*100 / 300
porcentagemPlayer3 = vitórias[2]*100 / 300
porcentagemPlayer4 = vitórias[3]*100 / 300

print("% de vitória do jogador", nome[1], porcentagemPlayer1, "%")
print("% de vitória do jogador", nome[2], porcentagemPlayer2, "%")
print("% de vitória do jogador", nome[3], porcentagemPlayer3, "%")
print("% de vitória do jogador", nome[4], porcentagemPlayer4, "%")
