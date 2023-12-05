import random
import logging
from logging.handlers import TimedRotatingFileHandler
from Database_connection import MysqlDB
from datetime import datetime
import sys

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(funcName)s : %(lineno)d : %(message)s',
    handlers=[
        logging.handlers.TimedRotatingFileHandler(
            filename=r"runtime_log.log",
            when="D",
            interval=1,
            backupCount=0,
        )
    ]
)

rock = 1
paper = 2
scissors = 3

choices = [rock, paper, scissors]  # List of the choices of the game

date = datetime.now().strftime('%Y-%m-%d')  # date the player plays
time = datetime.now().strftime('%H:%M:%S')  # time the player plays


def check_player_choice(n):  # Validation of player's choice
    if n not in choices:
        raise IndexError


def find_winner(player_choice, computer_choice):  # Conditions to find the winner of the game
    if player_choice == computer_choice:
        print("Both players chose same. It is a tie.")
        logger.info("It is a tie")
        return "tie"

    elif player_choice == rock:
        if computer_choice == scissors:
            print("Rock smashes scissors! You win!")
            logger.info("Player won")
            return "win"
        else:
            print("Paper covers rock! You lose.")
            logger.info("Computer won")
            return "lose"
    elif player_choice == paper:
        if computer_choice == rock:
            print("Paper covers rock! You win!")
            logger.info("Player won")
            return "win"
        else:
            print("Scissors cuts paper! You lose.")
            logger.info("Computer won")
            return "lose"
    elif player_choice == scissors:
        if computer_choice == paper:
            print("Scissors cuts paper! You win!")
            logger.info("Player won")
            return "win"
        else:
            print("Rock smashes scissors! You lose.")
            logger.info("Computer won")
            return "lose"
    else:
        print("That's not a valid play. Check your choice!")
        logger.error("That's not a valid play. Check your choice!")


def Game(p_name):
    tie_count = 0  # total count of tie in the game
    win_count = 0  # total count of win in the game
    lose_count = 0  # total count of lose in th game

    rounds = int(input("Enter the rounds you want to play: "))  # rounds of the game

    for i in range(1, rounds + 1):
        try:
            player = int(input("Enter your choice number (rock(1) /paper(2) / scissors(3) ) : "))  # player's choice
            check_player_choice(player)  # Checking the player's choice

            computer = random.choice(choices)

            print(f"{p_name} chose {player} and computer chose {computer}.")

            # find the winner of the game
            status = find_winner(player, computer)

            # Condition to count the win, lose and tie
            if status == "win":
                win_count += 1
            elif status == "lose":
                lose_count += 1
            else:
                tie_count += 1

        except ValueError:
            error_message = "Sorry, You entered text instead of a number. Please enter a number between 1 and 3"
            logger.error(error_message)
            print(error_message)

        except IndexError:
            error_message = "Sorry, you entered an incorrect number. Please enter a number between 1 and 3"
            logger.error(error_message)
            print(error_message)

        except BaseException:
            error_message = "An error occurred"
            print(error_message)
            logger.error(error_message)

    print('Thank you for playing')

    continue_play = input("Want to play again? (y/n): ")
    if continue_play.lower() == "y":
        new_results = Game(p_name)
        logger.info('Player want to play again')
        rounds = rounds + new_results[0]
        win_count = win_count + new_results[1]
        lose_count = lose_count + new_results[2]
        tie_count = tie_count + new_results[3]
    else:
        print("Thank you for playing ")
        logger.info("End of the game")

    return [rounds, win_count, lose_count, tie_count]


# Starting the game
try:
    print('Welcome to the Rock,Paper,Scissors Game')

    player_name = input("Enter your name: ")  # Getting the player's name
    results = Game(player_name)

    # Inserting the records into the database
    insert_data = [player_name, date, time, results[0], results[1], results[2], results[3]]
    logger.info("Inserting data into database")
    if insert_data:
        con = MysqlDB.getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO RPS_INFO (PLAYER_NAME,PLAY_DATE,PLAY_TIME,NO_OF_ROUNDS,NO_OF_WIN,NO_OF_LOSE,"
                    "NO_OF_TIE) VALUES (%s,%s,%s,%s,%s,%s,%s)", insert_data)
        con.commit()
        con.close()

        logger.info("Data inserted successfully")
        input("Press Enter to close the game")


except Exception as e:
    logger.error('An error occurred: %s', str(e))
    print(e, 'An ERROR occurred in table INSERT Method')
