import socket
import threading

## The first steps of the client are to choose a nickname and to connectto our server.
## We will need to know the exact address and the port at which our server is running.

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


## As you can see, we are using a different function here. Instead of binding the data and
## listening, we are connecting to an existing server.

## Now, a client needs to have two threads that are running at the same time. The first one
## will constantly receive data from the server and the second one will send our own messages
## to the server. So we will need two functions here. Let’s start with the receiving part.


# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

## Again we have an endless while-loop here. It constantly tries to receive messages and to
## print them onto the screen. If the message is ‘NICK’ however, it doesn’t print it but it
## sends its nickname to the server. In case there is some error, we close the connection and
## break the loop. Now we just need a function for sending messages and we are almost done.


# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))



# The last thing we need to do is to start two threads that run these two functions.



# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
