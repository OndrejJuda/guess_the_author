import requests
from bs4 import BeautifulSoup
from random import choice
from csv import writer, reader
from datetime import date
from time import sleep


"""
Rozdělit na dva soubory, get_quotes a ulož do csv. Přidat datum uložení a pokaždé, když by aktuální datum bylo o 7 dní starší,
tak by se znovu aktualizovalo.
"""


# score part
def write_score(win, loose):
    with open('guess_the_author_score.csv', 'a') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow([date.today(), win, loose])


def read_score():
    with open('guess_the_author_score.csv') as csv_file:
        csv_reader = reader(csv_file)
        for row in csv_reader:
            if row:
                print(f'Date: {row[0]}. Wins: {row[1]}. Losses: {row[2]}')


def get_high_score():
    with open('guess_the_author_score.csv') as csv_file:
        csv_reader = reader(csv_file)
        high_score = [0, 0, 0]
        for row in csv_reader:
            if row:
                if int(row[1]) > int(high_score[1]):
                    high_score = row
        print(f'YOUR HIGH SCORE - Date: {high_score[0]}. Wins: {high_score[1]}. Losses: {high_score[2]}')


# scrapping part
def get_author_data(href):
    # method gets url to authors bio and returns info about them
    resp = requests.get('http://quotes.toscrape.com'+href)
    soup = BeautifulSoup(resp.text, 'html.parser')
    born_date = soup.find(class_='author-born-date').get_text()
    born_location = soup.find(class_='author-born-location').get_text()
    return f'Author was born on {born_date} {born_location}.'


def get_quotes():
    # returns list of all quotes and their data
    quotes_list = []
    base_url = 'http://quotes.toscrape.com'
    url = '/page/1'

    # while there is reference for next button, loop
    while url:
        # setting up soup
        response = requests.get(f'{base_url}{url}')
        soup = BeautifulSoup(response.text, 'html.parser')

        # getting list of quotes
        quotes = soup.find_all(class_='quote')

        # creating list of quotes
        for quote in quotes:
            quotes_list.append(
                {
                    'text': quote.find(class_='text').get_text(),
                    'author': quote.find(class_='author').get_text(),
                    'href': quote.find('a')['href']
                }
            )
        next_button = soup.find(class_='next')
        url = next_button.find('a')['href'] if next_button else None
        # sleep(2)  # not to get caught
    return quotes_list


# game part
def game_mechanics():
    # choose random list from get_quotes and works with the further
    chance = 3
    quote = choice(get_quotes())
    while chance > 0:
        if chance == 3:
            print(quote['text'])
        elif chance == 2:
            hint = input('Do you wanna hint? \nHit enter if no. Write anything if yes.')
            if hint:
                print(get_author_data(quote['href']))
        user_guess = input(f'Who said this? Guess {chance} times: ')
        if user_guess == quote['author']:
            print('You\'re right!')
            return 1, 0
        else:
            print('Wrong guess...')
            # print(f'the answer is {quote[1]}')
        chance -= 1
        if chance == 0:
            print(f'The answer is {quote["author"]}')
            return 0, 1


def quit_game():
    print("\nSee you next time")
    quit()


def game():
    switcher = {
        'p': game_loop,
        's': read_score,
        'h': get_high_score,
        'q': quit_game
    }
    allowed_input = ('p', 's', 'h', 'q')
    print('Welcome to the game of Guess the author.'
          '\nI will print a quote and you have to guess who said/wrote it.'
          '\nYou have 3 chances to guess the author.'
          '\nWish you good luck!')
    while True:
        player_input = input('\nWrite one of the followings:'
                             '\nPlay the game. (p)'
                             '\nShow the score. (s)'
                             '\nShow the high score (h)'
                             '\nQuit the game. (q)'
                             '\nWrite down your choice: ')
        if player_input in allowed_input:
            func = switcher.get(player_input)
            func()
        else:
            print('Wrong input. Try again.')


def game_loop():
    wins = 0
    losses = 0
    while True:
        win, loss = game_mechanics()
        wins += win
        losses += loss
        cont = input('Do you wanna continue? (y/n): ')
        if cont.lower() == 'n':
            print('See you again.')
            write_score(wins, losses)
            break
        elif cont.lower() != 'y':
            print('Wrong input... shutting down!')
            write_score(0, 0)
            quit()


game()



