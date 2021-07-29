import pygame
import math
import os
from settings import PATH,PATH_two,RED,GREEN  # import路徑一,路徑二,紅色,綠色


pygame.init()
# 讀取圖片 
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))  

class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path = PATH
        self.path_index = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]
    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)
        

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        pygame.draw.rect(win,GREEN,[self.x-20,self.y-30,20,5])
        pygame.draw.rect(win,RED,[self.x,self.y-30,20,5])

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        x_a,y_a = self.path[self.path_index]        # 當前座標
        x_b,y_b = self.path[self.path_index + 1]    # 下一個座標
        distance = math.sqrt((x_a - x_b)**2 + (y_a - y_b)**2)  # 兩個座標的距離
        max_count = int(distance / self.stride)                # 最大步數

        if(self.move_count < max_count):
            uni_vec_x = (x_b - x_a) / distance  # x的單位向量
            uni_vec_y = (y_b - y_a) / distance  # y的單位向量
            delta_x = uni_vec_x * self.stride   
            delta_y = uni_vec_y * self.stride

            self.x += delta_x
            self.y += delta_y

            self.move_count += 1
        else:
            self.path_index += 1  # 進入下一個點
            self.move_count = 0
            
               
            
class EnemyGroup:
    def __init__(self):
        self.campaign_count = 0
        self.campaign_max_count = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = []  # don't change this line until you do the EX.3 
    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # 先判斷有沒有還沒產生的敵人 且 count有沒有等於120                   
        if(len(self.reserved_members) != 0 and self.campaign_max_count == self.campaign_count):                   
            self.expedition.append(self.reserved_members[0])                  
            self.reserved_members.pop(0)
            self.campaign_count = 0
        # 判斷有沒有還沒產生的敵人 且 count有沒有小於120    
        elif(len(self.reserved_members) != 0 and self.campaign_max_count > self.campaign_count):
            self.campaign_count += 1
            
    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        for i in range(num):
            self.reserved_members.append(Enemy())  # 將還沒產生的敵人先放到reserved_members這個list裡
            self.campaign_count = 120 
            
    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)





