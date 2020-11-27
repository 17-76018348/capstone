#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 12:49:36 2017

@author: simon
"""

import queue
import threading
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
import time



class UIMthread(threading.Thread):

    def __init__(self, commandQueue, eventCommand, eventSMQueue, eventLock):
        threading.Thread.__init__(self)
        self.commandQueue = commandQueue
        self.eventCommand = eventCommand
        self.eventSMQueue = eventSMQueue
        self.eventLock = eventLock
        self.commandCompleter = WordCompleter(['addVehicles',
        'close',
        'continue',
        'createNewSolution',
        'currentStatus',
        'deleteRequest',
        'deleteVehicles',
        'generateScenario',
        'insertRequest',
        'loadCarrier',
        'loadCustomer',
        'loadFile',
        'loadGraph',
        'loadNewSolution',
        'loadScenario',
        'loadUserSolutions',
        'newRequest',
        'pause',
        'printCarrier',
        'printCustomers',
        'printGraph',
        'printScenario',
        'printSolverSolution',
        'printUserSolution',
        'saveUserSolution',
        'saveScenario',
        'saveSolutions',
        'sendCarrierToSolver',
        'sendCustomersToSolver',
        'sendAll',
        'sendFile',
        'sendGraphToSolver',
        'setComputationTime',
        'setVehicleCapacity',
        'setLogFile',
        'setOfflineTime ',
        'showVehicles',
        'showVehicleType',
        'startOfflineSimulation',
        'startOnlineSimulation',
        'stopSimulation',
        'test',
        'testConnection',
        'solve' ], ignore_case = True)
        
    def run(self):
        exitFlag = False
        while not exitFlag:
            
            #TODO: rajouter un lock sur la fonction input pour pas faire buger un éventuel print dans la commande précédente
            # auto make 자동완성 기능
            # save inserted command to history.txt
            command = prompt('--:', history = FileHistory('history.txt'),
                auto_suggest = AutoSuggestFromHistory(),
                completer = self.commandCompleter,
                )

            # program exit
            if command.split() == ['close']:
                exitFlag = True
            
            # enter mode except exit mode
            if command != '':
                """
                Event 
                set -> make flag 1
                clear -> make flag 0
                wait -> if flag = 1 return else if flag = 0 waiting for 1
                isSet -> return flag
                """
                # share data permission lock
                self.eventLock.acquire()

                # set thread event flag 0
                self.eventCommand.clear()
                self.commandQueue.put(command)

                # set thread event flag 1
                self.eventSMQueue.set()
                self.eventLock.release()
                # share data permission release

                # if flag = 1 return else if flag = 0 wait for being 1
                self.eventCommand.wait()





class guiInput():
    def __init__(self, commandQueue, eventCommand, eventSMQueue, eventLock, guiQueue):
        self.commandQueue = commandQueue
        self.eventCommand = eventCommand
        self.eventSMQueue = eventSMQueue
        self.eventLock = eventLock
        self.guiQueue = guiQueue

    def sendCommand(self, command):
        '''send a command to the simulator'''
        self.eventLock.acquire()
        self.eventCommand.clear()
        self.commandQueue.put(command)
        self.eventSMQueue.set()
        self.eventLock.release()
        self.eventCommand.wait()

    def getNextMessage(self):
        ''' waits for a message to be available in the queue and returns it '''
        while self.guiQueue.empty():
            pass
        return self.guiQueue.get()

    def getMessage(self):
        '''returns the first message in the queue, None if empty '''
        if not self.guiQueue.empty():
            return self.guiQueue.get()
        else:
            return None
            
        
    
