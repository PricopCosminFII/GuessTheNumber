import socket


def send_valid_number():
    valid_number = False
    while not valid_number:
        number = input('Your number: ')
        if number.isnumeric():
            number = int(number)
            if 0 <= number <= 50:
                return number
            else:
                print('\nYour number is out of range. Please choose a number in range [0-50]. \n')

        else:
            print('\nYour input is not numeric!\n')


def send_valid_role():
    valid_role = False
    while not valid_role:
        role = input('Your role: ')
        if role.isnumeric():
            role = int(role)
            if role == 1:
                return role
            elif role == 2:
                return role
            else:
                valid_role = False
                print('\n Invalid role ! \n')

        else:
            valid_role = False
            print('\n Invalid role ! \n')


def send_valid_option():
    valid_option = False
    while not valid_option:
        option = input('Your option: ')
        if option.isnumeric():
            option = int(option)
            if option == 1:
                return option
            elif option == 2:
                return option
            else:
                print('\n Invalid option ! \n')

        else:
            print('\n Invalid option ! \n')


def main():
    client = socket.socket()
    host = '127.0.0.1'
    port = 2004

    print('Waiting for connection response')
    try:
        client.connect((host, port))
    except socket.error as e:
        print(str(e))

    res = client.recv(1024)
    print(res.decode('utf-8'))
    option = send_valid_option()
    if option == 1:
        client.send(str.encode(str(option)))
        for i in range(3):
            begin_round = client.recv(1024)
            print(begin_round.decode('utf-8'))
            won_round = ''
            while not won_round == 'Correct! Number guessed!\n':
                number = send_valid_number()
                client.send(str.encode(str(number)))
                won_round = client.recv(1024).decode('utf-8')
                print(won_round)
        score = client.recv(1024).decode('utf-8')
        print(score)
    elif option == 2:
        client.send(str.encode(str(option)))
        print('\nDo you want to play as ?\n1.Guesser\n2.Sender\n')
        role = send_valid_role()
        if role == 1:
            client.send(str.encode(str(role)))
            server_role = client.recv(1024).decode('utf-8')
            print(server_role)
            if server_role == '\nSorry but this role has been taken!\n':
                return
            for i in range(3):
                begin_round = client.recv(1024)
                print(begin_round.decode('utf-8'))
                won_round = ''
                while not won_round == 'Correct! Number guessed!\n':
                    number = send_valid_number()
                    client.send(str.encode(str(number)))
                    won_round = client.recv(1024).decode('utf-8')
                    print(won_round)
            score = client.recv(1024).decode('utf-8')
            print(score)
        elif role == 2:
            client.send(str.encode(str(role)))
            server_role = client.recv(1024).decode('utf-8')
            print(server_role)
            if server_role == '\nSorry but this role has been taken!\n':
                return
            for i in range(3):
                begin_round = client.recv(1024)
                print(begin_round.decode('utf-8'))
                number = send_valid_number()
                client.send(str.encode(str(number)))
                won_round = ''
                while not won_round == 'Correct! Number guessed!\n':
                    won_round = client.recv(1024).decode('utf-8')
                    print(won_round)
            score = client.recv(1024).decode('utf-8')
            print(score)

    client.close()


if __name__ == "__main__":
    main()
