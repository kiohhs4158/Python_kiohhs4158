#モジュールのインポート
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import random
#スタート画面の描画
def draw_start():    
    start = Tk()
    start.title(u'Squash Game!')
    canvas_st = Canvas(start, width = 640, height = 480)
    canvas_st.pack()
    canvas_st.create_rectangle(0, 0, 640, 480, fill = 'white')
    canvas_st.create_text(320, 140, text = 'Welcome to Squash Game',
                          fill = 'blue', font = ('Meiryo UI', 24), justify = 'center')
    canvas_st.create_text(320, 220, text = 'ラケットの大きさを選択してください', font = ('Meiryo UI', 16), justify = 'center')
    
    global select
    select = IntVar(start, value = 150)
    #ラジオボタンの設定
    for i in range(3):
        size_radio = ttk.Radiobutton(start, text = str(75 * (i + 1)),value = 75 * (i + 1), variable = select)
        size_radio.place(x = 260 + (i * 60), y = 270)

    start_btn = ttk.Button(start, text = 'Start', width = 30, command = lambda:[close_start(), game_start()])
    start_btn.place(x = 250, y = 320)
    
    def close_start():
        global select_size
        select_size = select.get()
        canvas_st.delete('all')
        start.destroy()

draw_start()

def game_start():
    #ウィンドウの作成
    root = Tk()
    canvas = Canvas(root, width = 640, height = 480)
    canvas.pack()
    #ゲームの初期化
    def init_game():
        global is_gameover, point, life, game_speed, move_speed
        global ball_position_x, ball_position_y, ball_move_x, ball_move_y, ball_size
        global racket_center_x, racket_size
        global block_position_x, block_position_y, block_move_x, block_move_y, block_size_x, block_size_y
        
        is_gameover = False
        point = 0
        life = 3
        game_speed = 50
        move_speed = 15
        ball_position_x = random.randint(400, 500)
        ball_position_y = random.randint(100, 200)
        ball_move_x = move_speed
        ball_move_y = move_speed * -1
        ball_size = 10
        racket_center_x = 320
        racket_size = select_size
        block_position_x = 10
        block_position_y = random.randint(60, 100)
        block_size_x = random.randint(30, 120)
        block_size_y = random.randint(40, 300)
        block_move_x = move_speed
    #ゲーム画面の描画
    def draw_game():
        canvas.delete('all')
        canvas.create_rectangle(0, 0, 640, 480, fill = 'white', width = 0)
    #ボールの描画
    def draw_ball():
        canvas.create_oval(ball_position_x - ball_size, ball_position_y - ball_size,
                           ball_position_x + ball_size, ball_position_y + ball_size, fill = 'yellow')
    #ラケットの描画
    def draw_racket():
        global racket_left_x, racket_right_x
        racket_left_x = racket_center_x - racket_size/2
        racket_right_x = racket_center_x + racket_size/2
        #上記をgame_init内に記述するとgame_loop()中にmotion()の値で上記の計算がされないのでラケットは動かない
        canvas.create_rectangle(racket_left_x, 470, racket_right_x, 480, fill = '#00ffff')
        canvas.create_line(racket_center_x, 470, racket_center_x, 480, width = 4.0)
    #障害物の描画
    def draw_block():
        canvas.create_rectangle(block_position_x, block_position_y,
                                block_position_x + block_size_x, block_position_y + block_size_y, fill = 'red')
    #的の描画
    def draw_target():
        for j in range(3):
            canvas.create_rectangle(160 * j + 120, 0, 160 * j + 200, 10, fill = 'green')
    #ボールの移動
    def move_ball():
        global is_gameover, point, life
        global ball_position_x, ball_position_y, ball_move_x, ball_move_y
        
        if is_gameover:
            return
        #左右の壁に当たったかどうかの判定
        if ball_position_x + ball_move_x < 0 or ball_position_x + ball_move_x >640:
            ball_move_x *= -1
        #天井に当たったかどうかの判定
        if ball_position_y + ball_move_y < 0:
            ball_move_y *= -1
        #的に当たった時の判定
        for k in range(3):
            if ball_position_y + ball_move_y < 10 and \
               (160 * k + 120) <= ball_position_x + ball_move_x <= (160 * k + 200):
                ball_move_y *= -1
        #ラケットの左側に当たったかどうかの判定
        if ball_position_y + ball_move_y >= 470 and \
           racket_left_x - 5 <= ball_position_x + ball_move_x <= racket_center_x:
            ball_move_y *= -1
            if ball_move_x > 0:
                ball_move_x *= -1
                
            mes = random.randint(0, 2)
            if mes == 0:
                message = '素敵'
            elif mes == 1:
                message = '上手'
            else:
                message = 'ナイス'
            point += 10
            root.title(message + '！あなたの得点は' + str(point) + '点です')
        #ラケットの右側に当たったかどうかの判定
        if ball_position_y + ball_move_y >= 470 and \
           racket_center_x <= ball_position_x + ball_move_x <= racket_right_x + 5:
            ball_move_y *= -1
            if ball_move_x < 0:
                ball_move_x *= -1
            mes = random.randint(0, 2)
            if mes == 0:
                message = '素敵'
            elif mes == 1:
                message = '上手'
            else:
                message = 'ナイス'
            point += 10
            root.title(message + '！あなたの得点は' + str(point) + '点です')
        #ミスした時の判定
        if ball_position_y + ball_move_y >= 480 and life > 0:
            life -= 1
            ball_position_x = random.randint(400, 500)
            ball_position_y = random.randint(100, 200)
        elif ball_position_y + ball_move_y >= 480 and life == 0:
            is_gameover = True
            if point <= 50:
                message = 'ドンマイ'
            elif 50 < point <= 200:
                message = '次は高得点を目指そう'
            else:
                message = 'あなたは最高のプレーヤーです'
            
            root.title('あなたの得点は' + str(point) + '点でした！' + message)
        #障害物に当たったかどうかの判定
        #障害物の上下
        if ball_move_y > 0 and \
           block_position_y <= ball_position_y + ball_move_y <= block_position_y + block_size_y / 2  and \
           block_position_x + block_move_x <= ball_position_x + ball_move_x <= block_position_x + block_move_x + block_size_x:
            ball_move_y *= -1
        if ball_move_y < 0 and \
           block_position_y - block_size_y / 2 <= ball_position_y + ball_move_y <= block_position_y + block_size_y   and \
           block_position_x + block_move_x <= ball_position_x + ball_move_x <= block_position_x + block_move_x + block_size_x:
            ball_move_y *= -1
        #障害物の左右
        if ball_move_x > 0 and \
           block_position_x +block_move_x  <= ball_position_x + ball_move_x <= block_position_x +block_move_x + block_size_x / 2 and \
           block_position_y <= ball_position_y + ball_move_y  <= block_position_y + block_size_y:
            ball_move_x *= -1
        if ball_move_x < 0 and \
           block_position_x + block_move_x - block_size_x / 2 <= ball_position_x + ball_move_x <= block_position_x + block_size_x + block_move_x and \
           block_position_y <= ball_position_y + ball_move_y  <= block_position_y + block_size_y:
            ball_move_x *= -1
        #ボールの移動
        if 0 <= ball_position_x + ball_move_x <= 640:
            ball_position_x = ball_position_x + ball_move_x
        if 0 <= ball_position_y + ball_move_y <= 480:
            ball_position_y = ball_position_y + ball_move_y
    #ラケットの移動
    def motion(event):
        if is_gameover:
            return
        
        global racket_center_x
        racket_center_x = event.x

    def click(event):
        if event.num == 1 and is_gameover:
            init_game()

    root.bind('<Motion>', motion)
    root.bind('<Button>', click)
    #障害物の移動
    def move_block():
        global block_position_x, block_move_x

        if is_gameover:
            return
        #障害物が壁に当たったかどうかの判定
        if block_position_x + block_move_x < 0 or block_position_x + block_size_x + block_move_x >640:
            block_move_x *= -1
        #障害物の移動
        if 0 <= block_position_x + block_move_x and block_position_x + block_size_x + block_move_x <= 640:
            block_position_x = block_position_x + block_move_x
    #ゲームの繰り返し処理
    def game_loop():
        draw_game()
        draw_target()
        draw_racket()
        draw_block()
        draw_ball()
        move_ball()
        move_block()
        root.after(game_speed, game_loop)
    #ゲームのメイン処理
    init_game()
    game_loop()
    root.mainloop()
