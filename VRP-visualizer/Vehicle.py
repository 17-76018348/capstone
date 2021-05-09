import pygame
from pygame.locals import *
from pygame.rect import *

import numpy as np

class Vehicle():
    # input
    # pygame screen
    # 시작 좌표
    # 목표 좌표 리스트
    # 차량 id
    # (도형 반지름)
    def __init__(self,screen,start,target,id,rad=25):
        self.id = id # 차량 번호
        self.speed = 5 # 차량 속도
        self.node_current = np.array(start) # 시작 위치(depot)
        self.targets = np.array(target) # 목표 노드
        self.set_target() # 속도 설정
        self.screen = screen # 스크린 설정

        self.vehicle = Rect(list(self.node_current-[rad,rad])+[2*rad,2*rad]) # (도형 객체) 생성
        
        pygame.draw.ellipse(self.screen,(0, 0, 255),self.vehicle) # (도형 객체) 출력
        
    def move(self):
        # target이 존재할 때
        if len(self.targets)!=0:
            # target으로 속도 설정
            self.set_target()
            # (도형 객체) 이동
            self.vehicle.move_ip(self.velocity)
            # (도형 객체)의 현재 좌표를 저장
            self.node_current = self.vehicle.center
        # (도형 객체) 출력
        pygame.draw.ellipse(self.screen,(0, 0, 255),self.vehicle)
        
        
    def isArrived(self):
        # target이 존재할 때
        if len(self.targets)!=0:
            # target까지의 거리 측정
            distance = self.node_current - self.targets[0]
            distance = np.linalg.norm(distance)
            # 거리가 1 tick당 이동량 보다 작을 때
            if distance < self.speed:
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
        # 객체로부터 target으로의 벡터 연산 및 0방지용 epsilon 추가
        self.velocity = (np.array(self.targets[0])-np.array(self.node_current)+[0.0001,0.0001])
        # 단위 벡터만 추출하고 speed값 곱하여 저장
        self.velocity = list((self.velocity/np.linalg.norm(self.velocity))*self.speed)

