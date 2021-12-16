import random
import socket
from _thread import *
import sys
import threading

n = -1
resp_sender = -1
minimum = sys.maxsize
sender = 0
guesser = 0
lock_for_number = threading.Lock()
lock_for_answer = threading.Lock()
lock_for_minim = threading.Lock()
lock_guesser = threading.Lock()
lock_sender = threading.Lock()


def validation_answer(answer, number):
    if answer < number:
        message = 'Wrong! The number is greater\n'
        won_round = 0
    elif answer > number:
        message = 'Wrong! The number is lesser\n'
        won_round = 0
    else:
        message = 'Correct! Number guessed!\n'
        won_round = 1
    return message, won_round


def get_random_number():
    number = random.randint(0, 50)
    return number


def multi_threaded_client(connection):
    connection.sendall(str.encode('<<< Welcome To Guess The Number ! >>>\n1.Guess The Number Single Player\n2.Guess '
                                  'the Number Multiplayer\n'))
    game_type = connection.recv(2048).decode('utf-8')
    global n
    global resp_sender
    global minimum
    global sender
    global guesser
    global lock_for_number
    global lock_for_answer
    global lock_guesser
    global lock_sender
    global lock_for_minim
    if game_type == '1':
        minimum = sys.maxsize
        for i in range(3):
            number_of_tries = 0
            won_guesser = 0
            numb = get_random_number()
            print('\n'+str(numb)+'\n')
            connection.sendall(str.encode(' <<<Guess The Number !' + 'Round ' + str(i + 1) + ' >>>\n'))
            while won_guesser == 0:
                response = int(connection.recv(2048).decode('utf-8'))
                result = validation_answer(response, numb)
                connection.sendall(str.encode(result[0]))
                won_guesser = result[1]
                number_of_tries += 1

            if number_of_tries <= minimum:
                minimum = number_of_tries
        connection.sendall(str.encode('The best score is ' + str(minimum) + ' !\n'))
    elif game_type == '2':
        game_role = connection.recv(2048).decode('utf-8')
        minimum = sys.maxsize
        if guesser == 1 and game_role == '1':
            connection.sendall(str.encode('\nSorry but this role has been taken!\n'))
            connection.close()
            return
        elif guesser == 0 and game_role == '1':
            connection.sendall(str.encode('\nYou received GUESSER role!\n'))
        if sender == 1 and game_role == '2':
            connection.sendall(str.encode('\nSorry but this role has been taken!\n'))
            connection.close()
            return
        elif sender == 0 and game_role == '2':
            connection.sendall(str.encode('\nYou received SENDER role!\n'))

        if guesser == 0 or sender == 0:
            if game_role == '1':
                lock_guesser.acquire()
                guesser = 1
                lock_guesser.release()
            elif game_role == '2':
                lock_sender.acquire()
                sender = 1
                lock_sender.release()
        for i in range(3):
            won_guesser = 0
            won_sender = 0
            resp_sender = -1
            number_of_tries = 0
            n = -1
            if game_role == '1':
                while n == -1:
                    pass
                connection.sendall(str.encode(' <<<Guess The Number !' + 'Round ' + str(i + 1) + ' >>>\n'))
                while won_guesser == 0:
                    response = int(connection.recv(2048).decode('utf-8'))
                    lock_for_answer.acquire()
                    resp_sender = response
                    lock_for_answer.release()
                    result = validation_answer(response, n)
                    connection.sendall(str.encode(result[0]))
                    won_guesser = result[1]
                    number_of_tries += 1
                if number_of_tries < minimum:
                    minimum = number_of_tries
            elif game_role == '2':
                while guesser == 0:
                    pass
                connection.sendall(str.encode(' <<<Guess The Number !' + 'Round ' + str(i + 1) + ' >>>\n'))
                lock_for_number.acquire()
                n = int(connection.recv(2048).decode('utf-8'))
                lock_for_number.release()
                while won_sender == 0:
                    while resp_sender == -1:
                        pass
                    result = validation_answer(resp_sender, n)
                    connection.sendall(str.encode(result[0]))
                    won_sender = result[1]
                    resp_sender = -1

        connection.sendall(str.encode('The best score is ' + str(minimum) + ' !\n'))

    connection.close()
    guesser = 0
    sender = 0
    n = -1
    resp_sender = -1


def main():
    server_side_socket = socket.socket()
    host = '127.0.0.1'
    port = 2004
    thread_count = 0
    try:
        server_side_socket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Socket is listening..')
    server_side_socket.listen(5)

    while True:
        client, address = server_side_socket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (client,))
        thread_count += 1
        print('Thread Number: ' + str(thread_count))


if __name__ == "__main__":
    main()
