import pygame as pg
import time
from grid import Grid
from grid import Button
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'

surface = pg.display.set_mode((600,600))
pg.display.set_caption('Tic-tac-toe')

# create a separate thread to send and receive data from the client
import threading
def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

# creating a TCP socket for the server
import socket
HOST = '127.0.0.1'
PORT = 65432
connection_established = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

def receive_data():
    while True:
        data = conn.recv(1024).decode() # receive data from the client, it is a blocking method
        if data == "bluewin":
            grid.winner_final = 1
            print("got")
            break
        elif data == "redwin":
            grid.winner_final = 0
            print("got")
            break
        else:
            data = data.split('-') # the format of the data after splitting is: ['x', 'y', 'yourturn', 'playing']

            temp = data[0]
            temp = temp.strip('(')
            temp = temp.strip(')')
            temp = temp.split(',')
            t = int(temp[0])
            t1 = int(temp[1])
            #print("t: ",t)
            #print("t1: ",t1)
            select = int(data[1])
            if select == 0 or select==1:
                cup_color = 1
            elif select == 2 or select == 3:
                cup_color = 3
            elif select == 4 or select == 5:
                cup_color = 5
            grid.blue[select]=(t,t1)
            if t > 200 and t <400 :
                if t1 <160:
                    grid.board[0][2] = cup_color

                elif t1 >160 and t1 <320:
                    grid.board[1][2] = cup_color

                elif t1 >320 and t1 <480:
                    grid.board[2][2] = cup_color

            elif t >400 and t <600 :
                if t1 <160:
                    grid.board[0][3] = cup_color

                elif t1 >160 and t1 <320:
                    grid.board[1][3] = cup_color

                elif t1 >320 and t1 <480:
                    grid.board[2][3] = cup_color

            elif t > 600 and t <800 :
                if t1 <160:
                    grid.board[0][4] = cup_color

                elif t1 >160 and t1 <320:
                    grid.board[1][4] = cup_color

                elif t1 >320 and t1 <480:
                    grid.board[2][4] = cup_color



            print("grid.blue: ",grid.blue[select])

            turn = int(data[2])
            grid.turn = turn
            num3 = int(data[3])
            num4 = int(data[4])
            if num4 == 0:
                if num3 == 2:
                    num = 0
                elif num3 == 3:
                    num = 1
                elif num3 == 4:
                    num = 2
            elif num4 == 1:
                if num3 ==2:
                    num = 3
                elif num3 == 3:
                    num = 4
                elif num3 == 4:
                    num = 5
            elif num4 == 2:
                if num3 == 2:
                    num = 6
                elif num3 == 3:
                    num = 7
                elif num3 == 4:
                    num = 8
            cup_idx = int(data[5])
            grid.cup[cup_idx].append(select)
            if(num3 !=10 and num4 != 10):
                    if grid.cup[num] == []:
                        grid.board[num4][num3] = -1
                    else:
                        grid.cup[num].pop()
                        if grid.cup[num] == []:
                            grid.board[num4][num3] = -1
                        else:
                            val = grid.cup[num][0]
                            print("val",val)
                            if val == 0 or val == 1: # 大的
                                grid.board[num4][num3] = 0
                            elif val == 2 or val == 3: # 中的
                                grid.board[num4][num3] = 2
                            else: # 小的
                                grid.board[num4][num3] = 4



            print(grid.board)
            print(grid.cup)
            grid.print_cups()

def waiting_for_connection():
    global connection_established, conn, addr
    print("124")
    conn, addr = sock.accept() # wait for a connection, it is a blocking method
    print('client is connected')
    connection_established = True
    receive_data()

# run the blocking functions in a separate thread
create_thread(waiting_for_connection)

grid = Grid()
grid.who_start('o')
running = True
if grid.winner_final!=-1:
    running = False
while running:
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
            pg.quit()
        #click
        if grid.turn%2==1 and event.type == pg.MOUSEBUTTONDOWN and grid.which_choice and grid.win is None:
            #print('turn = ', grid.turn)

            grid.choice()
            """
            if grid.error_flag == 1:
                pg.mixer.Channel(0).play(pg.mixer.Sound('sound\Concussive_Hit_Guitar_Boing.wav'))
                pg.mixer.Channel(0).set_volume(1000)
            """
        #drag
        elif event.type == pg.MOUSEMOTION and grid.which_choice and grid.win is None:
            if grid.selected is not None:
                grid.move()
                if grid.side==1:
                    num1 = grid.term1
                    num2 = grid.term2
                else :
                    num1 = 10
                    num2 = 10

        #drop
        elif event.type == pg.MOUSEBUTTONUP and grid.which_choice and grid.win is None:
                    #print('selected',grid.selected)
                    """
                    if grid.error_flag == 0:
                        pg.mixer.Channel(0).play(pg.mixer.Sound('sound\Pop.wav'))
                        pg.mixer.Channel(0).set_volume(0.8)
                    else:
                        grid.error_flag=0
                    """
                    if grid.selected is not None:
                        grid.set_board()
                        print('hihi')
                        print('selected:', grid.selected)
                        print(grid.cup[grid.cup_idx])
                        #print("type: ",type(grid.selected))
                        send_data = '{}-{}-{}-{}-{}-{}'.format(grid.red[grid.selected],grid.selected,grid.turn,num1,num2,grid.cup_idx).encode()
                        conn.send(send_data)
                        grid.print_cups()
                        print(grid.board)
                        print('++++++++++++++++')
                        print(grid.cup)
                        print('=================================================')
                    grid.selected = None


    if grid.selected != None  and grid.win is None :
        grid.print_cups()

    if grid.winner_final == 0 :
        bg = pg.Surface(grid.screen.get_size())
        bg = bg.convert()
        bg.fill((0, 0, 0))
        font = pg.font.SysFont("arial", 80)
        text = font.render("RED WIN!!", 1, (225, 0, 0))
        bg.blit(text, (300, 100))
        grid.screen.blit(bg, (0, 0))
        pg.display.update()
        conn.send(("redwin").encode())
        print("redwin")
        grid.winner_final = None

        #time.sleep(5)

        #break

    elif grid.winner_final == 1  :
        print("bluewin")
        bg = pg.Surface(grid.screen.get_size())
        bg = bg.convert()
        bg.fill((0, 0, 0))
        font = pg.font.SysFont("arial", 80)
        text = font.render("BLUE WIN!!", 1, (0, 225, 0))
        bg.blit(text, (300, 100))
        grid.screen.blit(bg,(0,0))
        pg.display.update()
        conn.send(("bluewin").encode())
        grid.winner_final = None
        #time.sleep(5)

        #break


        #surface.fill((0,0,0))
        #grid.print_cups()
        #pg.display.flip()


#time.sleep(5)


pg.quit()
