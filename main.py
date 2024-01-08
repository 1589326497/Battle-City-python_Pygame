import pygame
import time
import random

"""
NZX 坦克大战练习项目  项目创建于2022年9月8日 最终版完成时间2022年9月19日    

笔记：    
面向对象的编程
2.明白需求
    1.有哪些类
        1.主逻辑类
            开始游戏
            创建界面窗口
            事件处理
            文字绘制的功能
            结束游戏
        2.坦克类型（1.我方坦克 2.敌方坦克）
            坦克的速度
            移动
            射击  
        3.子弹类
            子弹移动
            子弹的展示
        4.爆炸效果类
            爆炸效果展示
        5.墙壁类
            属性：是否可以通过
        6.音效类
            播放音乐           
"""


class MainGame():
    window = None  # None是一个空对象，可以赋值但不能创建

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500

    COLOR_BLACK = pygame.Color(0, 0, 0)
    COLOR_RED = pygame.Color(255, 0, 0)
    COLOR_WHITE=pygame.Color(255,225,255)

    TANK_PI = None  # 创建我方坦克（坦克的位置随时改变）

    EnemyTank_list = []  # 创建敌方坦克链表
    EnemyTank_count = 5  # 敌方坦克数量

    Bullent_list = []  # 存储我方子弹的链表

    Enemy_bullet_list = []  # 存储敌方子弹的列表

    Explode_list = []  # 爆炸效果链表

    Wall_list = []  # 墙壁链表

    def __init__(self):
        pass

    def startGame(self):  # 开始游戏
        pygame.display.init()  # 初始化显示块模
        MainGame.window = pygame.display.set_mode(
            [MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])  # 初始化要显示的窗口,返回值surfase
        # 创建我方坦克
        self.creatMyTank()
        # 创建敌方坦克
        self.creatEnemyTank()  # 调用创建方法
        # 调用创建墙壁方法
        self.creatWalls()

        pygame.display.set_caption("坦克大战")  # 设置游戏标题
        while True:
            MainGame.window.fill(MainGame.COLOR_BLACK)  # 填充窗口颜色
            self.getEvent()  # 完成事件的获取
            MainGame.window.blit(self.getTextSurface_1("剩余敌方坦克%d辆" % len(MainGame.EnemyTank_list)),
                                 (5, 5))  # 将textSurface粘到window
            MainGame.window.blit(self.getTextSurface_2('攻击空格 方向上下左右 重生m 增加敌人b'), (5, 35))
            MainGame.window.blit(self.getTextSurface_2('NZX 坦克大战练习项目 最终版完成时间2022年9月19日'),(5,475))

            # 调用展示墙壁方法
            self.blitWalls()

            if MainGame.TANK_PI and MainGame.TANK_PI.live:
                # 我方坦克图片的加载
                MainGame.TANK_PI.displayTank()
            else:
                del MainGame.TANK_PI  # 删除坦克
                MainGame.TANK_PI = None

            # 敌方坦克图片的加载
            self.blitEnemyTank()
            if MainGame.TANK_PI and not MainGame.TANK_PI.stop:  # 根据开关的状态来判断是否调用坦克的移动
                MainGame.TANK_PI.move()  # 调用坦克的移动
                # 调用判断碰撞的方法
                MainGame.TANK_PI.hitWalls()  # 墙壁碰撞
                MainGame.TANK_PI.hitEnemyTank()  # 我方坦克碰撞
            # 调用子弹渲染链表方法
            self.blitBullent()
            # 调用渲染敌方子弹列表的一个方法
            self.blitEnemyBullet()
            # 调用爆炸效果展示的方法
            self.displayExplodes()
            time.sleep(0.02)  # 休眠延迟循环的速度
            pygame.display.update()  # 屏幕刷新

    # 创建我方坦克的方法
    def creatMyTank(self):
        MainGame.TANK_PI = MyTank(250, 400)  # 坦克的位置赋值
        # 创建音乐对象
        music = Music('img/start.wav')
        music.play()  # 播放

    # 创建敌方坦克
    def creatEnemyTank(self):
        top = 100
        speed = random.randint(3, 6)  # 随机速度

        for i in range(MainGame.EnemyTank_count):  # 遍历5次
            speed = random.randint(3, 6)  # 随机速度
            left = random.randint(1, 7)  # 随机位置
            eTank = EnemyTank(left * 100, top, speed)
            MainGame.EnemyTank_list.append(eTank)  # append() 是在链表后增加元素

    # 创建墙壁方法
    def creatWalls(self):
        for i in range(6):
            wall = Wall(145 * i, 240)
            MainGame.Wall_list.append(wall)

    # 将墙壁加载到窗口
    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.Wall_list.remove(wall)

    # 将坦克加入到窗口
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:  # 判断坦克是否活着
                eTank.displayTank()
                eTank.randMove()  # 坦克移动的方法
                eTank.hitWalls()  # 调用坦克与墙壁碰撞方法
                eTank.hitMyTank()  # 敌方坦克与我方坦克的碰撞
                eBullet = eTank.shot()  # 调用敌方坦克的射击
                if eBullet:
                    # 将子弹存储敌方子弹列表
                    MainGame.Enemy_bullet_list.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)

    # 遍历子弹展示
    def blitBullent(self):
        for bullet in MainGame.Bullent_list:
            if bullet.live:
                bullet.displayBullet()  # 子弹的展示
                bullet.bulletmove()  # 让子弹移动
                bullet.hitEnemyTank()  # 调用我方子弹和敌方坦克的碰撞
                bullet.hitWalls()  # 调用我方子弹是否碰撞墙壁
            else:
                MainGame.Bullent_list.remove(bullet)  # 子弹从链表里移除

    def blitEnemyBullet(self):  # 绘制敌方坦克子弹
        for eBullet in MainGame.Enemy_bullet_list:
            # 如果子弹还活着，绘制出来，否则，直接从列表中移除该子弹
            if eBullet.live:
                eBullet.displayBullet()
                # 让子弹移动
                eBullet.bulletmove()
                # 敌方子弹是否撞墙
                eBullet.hitWalls()
                # 敌方坦克子弹打中我发坦克
                if MainGame.TANK_PI and MainGame.TANK_PI.live:
                    eBullet.hitMyTank()

            else:
                MainGame.Enemy_bullet_list.remove(eBullet)

    def displayExplodes(self):  # 遍历爆炸效果
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.Explode_list.remove(explode)

    def getTextSurface_1(self, text):  # 左上角文字绘制类型1
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 30)  # 选择字体
        textSurface = font.render(text, True, MainGame.COLOR_RED)  # 函数返回文字的画布
        return textSurface

    def getTextSurface_2(self, text):  # 左上角文字绘制类型2
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 20)  # 选择字体
        textSurface = font.render(text, True, MainGame.COLOR_WHITE)  # 函数返回文字的画布
        return textSurface

    def getEvent(self):  # 获取所有事件 鼠标事件 键盘事件
        eventList = pygame.event.get()  # 获取所有事件
        for event in eventList:  # 对事件进行判断
            # 判断evevt.type 是否QUIT，如果是退出的话，直接调用程序结束方法
            if event.type == pygame.QUIT:
                self.endGame()
            # 判断事件类型是否为按键按下，如果是判断按键是那个
            if event.type == pygame.KEYDOWN:

                # 点击m按键让我方坦克重生
                if event.key == pygame.K_m and not MainGame.TANK_PI:
                    # 创建我方坦克的方法
                    self.creatMyTank()
                #点击b按键怎加敌人
                if event.key==pygame.K_b:
                    # 创建敌方坦克的方法
                    self.creatEnemyTank()

                if MainGame.TANK_PI and MainGame.TANK_PI.live:
                    if event.key == pygame.K_LEFT:  # 事件发生后完成 1.修改坦克的方向 2.修改坦克的位置（调用移动方法）
                        print("坦克向左移动")
                        MainGame.TANK_PI.direction = 'L'  # 修改direction
                        MainGame.TANK_PI.stop = False  # 修改开关的状态
                    elif event.key == pygame.K_RIGHT:
                        print("坦克向右移动")
                        MainGame.TANK_PI.direction = 'R'
                        MainGame.TANK_PI.stop = False
                    elif event.key == pygame.K_UP:
                        print("坦克向上移动")
                        MainGame.TANK_PI.direction = 'U'
                        MainGame.TANK_PI.stop = False
                    elif event.key == pygame.K_DOWN:
                        print("坦克向下移动")
                        MainGame.TANK_PI.direction = 'D'
                        MainGame.TANK_PI.stop = False
                    elif event.key == pygame.K_SPACE:
                        print("坦克发射子弹")
                        if len(MainGame.Bullent_list) < 3:  # 控制子弹数量 如果子弹数小于三才能产生子弹
                            m = Bullet(MainGame.TANK_PI)  # 产生一个子弹
                            MainGame.Bullent_list.append(m)  # 将子弹加入链表
                            #子弹音效
                            music=Music('img/fire.wav')
                            music.play()
                        else:
                            print("子弹数量不足")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if MainGame.TANK_PI and MainGame.TANK_PI.live:
                        MainGame.TANK_PI.stop = True  # 修改坦克移动状态

    def endGame(self):  # 结束游戏
        print("谢谢使用")
        exit()


class BaseItem(pygame.sprite.Sprite):  # 创建一个类让他继承精灵类
    def __init__(self):
        pygame.sprite.Sprite.__init__()


class Tank(BaseItem):
    def __init__(self, left, top):  # left top为坐标
        self.images = {
            'U': pygame.image.load('img/enemy3U.gif'),
            'D': pygame.image.load('img/enemy3D.gif'),
            'L': pygame.image.load('img/enemy3L.gif'),
            'R': pygame.image.load('img/enemy3R.gif')
        }  # 字典定义加载坦克的不同方向状态的画布
        self.direction = 'U'  # 拿出对应的方向
        self.image = self.images[self.direction]  # image为字典的搜查结果 是一个surface
        ''' 
        坦克所在的方向   
        get_rect()用来获取surface的宽高返回一个Rect（）类型   
        Rect矩形结构类 包含4个结构变量left，top 宽度 高度
        '''
        self.rect = self.image.get_rect()
        self.rect.left = left  # 指定坦克初始化位置分别据X轴和Y轴的位置
        self.rect.top = top
        self.speed = 5  # 坦克的速度
        self.stop = True  # 坦克移动开关
        self.live = True  # 坦克是否还活着
        # 新增属性：记录坦克移动之前的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    def move(self):  # 坦克移动  按下方向健坦克持续移动
        # 记录移动之前的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.width < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed

    def stay(self):  # 位置还原方法
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    def hitWalls(self):  # 坦克碰撞墙壁方法
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.stay()

    def shot(self):  # 射击方法
        return Bullet(self)

    def displayTank(self):  # 坦克的显示(将坦克画布绘制到窗口)
        # 1.重新设置坦克的图片 (更具方向设置图片)
        self.image = self.images[self.direction]
        # 2.将坦克加入到窗口中
        MainGame.window.blit(self.image, self.rect)  # window.blit（）把图片粘贴在window之上


class MyTank(Tank):
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)  # 调用父类方法

    # 新增主动碰撞到敌方坦克的方法
    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):  # eTank是敌方坦克self是自己
                self.live = False
                eTank.live = False
                MainGame.EnemyTank_list.remove(eTank)  # 把敌方坦克从链表里移除
                # 调用爆炸效果类
                explode1 = Explode(eTank)
                explode2 = Explode(self)
                # 将爆炸效果加入到链表
                MainGame.Explode_list.append(explode1)
                MainGame.Explode_list.append(explode2)



class EnemyTank(Tank):  # 敌方坦克 MyTank(Tank)子类继承父类的方法 可以直接使用
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)  # 在子类中调用父类的初始化方法
        # 图片集
        self.images = {
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif')
        }  # 字典定义加载坦克的不同方向状态的画布
        self.direction = self.randDirection()  # 拿出对应的方向
        self.image = self.images[self.direction]  # image为字典的搜查结果 是一个surface
        '''
        坦克所在的方向   
        get_rect()用来获取surface的宽高返回一个Rect（）类型   
        Rect矩形结构类 包含4个结构变量left，top 宽度 高度
        '''
        self.rect = self.image.get_rect()
        self.rect.left = left  # 指定坦克初始化位置分别据X轴和Y轴的位置
        self.rect.top = top
        self.speed = 2  # 坦克的速度
        self.stop = True  # 坦克移动开关
        self.step = 20  # 步数属性用来控制坦克的随机移动

    def randDirection(self):  # 生成随机数返回不同的方向
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    # 随机移动
    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()  # 重新调用方向
            self.step = 20  # 复位步数
        else:
            self.move()
            self.step -= 1

    def shot(self):  # 随机射击
        num = random.randint(1, 1000)
        if num <= 20:
            return Bullet(self)

    def hitMyTank(self):  # 碰撞到我方坦克
        if MainGame.TANK_PI and MainGame.TANK_PI.live:
            if pygame.sprite.collide_rect(self, MainGame.TANK_PI):
                # 让敌方坦克停下
                self.stay()


class Bullet(BaseItem):  # 子弹类
    def __init__(self, tank):
        self.image = pygame.image.load('img/enemymissile.gif')  # 加载子弹图片
        self.diection = tank.direction  # 位置
        self.rect = self.image.get_rect()  # 获取图片的rect  image为画布
        if self.diection == 'U':  # 对rect进行赋值
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2  # 子弹的位置
            self.rect.top = tank.rect.top - self.rect.height
        elif self.diection == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.diection == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.diection == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2

        self.speed = 7  # 子弹的速度

        self.live = True  # 标记子弹的状态

    def bulletmove(self):  # 子弹的移动
        if self.diection == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.diection == 'D':
            if self.rect.top <= MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.diection == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.diection == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False

    def displayBullet(self):  # 子弹的展示
        MainGame.window.blit(self.image, self.rect)  # 展示子弹

    # 我方子弹碰撞坦克方法
    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):  # self就是子弹
                # 调用爆炸效果类
                explode = Explode(eTank)
                # 将爆炸效果加入到链表
                MainGame.Explode_list.append(explode)
                self.live = False  # 如果打中那子弹和坦克修改状态
                eTank.live = False

    # 敌方子弹与我发子弹的碰撞
    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.TANK_PI):
            explode = Explode(MainGame.TANK_PI)  # 产生爆炸状态，并加入到爆炸效果列表中
            MainGame.Explode_list.append(explode)  # 爆炸效果加入到链表
            self.live = False  # 修改子弹状态
            MainGame.TANK_PI.live = False  # 修改我方坦克状态

    # 子弹与墙壁的碰撞
    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):  # 判断碰撞
                # 修改子弹的live属性
                self.live = False
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live = False


class Explode():  # 爆炸效果
    def __init__(self, tank):
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif'),
        ]  # 爆炸效果的集合
        self.image = self.images[self.step]
        self.live = True

    def displayExplode(self):  # 展示爆炸效果
        if self.step < len(self.images):  # 防止越界
            MainGame.window.blit(self.image, self.rect)  # rect 为位置
            self.image = self.images[self.step]  # 修改爆炸图片
            self.step += 1
        else:
            self.step = 0
            self.live = False

    def display(self):
        pass


class Wall():  # 墙壁类型
    def __init__(self, left, top):
        self.image = pygame.image.load('img/steels.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 3  # 墙壁的生命值

    def displayWall(self):  # 展示墙壁
        MainGame.window.blit(self.image, self.rect)


# 音效类
class Music():
    def __init__(self, fileName):
        self.fileName = fileName
        pygame.mixer.init()  # 初始化模块
        pygame.mixer.music.load(self.fileName)  # 加载音乐文件

    def play(self):  # 开始播放音乐
        pygame.mixer.music.play(loops=0)  # 播放音乐


MainGame().startGame()
