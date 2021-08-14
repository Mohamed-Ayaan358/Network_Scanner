from queue import Queue
import socket
import threading
import os
# IP->Address of the system network, Port-> address of service within system.
import platform
choice = int(input('\nEnter your choice \n1.Live TCP scan(Used for specifically finding the open ports) \n2.Detailed TCP scan(Slower but it tells what networks are live and what is not)'))
if(choice == 1):
    socket.setdefaulttimeout(0.30)
    print_lock = threading.Lock()
# This part of the code I used threading as a challenge to myself.
    target = input('Enter the host to be scanned: ')
    minlimit = int(input('Enter the minimum value: '))
    maxlimit = int(input('Enter the maximum value: '))
    t_IP = socket.gethostbyname(target)
    print('Starting scan on host: ', t_IP)

    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #These sockets are used for sending and receiving packets
        try:
            con = s.connect((t_IP, port))
            with print_lock:
                print(port, 'is open')
            con.close()
        except:
            pass
        else:
            print("There are no networks within that range")

    def threader(): #We use threading so as to increase the speed of the programs as some ranges may take longer than normal
        while True:
            worker = q.get()
            portscan(worker)
            q.task_done()

    q = Queue()

    for x in range(100):
        t = threading.Thread(target=threader)
        t.daemon = True #It allows the program to run in the background
        t.start()

    for worker in range(minlimit, maxlimit):
        q.put(worker)

    q.join()

elif(choice == 2):
    net = input("Enter the IP address: ")
    net1 = net.split('.')
    a = '.'

    net2 = net1[0] + a + net1[1] + a + net1[2] + a
    minlimit = int(input("Enter the minimum Number: "))
    maxlimit = int(input("Enter the maximum Number: "))
    maxlimit = maxlimit + 1

    def scan(addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((addr, 135))
        if result == 0:
            return 1
        else:
            return 0

    def run1():
        for ip in range(minlimit, maxlimit):
            addr = net2 + str(ip)
            if (scan(addr)):
                print(addr, "is live")

    run1()
