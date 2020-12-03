# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:55:02 2017

@author: scandaele
"""

import threading
import time
import json
import queue
from simulatorAPIClasses import simulatorAPI
import sys

# Thread to manage an offline simulation
class simulationOfflineThread(threading.Thread):

    def __init__(self, scenario, downQueue, upQueue, logFileLock, simuAPI, simulationQueue, eventSMQueue, eventLock, myCarrier, mySolutions, myCustomer, myGraph,logFile = None):
        threading.Thread.__init__(self)
        self.eventSMQueue = eventSMQueue
        self.eventLock = eventLock
        self.scenario = scenario
        self.downQueue = downQueue
        self.upQueue = upQueue
        self.logFile = logFile
        self.logFileLock = logFileLock
        self.pauseSimulation = False
        self.simuAPI = simuAPI
        self.simulationQueue = simulationQueue

        self.myCarrier=myCarrier
        self.mySolutions=mySolutions
        self.myCustomer=myCustomer 
        self.myGraph =myGraph   

        
    def run(self):
        timeUnit = -1
        
        exitFlag = False
        endOfflineMsgSent = False

        OfflineTime = self.scenario.data['OfflineTime']

        totalPauseTime = 0.0
        
        startPause = 0
        endPause = 0

        # Wait for the solver to be connected before sending requests
        #while not self.simuAPI.testConnection():
        #    time.sleep(1)

        # send all the offline requests of the scenario

        # for request in self.scenario.data['Requests']:
        #     if request['RevealTime'] == -1:
        #         msg = json.dumps(request)
        #         msg = '{"NewRequests" : ' + msg + "}"
        #         self.simuAPI.sendNewRequestsJsonToSolver(msg)
        #         if self.logFile is not None:
        #             self.logFileLock.acquire()
        #             localtime = time.asctime( time.localtime(time.time()) )
        #             lf = open(self.logFile, 'a')
        #             lf.write(localtime + ' : ' + 'mesage to solver : \n' + msg + '\n\n')
        #             lf.close()
        #             self.logFileLock.release()
        
        # wait the solver to be ready for the simulation
        #while not self.simuAPI.isReadyForOffline():
        #    pass

        print('   The solver is ready, offline simulation will start very shortly')

        # The simulator API decide the starTime, we wait until this time to start
        startTime = 0
        self.upQueue.put(('startTimeOffline', startTime))
        self.eventLock.acquire()
        self.eventSMQueue.set()
        self.eventLock.release()

        while not exitFlag:

            # check if solver confirm the pause
            # while not self.simuAPI.pauseMessageQueue.empty():
            #     message = self.simuAPI.pauseMessageQueue.get()
            #     if message[0] == "OK":
            #         self.simuAPI.pauseMessageThread.join()
            #         self.simuAPI.pauseMessageThread = None
            #         startPause = message[1]
            #         endPause = sys.float_info.max
            #         self.pauseSimulation = True
            #         self.upQueue.put(('startOfflinePause',startPause))
            #         self.eventLock.acquire()
            #         self.eventSMQueue.set()
            #         self.eventLock.release()
            

            while not self.downQueue.empty():
                message = self.downQueue.get()
                
                # order to start a pause
                if message == 'pause' :
                    self.simuAPI.sendPauseMessageT()
                # order to end a pause   
                elif message == 'continue':
                    if True == True:
                        
                        print('   Simulation not in pause')

                # send an empty solution to the solver
                elif message == 'sendEmptySolutionWithTOS':
                    self.simuAPI.setCurrentSolution(json.dumps('{"TimeOfSubmission":'+str(timeUnit)+'}'))

                # order to close the simulator
                elif message == 'close':
                    self.simuAPI.sendCloseMessage()
                    exitFlag = True

                # order to close the simulator
                elif message == 'stopSimulation':
                    self.simuAPI.sendCloseMessage()
                    exitFlag = True

                # simulation manager ask to close the thread
                elif message == 'closeThread':
                    exitFlag = True

                # if rpc error, end the simulation
                elif message == 'RpcError : close':
                    exitFlag = True
            #downq 사용이 끝남

            while not self.simulationQueue.empty():
                message = self.simulationQueue.get()
                # 알고리즘 돌릴지 
                if message == 'sendTimeUnit':
                    tu = (time.time() - startTime - OfflineTime)
                    self.simuAPI.timeUnitQueue.put(tu/OfflineTime)
                # 아예 끝낼지
                elif message == 'close':
                    print('   SIMULATION OFFLINE THREAD :: close from simulationQueue')
                    exitFlag = True

                elif message.startswith("logFile "):
                    self.logFile = message.replace('logFile ', '', 1)
            print("확인용")
            exitFlag = True
            endOfflineMsgSent = True
            
            # 작업중 -- 체크포인트!!!!

            # 1. valid한 solution을 만들기
            # 2. if문을 이용해서 constraint을 만족하면 True , true, true..  솔루션.data의 valid solution에 삽입
            # 3. json으로 출력
            
            # 1) request의 사이즈를 확인
            # 2) 루프물 돌림.

            temp=[]
            for request in self.scenario.data['Requests']:
                if request['RevealTime'] == -1:
                    # 3) if문 --> isRoadvalid함수 사용
                    # 3-1) 초기화 -->특정 veh를 넣어준다
                    # roadId는 루프돌며순회하는 인덱스임
                    # 개수는?-->veh.의 개수이니까. carrier 파일에서 가져와야함.

                    # road는 딕셔너리의 배열. index는 position!
                    # 밑에 변수들 다 초기화해줘야함.
                    # 현재선언함. 초기화 해야함!!
                    # 이유는 depot이 1이란걸 알기때문에, 만약 그렇지않다면 소스코드 좀 수정해야함.
                    

                    for roadId in self.myCarrier.data['Vehicles']:
                        # 2대의 차량이 request를 처리하면 초기화하고 다음 request 처리
                        if len(temp) == 2:
                            temp = []
                        # 1 vehicle 1 request 이라서
                        if roadId in temp:
                            continue 


                        
                        # 0으로 다초기화
                        nodeId=1
                        # 참고 맨마지막 1은 시작하는 timeslot이고 getTimeSlotOfTimeUnit이 메서드로 호출가능한 부분
                        arrivaltime= self.myCarrier.getTravelTime(nodeId,request['Node'],self.myCarrier.getVehicleType(roadId),1)
                        departuretime= request['ServiceDuration'] + arrivaltime
                        road = [{"ArrivalTime" : 0, "DepartureTime": 0 , "NodeId": nodeId,"InstanceVertexID":nodeId}]
                        road.insert(1,{"ArrivalTime" : arrivaltime+departuretime, "DepartureTime": 0 , "NodeId": nodeId, "InstanceVertexID":nodeId})
                        road.insert(1,{"ArrivalTime" : arrivaltime, "DepartureTime": departuretime , "NodeId": request['Node'], "InstanceVertexID":request['Node'], "RequestId": request['RequestId'],"RequestInstanceId":request['RequestId']})
                        # vehicle마다 arrival time, departuretime 달라짐.
                        # node id는 1.. 

                        
                        if self.mySolutions.isRoadValid(roadId,road,self.myGraph,self.myCarrier, self.scenario,self.myCustomer.data["TimeSlots"]):
                            # Constraint 통과시 추가됨.
                            self.mySolutions.data['Solutions'].append({"TimeUnitOfSubmission":0, "Routes": {roadId: road}})
                            temp.append(roadId)
                            print(self.mySolutions.data['Solutions'], "\n")
                            break



                        # 3-1여기에다가 roadid를 삽입해야함


                        # 3-2 vertex id
                        # 3-3 departure time, arrival time


                    

            
            
            # 4) first fit이라서 처음 리턴되는거 그대로 솔루션에 때려박기
            # 5) 우선순위는 완성되지 않은 rotue(road) > 기존에 완성된 road(route)







            self.upQueue.put(('endOfOfflineSimulation',))
            self.eventLock.acquire()
            self.eventSMQueue.set()
            self.eventLock.release()
            # check if we reach the end of the offline time
            # if ( time.time() - startTime - totalPauseTime ) >= OfflineTime:
            #     if not self.pauseSimulation and not endOfflineMsgSent:
            #         endOfflineMsgSent = True
            #         self.upQueue.put(('endOfOfflineSimulation',))
            #         self.eventLock.acquire()
            #         self.eventSMQueue.set()
            #         self.eventLock.release()

            # elif time.time() > endPause:
            #     self.pauseSimulation = False

            
                            
class simulationOnlineThread(threading.Thread):
    
    def __init__(self, scenario, downQueue, upQueue, logFileLock, simuAPI, simulationQueue, eventSMQueue, eventLock, myCarrier, mySolutions, myCustomer, myGraph,logFile = None):
        threading.Thread.__init__(self)
        self.eventSMQueue = eventSMQueue
        self.eventLock = eventLock
        self.scenario = scenario
        self.horizonSize = myCustomer.data["HorizonSize"]
        self.downQueue = downQueue
        self.logFile = logFile
        self.logFileLock = logFileLock
        self.pauseSimulation = False
        self.simuAPI = simuAPI
        self.simulationQueue = simulationQueue
        #security margin, so that requests are available for solver at the beginning of the time unit
        self.marginTimeRequestSending = 0.2
        self.myCarrier=myCarrier
        self.mySolutions=mySolutions
        self.myCustomer=myCustomer 
        self.myGraph =myGraph
        self.downQueue = downQueue
        self.upQueue = upQueue
    def run(self):
        timeUnit = 0
        
        exitFlag = False
        ComputationTime = self.scenario.data['ComputationTime']

        totalPauseTime = 0.0
        
        startPause = 0
        endPause = 0


        numberRequestToSend = 0
        # count the number of request to send at the first time unit
        for request in self.scenario.data['Requests']:
            if request['RevealTime'] == 0:
                numberRequestToSend += 1

        #while not self.simuAPI.isReadyForOnline():
        #    pass

        print('   The solver is ready, online simulation will start very shortly')

        # The simulator API decide the starTime, we wait until this time to start
        startTime = 0
        self.upQueue.put(('startTimeOnline', startTime))
        self.eventLock.acquire()
        self.eventSMQueue.set()
        self.eventLock.release()

        while not exitFlag:

            #통과예상
            # while not self.simuAPI.pauseMessageQueue.empty():
            #     message = self.simuAPI.pauseMessageQueue.get()
            #     if message[0] == "OK":
            #         self.simuAPI.pauseMessageThread.join()
            #         self.simuAPI.pauseMessageThread = None
            #         endPause = sys.float_info.max
            #         startPause = message[1]
            #         self.pauseSimulation = True
            #         self.upQueue.put(('startOnlinePause',startPause))
            #         self.eventLock.acquire()
            #         self.eventSMQueue.set()
            #         self.eventLock.release()
            #통과예상
            while not self.downQueue.empty():
                message = self.downQueue.get()
                
                if message == 'pause' :
                    self.simuAPI.sendPauseMessageT()

                elif message == 'continue':
                    if True == True:
                        if self.pauseSimulation == True:
                            endPause = self.simuAPI.sendContinueMessage()
                            totalPauseTime +=  endPause - startPause
                            self.upQueue.put(('endOnlinePause',endPause))
                            self.eventLock.acquire()
                            self.eventSMQueue.set()
                            self.eventLock.release()
                        else:
                            print('   Simulation not in pause')

                    
                elif message.startswith('newRequest'):
                    # The simulation manager thread communicate a new Request
                    # except the TU, the validity was already verified
                    newRequest = json.loads(message.replace('newRequest ', ''))

                    # Request with a RevealTime anterior to the current Time are not inserted
                    if newRequest['RevealTime'] >= timeUnit:
                        self.upQueue.put((message,))
                        self.eventLock.acquire()
                        self.eventSMQueue.set()
                        self.eventLock.release()




                elif message == 'sendEmptySolutionWithTOS':
                    self.simuAPI.setCurrentSolution(json.dumps('{"TimeOfSubmission":'+str(timeUnit)+'}'))

                elif message == 'close':
                    self.simuAPI.sendCloseMessage()
                    exitFlag = True

                # order to close the simulator
                elif message == 'stopSimulation':
                    self.simuAPI.sendCloseMessage()
                    exitFlag = True

                # simulation manager ask to close the thread
                elif message == 'closeThread':
                    exitFlag = True

                elif message == 'RpcError : close':
                    exitFlag = True
            
            while not self.simulationQueue.empty():
                message = self.simulationQueue.get()
                if message == 'sendTimeUnit':
                    tu = (time.time() - startTime)
                    if tu >= 0:
                        self.simuAPI.timeUnitQueue.put(tu/ComputationTime)
                    else :
                        print('   ERROR: should not have negative time unit in online simulation')

                elif message == 'close':
                    exitFlag = True

                elif message.startswith("logFile "):
                    self.logFile = message.replace('logFile ', '', 1)
            
            # test the beginning of a new time unit
            if (time.time() - startTime - totalPauseTime) >= timeUnit * ComputationTime - self.marginTimeRequestSending * numberRequestToSend :
                
                if not self.pauseSimulation:
                    numberRequestToSend = 0
                    endPause = 0
                    startPause = 0

                    self.upQueue.put(('newTimeUnit', timeUnit))
                    self.eventLock.acquire()
                    self.eventSMQueue.set()
                    self.eventLock.release()
                    
                    newcharge=0

                    for request in self.scenario.data['Requests']:
                        if request['RevealTime'] > timeUnit+1:
                            pass
                        if request['RevealTime'] == timeUnit + 1:
                            numberRequestToSend += 0.5
                        if request['RevealTime'] == timeUnit: 
                            # new request
                            # first fit 알고리즘
                            # request fetching 
			                # The load of the road must not exceed vehicle's capacity
                            #체크포인트
                        
                            print("firstfit제발돌아가라")
                            newcharge = request['Demand']
                            for roadid in self.myCarrier.data['Vehicles']:

                                vehicleCapacity= self.myCarrier.getCapacityOfVehicle(roadid)
                                if newcharge <= vehicleCapacity:
                                    vehicleCapacity-=newcharge

                                    #valid한지 check
                                    self.mySolutions.insertRequest(request['RequestId'],roadid,0, self.myGraph,self.myCarrier,self.myCustomer,self.scenario)

                                    break
                            # msg = json.dumps(request)
                            # msg = '{"NewRequests" : ' + msg + "}"
                            # self.simuAPI.sendNewRequestsJsonToSolver(msg)
                            # if self.logFile is not None:
                            #     self.logFileLock.acquire()
                            #     localtime = time.asctime( time.localtime(time.time()) )
                            #     lf = open(self.logFile, 'a')
                            #     lf.write(localtime + ' : ' + 'mesage to solver : \n' + msg + '\n\n')
                            #     lf.close()
                            #     self.logFileLock.release()

                    timeUnit += 1
                    if timeUnit >= self.horizonSize:  
                        self.upQueue.put(('endOfOnlineSimulation',  (time.time() - startTime - totalPauseTime)/ComputationTime))
                        self.eventLock.acquire()
                        self.eventSMQueue.set()
                        self.eventLock.release()
                    
                    

                #self.simuAPI.testConnection()

            elif time.time() > endPause:
                self.pauseSimulation = False  
