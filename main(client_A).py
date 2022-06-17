import socket
import random

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "192.168.56.1"
PORT = 12334
connection.connect((IP, PORT))


def proverka(n):# Функция разложения чисел на множители
    d=2
    a = []
    while d*d <= n:
        if n%d == 0:
            a.append(d)
            n //= d
        else:
            if d % 2 != 0:
                d += 2
            else:
                d+= 1
    if n>1:
        a.append(n)
    return a


def generate():# функция генерации ключей
    while True:  # Генерим простое число q
        p = random.randint(2**10,2**20)
        a = proverka(p)
        if len(a) == 1:
            break
    print("Простое число p:",p)

    while True:  # Генерим простое число q
        q = random.randint(10,2**20)
        a = proverka(q)
        if len(a) == 1:
            if (p-1)%q==0:# проверка на делимость без остатка
              break
    print("Простое число q:",q)

    h=random.randint(1,p-1)
    a=int((p-1)/q)
    g=pow(h,a,p)
    print("g:",g)

    w=random.randint(1,p-1)
    print("w (секретный ключ):",w)

    y=pow(g,q-w,p)
    print("y (g^(q-w) mod p):",y)

    print("Открытый ключ (p,q,g,y):","(",p,",",q,",",g,",",y,")")

    message = "{}:{}:{}:{}".format(p,q,g,y)
    connection.send(message.encode('utf-8'))# Отправляем (открытый ключ) клиенту В

    r=random.randint(1,q-1)
    print("r (случайное число):",r)

    x=pow(g,r,p)
    print("x (g^r mod p):",x)
    connection.send(str(x).encode('utf-8'))# Отправляем (x) клиенту В

    while True:# Слушаем клиента B
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    e=int(data)
    print("e:",e)

    s=pow(r+(w*e),1,q)
    print("s ((r + w*e) mod q ):",s)
    connection.send(str(s).encode('utf-8'))# Отправляем (s) клиенту В

    while True:# Слушаем клиента B
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    print("Идентификация:",data)


print("======================================")
# Начало программы
generate()
print("======================================")
