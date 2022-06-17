import socket
import random

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP = socket.gethostbyname(socket.gethostname())
PORT = 12334
listener.bind((IP, PORT))
listener.listen(0)
connection, address = listener.accept()

def fank(data):# функция проверки подлинности
    ############################
    data=data.split(":")
    p=int(data[0])# Принятые данные от Клиента A (открытый ключ)
    q=int(data[1])
    g=int(data[2])
    y=int(data[3])
    #############################
    print("открытый ключ от клиента А (p,q,g,y):", "(", p, ",", q, ",", g, ",", y, ")")

    while True:  # Слушаем клиента А
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    x=int(data)
    print("x:",x)

    t=6# параметр безопасности алгоритма
    print("t:",t)

    e=random.randint(0,(2**t)-1)
    print("e (случайное число):",e)
    connection.send(str(e).encode('utf-8'))# Отправляем (e) клиенту A

    while True:  # Слушаем клиента А
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    s=int(data)
    print("s:",s)

    z=pow((g**s)*(y**e),1,p)
    print("z ((g^s * y^e) mod p):",z)

    if x==z:# Проверка!
        print("Идентификация: Успех!")
        mes="Успех!"
        connection.send(mes.encode('utf-8'))# Отсылаем сообщение клиенту А
    else:
        print("Идентификация: False!")
        mes="False!"
        connection.send(mes.encode('utf-8'))# Отсылаем сообщение клиенту А



def listen():
    while True:# Слушаем клиента А
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    fank(data)

print("======================================")
# Начало программы
listen()
print("======================================")