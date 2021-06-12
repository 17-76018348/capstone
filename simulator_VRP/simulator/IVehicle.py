import pygame
from pygame.locals import *
from pygame.rect import *

import numpy as np

class Vehicle():
    '''
    input :
        pygame screen
        시작 좌표
        목표 좌표 리스트
        차량 id
        (도형 반지름)
    '''
    def __init__(self,screen,start,target,id,color, rad=25):
        self.id = id # 차량 번호
        self.speed = 5 # 차량 속도
        self.color = color
        self.node_current = np.array(start) # 시작 위치(depot)
        self.targets = np.array(target) # 목표 노드
        self.set_target() # 속도 설정
        self.screen = screen # 스크린 설정
        self.node_previous = self.node_current
        self.count_done = 0

        # (차량 이미지) 오픈
        self.img_deliver = pygame.image.load("delivery.png")
        # (차량 이미지) 최적화
        self.img_deliver.convert()
        # (차량 이미지) 속성값 추출
        self.rect = self.img_deliver.get_rect()
        # (차량 이미지) 초기 위치 설정
        self.rect.center = start[0],start[1]
        # (차량 이미지) 각도, 크기 조절 - 사용 안함
        self.img_deliver = pygame.transform.rotozoom(self.img_deliver, 0, 1)

        # (차량 이미지) 출력
        self.screen.blit(self.img_deliver,self.rect)

        #self.vehicle = Rect(list(self.node_current-[rad,rad])+[2*rad,2*rad]) # (도형 객체) 생성
        #pygame.draw.ellipse(self.screen,(0, 0, 255),self.vehicle) # (도형 객체) 출력
        
    def move(self):
        # target이 존재할 때
        if len(self.targets)!=0:
            # target으로 속도 설정
            self.set_target()
            # (차량 이미지) 이동
            self.rect = self.rect.move(self.velocity) #self.vehicle.move_ip(self.velocity)
            # (차량 이미지)의 현재 좌표를 저장
            self.node_current = self.rect.center
            

        # (차량 이미지) 출력
        self.screen.blit(self.img_deliver,self.rect)    
        #pygame.draw.ellipse(self.screen,(0, 0, 255),self.vehicle)
        
        
    def isArrived(self):
        # target이 존재할 때
        if len(self.targets)!=0:
            # target까지의 거리 측정
            distance = self.node_current - self.targets[0]
            distance = np.linalg.norm(distance)
            # 거리가 1 tick당 이동량 보다 작을 때
            if distance < self.speed:
                self.count_done += 1
                # 경로 출력용 노드 저장
                self.node_previous = self.targets[0]
                # 도착한 target을 target 리스트에서 삭제
                self.targets=self.targets[1:]
                # 도착하였으므로 true 반환
                return True
            # 거리가 1 tick당 이동량 큼 = 도착하지 않았으므로 false 반환
            else:
              return False
        # 처리할 target이 존재하지 않으므로 false 반환
        else:
            return True
    
    def set_target(self):
        # 객체로부터 target으로의 벡터 연산 및 zero 방지용 epsilon 추가
        self.velocity = (np.array(self.targets[0])-np.array(self.node_current)+[0.0001,0.0001])
        # 단위 벡터만 추출하고 speed값 곱하여 저장
        self.velocity = list((self.velocity/np.linalg.norm(self.velocity))*self.speed)

    def draw_path(self):
        if len(self.targets) > 0:
           pygame.draw.line(self.screen, self.color, self.node_current, self.targets[0], 5)
        if len(self.targets) > 1:
            for idx in range(len(self.targets)-1):
                pygame.draw.line(self.screen, self.color, self.targets[idx], self.targets[idx+1], 5)
