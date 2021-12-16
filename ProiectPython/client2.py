import socket

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
valid_option = False
while not valid_option:
    option = int(input('Your option: '))
    if option == 1:
        client.send(str.encode(str(option)))
        valid_option = True
        for i in range(3):
            begin_round = client.recv(1024)
            print(begin_round.decode('utf-8'))
            won_round = 0
            while not won_round:
                number = int(input("Your number: "))
                client.send(str.encode(str(number)))
                result_round = client.recv(1024).decode('utf-8')
                won_round = int(client.recv(1).decode('utf-8'))
                print(result_round)
        score = client.recv(1024).decode('utf-8')
        print(score)
    elif option == 2:
        client.send(str.encode(str(option)))
        valid_option = True
        valid_role = False
        print('\nDo you want to play as ?\n1.Guesser\n2.Sender\n')
        while not valid_role:
            role = int(input('Your role: '))
            if role == 1:
                client.send(str.encode(str(role)))
                valid_role = True
                for i in range(3):
                    begin_round = client.recv(1024)
                    print(begin_round.decode('utf-8'))
                    won_round = 0
                    while not won_round:
                        number = int(input("Your number: "))
                        client.send(str.encode(str(number)))
                        result_round = client.recv(1024).decode('utf-8')
                        won_round = int(client.recv(1).decode('utf-8'))
                        print(result_round)
                score = client.recv(1024).decode('utf-8')
                print(score)
            elif role == 2:
                client.send(str.encode(str(role)))
                valid_role = True
                for i in range(3):
                    valid_number = 0
                    number = -1
                    begin_round = client.recv(1024)
                    print(begin_round.decode('utf-8'))
                    while not valid_number:
                        number = int(input('Your number: '))
                        if number >= 0 & number <= 50:
                            valid_number = 1
                        else:
                            print('\n Invalid number! \n')
                    client.send(str.encode(str(number)))
                    won_round = 0
                    while not won_round:
                        result_round = client.recv(1024).decode('utf-8')
                        won_round = int(client.recv(1).decode('utf-8'))
                        print(result_round)
                score = client.recv(1024).decode('utf-8')
                print(score)

client.close()
