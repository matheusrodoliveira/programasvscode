#Embaralhar as cartas
import random

jogando = False
chip_pool = 100

bet = 1

restart_phrase = "\n\nPressione 'd' para embaralhar novamente ou pressione 'q' para sair."

naipes = ('H', 'D', 'C', 'S')
cartas = ('A', '2', '3', '4', '5', '6', '7', '8','9', '10', 'J', 'Q', 'K')

valor_cartas = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

#Classe das cartas
class Card:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor
        
    def __str__(self):
        return self.naipe + self.valor
    
    
    def tipo_carta(self):
        print (self.naipe + self.valor)
    
    def draw(self):
        return self.naipe + self.valor

#Classe da Mão
class Mão:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.às = False
    
    def __str__(self):
        mao_comp = ""
        
        for card in self.cards:
            nome_carta = card.__str__()
            mao_comp += " " + nome_carta
        
        return "Na mão temos {}".format(mao_comp)
    
    def adicionar_carta(self, card):
        self.cards.append(card)
        
        if card.valor=='A':
            self.às = True
        self.value += valor_cartas[card.valor]
    
    def calc_val(self):
        if (self.às == 'True' and self.value < 12):
            return self.value + 10
        else:
            return self.value
    
    def draw(self, hidden):
        if hidden == True and jogando == True:
            starting_card = 1
        else:
            starting_card = 0
        for x in range(starting_card, len(self.cards)):
            self.cards[x].draw()

class Deck:
    
    def __init__(self):
        self.deck = []
        
        for naipe in naipes:
            for carta in cartas:
                self.deck.append(Card(naipe, carta))
        
    def embaralhar(self):
        random.shuffle(self.deck)

    def entregar(self):
        return self.deck.pop()

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += " " + card.__str__()

        return "\nO deck tem " + deck_comp


def fazer_bet():
    global bet
    bet = 0
    
    print("\nQue quantidade de fichas você gostaria de apostar? (Digite um inteiro por favor)")
    
    while bet == 0:
        bet_comp = input()
        bet_comp = int(bet_comp)
        
        if bet_comp >= 1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            print("\nAposta inválida. Você tem apenas " + str(chip_pool) + " fichas restantes.")


def entregar_cartas():
    global resultado, jogando, deck, mao_jogador, mao_dealer, chip_pool, bet
    
    deck = Deck()
    deck.embaralhar()
    
    fazer_bet()
    
    mao_jogador = Mão()
    mao_dealer = Mão()
    
    # 2 Cartas para o Jogador
    mao_jogador.adicionar_carta(deck.entregar())
    mao_jogador.adicionar_carta(deck.entregar())
    
     # 2 Cartas para o Dealer
    mao_dealer.adicionar_carta(deck.entregar())
    mao_dealer.adicionar_carta(deck.entregar())
    
    resultado = "\nParar ou permanecer? Pressione 'h' or 's':"
        
    jogando = True
    game_step() 


def bater():
    
    global jogando, chip_pool, deck, mao_jogador, mao_dealer, resultado, bet
    
    if jogando:
        if mao_jogador.calc_val() <= 21:
            mao_jogador.adicionar_carta(deck.entregar())
        print("\nA mão do jogador é %s" %mao_jogador)
        
        if mao_jogador.calc_val() >= 21:
            resultado = "\nPego! " + restart_phrase
            chip_pool -= bet
            jogando = False
        
    else:
        resultado = "\nDesculpa, mas vc não pode bater! " + restart_phrase
    
    game_step()



def permanecer():
    global jogando, chip_pool, deck, mao_jogador, mao_dealer, resultado, bet
    
    if jogando == False:
        if mao_jogador.calc_val() > 0:
            resultado = "Desculpa, você não pode permanecer!"
    
    else:
        while mao_dealer.calc_val() < 17:
            mao_dealer.adicionar_carta(deck.entregar())
            
        if mao_dealer.calc_val() > 21:
            resultado = "\nDealer ultrapassou a soma 21 ! Você venceu! " + restart_phrase
            chip_pool += bet
            jogando = False
        
        elif mao_dealer.calc_val() < mao_jogador.calc_val():
            resultado = "\nYou bet the dealer! Você venceu! " + restart_phrase
            chip_pool += bet
            jogando = False
            
        elif mao_dealer.calc_val() == mao_jogador.calc_val():
            resultado = "\nEmpatado! " + restart_phrase
            jogando = False
        
        else:
            resultado = '\nDealer venceu! ' + restart_phrase
            chip_pool -= bet
            jogando = False
    game_step()


def game_step():
    print("")
    print("A mão do jogador é:")
    mao_jogador.draw(hidden = False)
    print(" A soma total do jogador é: " + str(mao_jogador.calc_val()))
    
    print("")
    print("A mão do dealer é:")
    mao_dealer.draw(hidden = True)
    print("A soma total do dealer é: " + str(mao_dealer.calc_val()))
    
    if jogando == False:
        print("Saldo: "+str(chip_pool))
    
    print(resultado)
    
    player_input()  




def game_exit():
    print("\nObrigado por estar jogando!")
    exit()



def player_input():
    plin = input().lower()
    
    if plin  == 'h':
        bater()
    elif plin  == 's':
        permanecer()
    elif plin  == 'd':
        entregar_cartas()
    elif plin  == 'q':
        game_exit()
    else:
        print("\nEntrada inválida... Digite h, s, d or q: ")
        player_input()



def intro():
    frase_efeito = '''Bem-vindo ao BlackJack! Chegue o mais perto possível de 21 sem ultrapassar!
    \nO dealer acerta até chegar a 17. Às contam como 1 ou 11.
    \nA saída do cartão vai uma letra seguida por um número de notação de face'''
    print(frase_efeito)


deck = Deck()
deck.embaralhar()

mao_jogador = Mão()
mao_dealer = Mão()

intro()
entregar_cartas()