import random
import logging
from logging.handlers import TimedRotatingFileHandler
from Database_connection import MysqlDB
from datetime import datetime

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

rounds = 1
tie_count = 0  # total count of tie in the game
win_count = 0  # total count of win in the game
lose_count = 0  # total count of lose in th game
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


player_name = input("Enter your name: ")  # Getting the player's name

while True:
    try:
        player = int(input("Enter your choice number (rock(1) /paper(2) / scissors(3) ) : "))  # player's choice
        check_player_choice(player)  # Checking the player's choice

        computer = random.choice(choices)

        print(f"{player_name} chose {player} and computer chose {computer}.")

        # find the winner of the game
        status = find_winner(player, computer)

        # Condition to count the win, lose and tie
        if status == "win":
            win_count += 1
        elif status == "lose":
            lose_count += 1
        else:
            tie_count += 1

        continue_play = input("Want to play again? (y/n): ")
        if continue_play.lower() != "y":
            print("Thank you for playing")
            logger.info("End of the game")
            break

        rounds += 1  # counting the no of rounds the player has played

    except ValueError:
        error_message = "Sorry, You entered text instead of a number. Please enter a number between 1 and 3"
        logger.error(error_message)
        print(error_message)

    except IndexError:
        error_message = "Sorry, you entered an incorrect number. Please enter a number between 1 and 3"
        logger.error(error_message)
        print(error_message)

    except BaseException as e:
        error_message = "An error occurred"
        print(error_message)
        logger.error(error_message)

# Inserting the records into the database
try:
    insert_data = [player_name, date, time, rounds, win_count, lose_count, tie_count]
    logger.info("Inserting data into database")
    if insert_data:
        con = MysqlDB.getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO RPS_INFO (PLAYER_NAME,PLAY_DATE,PLAY_TIME,NO_OF_ROUNDS,NO_OF_WIN,NO_OF_LOSE,"
                    "NO_OF_TIE) VALUES (%s,%s,%s,%s,%s,%s,%s)", insert_data)
        con.commit()
        con.close()

        logger.info("Data inserted successfully")


except Exception as e:
    logger.error('An error occurred: %s', str(e))
    print(e, 'An ERROR occurred in table INSERT Method')
