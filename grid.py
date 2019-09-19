import pygame as pg
import os
import time

pg.init()

class Button():

    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline = None): # win:哪一張畫布 / outline:按鈕邊框顏色
        if outline:
            pg.draw.rect(win, outline, (self.x+2, self.y-2, self.width+4, self.height+4), 0) #畫布, 顏色, [x座標, y座標, 寬度, 高度, 線寬]

        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pg.font.SysFont('arial', 32)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

StartButton = Button((0,225,0), 400, 350, 200, 50, 'Start')
RestartButton = Button((0,225,0), 200, 350, 150, 50, 'Restart')
ExitButton = Button((0,0,225), 600, 350, 150, 50, 'Exit')

class Grid:
    def __init__(self) :
        self.error_flag = 0;
        self.win_flag = 0;

        self.board = [
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1]
                                       ]
        self.cup = [[],[],[],[],[],[],[],[],[]]
        self.j = -1
        self.i=-1

        self.x_point = [100, 200, 400, 600, 800, 900, 1000]
        self.y_point = [160, 320, 480]
        self.start = False
        self.which_choice = False
        self.win = None
        self.choice_player = ''
        self.turn = 1
        width, height = 1000, 480
        self.screen = pg.display.set_mode((width, height), 0, 32)
        self.red = [(0,40), (100,40), (0,200), (100,200), (0,360), (100,360)]
        self.blue = [(800,40), (900,40), (800,200), (900,200), (800,360), (900,360)]
        self.winner_final = -1


        self.start_game = pg.image.load('image/start_game.png').convert()
        self.red1_1 = pg.image.load('image/red1.png').convert_alpha()
        self.red1_2 = pg.image.load('image/red1.png').convert_alpha()
        self.red2_1 = pg.image.load('image/red2.png').convert_alpha()
        self.red2_2 = pg.image.load('image/red2.png').convert_alpha()
        self.red3_1 = pg.image.load('image/red3.png').convert_alpha()
        self.red3_2 = pg.image.load('image/red3.png').convert_alpha()
        self.blue1_1 = pg.image.load('image/blue1.png').convert_alpha()
        self.blue1_2 = pg.image.load('image/blue1.png').convert_alpha()
        self.blue2_1 = pg.image.load('image/blue2.png').convert_alpha()
        self.blue2_2 = pg.image.load('image/blue2.png').convert_alpha()
        self.blue3_1 = pg.image.load('image/blue3.png').convert_alpha()
        self.blue3_2 = pg.image.load('image/blue3.png').convert_alpha()
        self.bluewin = pg.image.load('image/circlewin.png').convert_alpha()
        self.redwin = pg.image.load('image/xwin.png').convert_alpha()
        self.now = ''
        self.selected = None
        self.selected_offset_x = 0
        self.selected_offset_y = 0
        self.starting_point_x = None
        self.starting_point_y = None
        self.side = None
        self.min = 10000
        self.pos_x, self.pos_y = -1, -1
        self.term1 = 10
        self.term2 = 10
        self.cup_idx = -1


    def who_start(self, choice) :
        self.screen.fill((0,0,0))
        self.which_choice = True
        if choice == 'o' :
            self.choice_player = 'o'
        else :
            self.choice_player = 'x'
        self.screen.blit(self.start_game, (200, 0))

        self.screen.blit(self.red1_1, self.red[0])
        self.screen.blit(self.red1_2, self.red[1])
        self.screen.blit(self.red2_1, self.red[2])
        self.screen.blit(self.red2_2, self.red[3])
        self.screen.blit(self.red3_1, self.red[4])
        self.screen.blit(self.red3_2, self.red[5])
        self.screen.blit(self.blue1_1, self.blue[0])
        self.screen.blit(self.blue1_2, self.blue[1])
        self.screen.blit(self.blue2_1, self.blue[2])
        self.screen.blit(self.blue2_2, self.blue[3])
        self.screen.blit(self.blue3_1, self.blue[4])
        self.screen.blit(self.blue3_2, self.blue[5])
        pg.display.update()

    def restart_gui(self) :
        bg = pg.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill((0, 0, 0))
        font = pg.font.SysFont("arial", 80)
        if self.winner_final == 0:
            text = font.render("RED WIN!!", 1, (225, 0, 0))
        else:
            text = font.render("BLUE WIN!!", 1, (225, 0, 0))
        bg.blit(text, (300, 100))
        pg.display.update()
        time.sleep(5)

    def getpos(self, pick) :
        #print('pick:', pick)
        org_x, org_y = pg.mouse.get_pos()
        x, y = org_x, org_y
        xp = False
        yp = False
        i = 0
        j = 0
        #print('org_x:', x, "org_y:", y)
        #print('red_0:',self.red[0])
        for x_pt in self.x_point:
            if x < x_pt  and not xp:
                if i < 2 or i > 4:
                    print('lian bien')
                    self.side = 0
                    x = x_pt - 100
                else:
                    if pick == True: # 點到放在格子上的
                        self.side = 1
                        #print('hi')
                        #print('x_pt:', x_pt)
                        print('chong zien')

                    x = x_pt - 200
                xp = True
                break
            i += 1

        for y_pt in self.y_point:
            if y < y_pt and not yp:
                y = y_pt - 160
                yp = True
                break
            j += 1

        #print('new_x:', x, 'new_y:', y)
        if self.selected is None:
            self.pos_x = j
            self.pos_y = i
            return org_x, org_y, x, y
        else:
            return i, j, x, y

    def print_cups(self) :
        self.screen.fill((0,0,0))
        self.screen.blit(self.start_game, (200, 0))

        self.screen.blit(self.red3_1, self.red[4])
        self.screen.blit(self.red3_2, self.red[5])
        self.screen.blit(self.blue3_1, self.blue[4])
        self.screen.blit(self.blue3_2, self.blue[5])

        self.screen.blit(self.red2_1, self.red[2])
        self.screen.blit(self.red2_2, self.red[3])
        self.screen.blit(self.blue2_1, self.blue[2])
        self.screen.blit(self.blue2_2, self.blue[3])

        self.screen.blit(self.red1_1, self.red[0])
        #print("self.red[0]: ",self.red[0])
        self.screen.blit(self.red1_2, self.red[1])
        self.screen.blit(self.blue1_1, self.blue[0])
        self.screen.blit(self.blue1_2, self.blue[1])

        pg.display.update()

    def choice(self) :
        self.selected = None
        org_x, org_y, x, y = self.getpos(pick = True)
        print('x:', x, 'y:', y)
        self.starting_point_x = x
        self.starting_point_y = y

        if x >= 200 and x <400 :
            self.term1 = 2
        elif x >=400 and x <600 :
            self.term1 = 3
        elif x >= 600 and x <800 :
            self.term1 = 4
        if y <160:
            self.term2 = 0
        elif y >=160 and y <320:
            self.term2 = 1
        elif y >=320 and y <480:
            self.term2 = 2
        print(self.term1,self.term2)

        if self.turn % 2 == 1: #輪到紅色
            ## 點選的是放在兩旁的杯子
            if self.side == 0:
                for i, c in enumerate(self.red):
                    if c[0] == x and c[1]-40 == y:
                        print('red:')
                        print(i)
                        self.now = 'o'
                        self.selected = i
                        self.selected_offset_x = x - org_x
                        self.selected_offset_y = y - org_y
                        return

            ## 選到在格子裡的
            elif self.side == 1:
                output = self.trans(self.pos_x, self.pos_y)
                print('outputttttttt', self.cup[output])
                for i, c in enumerate(self.red):
                    #print ('c[0]:', c[0], 'c[1]', c[1])
                    if c[0] >= x and c[1] >= y:
                        self.now = 'o'
                        if c[0]-x <= self.min  and c[1] < y+160 and c[0] < x+200:
                            #print('cup:',self.cup)
                            print('reddddd:')
                            print(i)
                            self.min = abs(c[0]-x)
                            self.selected = i
                            self.selected_offset_x = x - org_x
                            self.selected_offset_y = y - org_y
                            if(len(self.cup[output])==3):
                                return
                if self.min < 10000:
                    #print('mamamia')
                    return
        else: #輪到藍色
            if self.side == 0:
                for i, c in enumerate(self.blue):
                    if c[0] == x and c[1]-40 == y:
                        print("blue:")
                        print(i)
                        self.now = 'x'
                        self.selected = i
                        self.selected_offset_x = x - org_x
                        self.selected_offset_y = y - org_y
                        return
            elif self.side == 1:
                output = self.trans(self.pos_x, self.pos_y)
                for i, c in enumerate(self.blue):
                    #print ('c[0]:', c[0], 'c[1]', c[1])
                    if c[0] >= x and c[1] >= y:
                        self.now = 'x'
                        if c[0]-x <= self.min  and c[1] < y+160 and c[0] < x+200:
                            print('blue:')
                            print(i)
                            self.min = abs(c[0]-x)
                            self.selected = i
                            self.selected_offset_x = x - org_x
                            if(len(self.cup[output])==3):
                                return


                if self.min < 10000:
                    #print('mamamia_2')
                    return

        ## 點錯顏色
        print("oops:")
        self.selected = None


    def move(self):
        x, y = pg.mouse.get_pos()
        if self.choice_player == 'o': #紅色先發
            if self.turn % 2 == 1: #輪到紅色
                self.red[self.selected] = (x + self.selected_offset_x, y + self.selected_offset_y)
                #print(self.red[self.selected])
            else:
                self.blue[self.selected] = (x + self.selected_offset_x, y + self.selected_offset_y)
                #print(self.blue[self.selected])
        else: #輪到藍色
            if self.turn % 2 == 1: #輪到藍色
                self.blue[self.selected] = (x + self.selected_offset_x, y + self.selected_offset_y)
                #print(self.blue[self.selected])
            else:
                self.red[self.selected] = (x + self.selected_offset_x, y + self.selected_offset_y)
                #print(self.red[self.selected])

    def who_win(self, winner) :
        if winner == 0 :
            print('red win!')
            self.winner_final = 0
        else :
            print('blue win!')
            self.winner_final = 1


    def is_win(self):
        wins = [
            [self.board[0][2], self.board[0][3], self.board[0][4]], # 橫(1)
            [self.board[1][2], self.board[1][3], self.board[1][4]], # 橫(2)
            [self.board[2][2], self.board[2][3], self.board[2][4]], # 橫(3)
            [self.board[0][2], self.board[1][2], self.board[2][2]], # 直(1)
            [self.board[0][3], self.board[1][3], self.board[2][3]], # 直(2)
            [self.board[0][4], self.board[1][4], self.board[2][4]], # 直(3)
            [self.board[0][2], self.board[1][3], self.board[2][4]], # 斜(1)
            [self.board[0][4], self.board[1][3], self.board[2][2]]  # 斜(2)
        ]

        for win in wins :
            if not min(win) == -1 and win[0]%2 == win[1]%2 and win[1]%2 == win[2]%2 :
                self.who_win(win[0]%2)
                self.win = win[0] % 2
                print('win')

    def trans(self, j, i):
        cup = None
        if j == 0:
            if i == 2:
                cup = 0
            elif i == 3:
                cup = 1
            elif i == 4:
                cup = 2
        elif j == 1:
            if i == 2:
                cup = 3
            elif i == 3:
                cup = 4
            elif i == 4:
                cup = 5
        elif j == 2:
            if i == 2:
                cup = 6
            elif i == 3:
                cup = 7
            elif i == 4:
                cup = 8
        return cup

    def set_board(self):
        print("set board")
        #print('now:',self.now)
        #print('selected:',self.selected)
        ## 用來判斷是否符合大杯子蓋小杯子的規則

        i, j, x, y = self.getpos(pick = False) # [j,i] 為目的地在self.board的位置
        #print('x:', j)
        #print('y:', i)
        #print('org:', self.board[j][i])
        self.j = j
        self.i = i
        self.cup_idx = self.trans(j, i)
        #print('set_x:', j, 'set_y:', i)
        if self.board[j][i] == -1 and self.now == 'o':
            #print('a')
            self.cup[self.cup_idx].append(self.selected)
            if self.selected == 0  or self.selected == 1: # 大的
                self.board[j][i] = 0
            elif self.selected == 2 or self.selected == 3: # 中的
                self.board[j][i] = 2
            else: # 小的
                self.board[j][i] = 4

        elif self.board[j][i] == -1 and self.now == 'x':
            #print('b')
            self.cup[self.cup_idx].append(self.selected)
            if self.selected == 0 or self.selected == 1: # 大的
                self.board[j][i] = 1
            elif self.selected == 2 or self.selected == 3: # 中的
                self.board[j][i] = 3
            else: # 小的
                self.board[j][i] = 5
        elif (self.board[j][i] == 2 or self.board[j][i] == 4) and self.now == 'x' and (self.selected == 0 or self.selected == 1): # 如果原先放的是紅中或是紅小，然後準備放的是藍大
                #print('c')
                self.cup[self.cup_idx].append(self.selected)
                self.board[j][i] = 1                                                                # 那就是藍大
        elif self.board[j][i] == 4 and self.now == 'x' and (self.selected == 2 or self.selected == 3):                            # 如果原先放的是紅小，然後準備放的是藍中，
                #print('d')
                self.cup[self.cup_idx].append(self.selected)
                self.board[j][i] = 3                                                                # 那就是藍中
        elif (self.board[j][i] == 3 or self.board[j][i] == 5) and self.now == 'o' and (self.selected == 0 or self.selected == 1): # 如果原先放的是藍中或是藍小，然後準備放的是紅大
                #print('e')
                self.cup[self.cup_idx].append(self.selected)
                self.board[j][i] = 0                                                                # 那就是紅大
        elif self.board[j][i] == 5 and self.now == 'o' and (self.selected == 2 or self.selected == 3):                            # 如果原先放的是藍小，然後準備放的是紅中
                #print('f')
                self.cup[self.cup_idx].append(self.selected)
                self.board[j][i] = 2                                                                # 那就是紅中
        else: # 不符合移動規則要把圖片放回原位
            print('oops')
            if self.now == 'o':
                self.red[self.selected] = (self.starting_point_x, self.starting_point_y + 40)
                self.turn -= 1
            else:
                self.blue[self.selected] = (self.starting_point_x, self.starting_point_y + 40)
                self.turn -= 1

        if self.side == 1:
            output = self.trans(self.pos_x, self.pos_y)
            #print('output:', output)
            if self.now == 'o':
                print(self.cup[output])
                if self.cup[output] == []:
                    #print('nnnnnnnnnnnnnn')
                    self.board[self.pos_x][self.pos_y] = -1
                else:
                    self.cup[output].pop()
                    if self.cup[output] == []:
                        self.board[self.pos_x][self.pos_y] = -1
                    else:
                        val = self.cup[output][len(self.cup[output])-1]
                        if val == 0 or val == 1: # 大的
                            self.board[self.pos_x][self.pos_y] = 1
                        elif val == 2 or val == 3: # 中的
                            self.board[self.pos_x][self.pos_y] = 3
                        else: # 小的
                            self.board[self.pos_x][self.pos_y] = 5
            else:
                self.cup[output].pop()
                #print(self.cup[output])
                if self.cup[output] == []:

                    self.board[self.pos_x][self.pos_y] = -1
                else:
                    if self.cup[output] == []:
                        self.board[self.pos_x][self.pos_y] = -1
                    else:
                        val = self.cup[output][len(self.cup[output])-1]
                        if val == 0 or val == 1: # 大的
                            self.board[self.pos_x][self.pos_y] = 0
                        elif val == 2 or val == 3: # 中的
                            self.board[self.pos_x][self.pos_y] = 2
                        else: # 小的
                            self.board[self.pos_x][self.pos_y] = 4

        self.is_win()

        self.turn += 1
        print("self.turn= ",self.turn)
