"""
Created on Wednesday January 3 16:29:18 2018

@author: scandaele

"""

from CarrierClass import Carrier
from ScenarioClass import Scenario

import pprint
import copy
import json


class Solution:
	def __init__(self):
		self.data = {"NumberOfSolutions" : 0, "Solutions" : [], "SolutionsNotValid" : [], 'UserSolution' : []}
		
		# 원래 none이었는데 임시로 했다
		self.realDurationPerTimeUnit = 60
		self.realTimeUnit = "Second"
		self.carrierUnit = "Second"
		self.convertDic = {'Second':1, 'Minute':60, 'Hour':3600}
		self.acceptedRequest = [] # a tab with the accepted/rejected request and the time when it was decided by the solver
		self.acceptedrequest = set({})
		self.displayFile = 'browserDisplay/solutionToDisplay.json'

	def acceptRequest(newRequest, scenario):
		"""
		receive a request message initially send by the solver, indicating if the request
		is accepted or not, and what was the submission time

		return True if the request is correctly added to the requests accepted
		return a string error message describing what happened otherwise
		"""
		# check if the request exists in the scenario
		requestInScenario = scenario.containsRequest(newRequest)
		if requestInScenario != True:
			return requestInScenario

		for reqId in self.acceptedrequest:
			# check the request was not already accepted
			if reqId == int(newRequest['RequestId']):
				return 'ERROR: request already accepted'

		# If the request is ok, we add it to the acceptedRequest
		self.acceptedrequest.add(int(newRequest['RequestId']))
		return True


	def containsValidInitialOfflineSolution(self, scenario):
		"""
		return the last valid solution sent before the start of the online simulation
		return false otherwise
		"""
		returnValue = False
		for solution in self.data["Solutions"]:
			if solution["TimeUnitOfSubmission"] <= 0.0:
				returnValue = solution

		notServedRequest = []
		# check all offline request are in the sol
		# 
		#  ==> si offlineTime = 0 c'est impossible à satisfaire
		#      en parler à michael, qui voulait que toute les requêtes
		#      offline doivent être incluse dans la solution offline finale.
		#
		# for request in scenario.data['Requests']:
		# 	if request['TimeSlot'] == -1:
		# 		requestPresent = False
		# 		for road in solution['Routes']:
		# 			for node in solution['Routes'][road]:
		# 				if 'RequestId' in node and int(request['RequestId']) == int(node['RequestId']):
		# 					# print('Present : ', request['RequestId'])
		# 					requestPresent = True
		# 		if not requestPresent:
		# 			# return False
		# 			notServedRequest +=[request['RequestId']]

		if notServedRequest != []:
			# print(len(notServedRequest))
			# print(notServedRequest)
			return False

		return returnValue



	def deleteRequest(self, requestId, roadId):
		"""
		delete the request with id requestId from the road with roadId in the user solution
		return True if the request was in the road and was deleted
		return False otherwise
		"""


		road = self.data['UserSolution'][-1]['Routes'][roadId]
		for i in range(0, len(road)):
			if 'RequestInstanceId' in road[i] and road[i]['RequestInstanceId'] == int(requestId):
				del(self.data['UserSolution'][-1]['Routes'][roadId][i])
				return True
		return False

	def loadFileSolverSol(self, solutionFile, myGraph, carrierObj, myScenario, timeslots):
		try:
			with open(solutionFile) as sFile:
				solution = json.load(sFile)
				if self.isSolutionValid(solution, myGraph, carrierObj, myScenario, timeslots, loadedSolution = True):
					# self.acceptedrequest = set()
					# for roadId, road in solution['Routes'].items():
					# 	for node in road:
					# 		if 'RequestId' in node:
					# 			self.acceptedrequest.add(int(node['RequestId']))
					return solution
				else:
					return False
		except IOError:
			print('cannot open', solutionFile)
			return False

	def loadFile(self, solutionFile):
		try:
			with open(solutionFile) as sFile:
				solutions = json.load(sFile)
				self.data['UserSolution'] += [solutions['Solutions'][-1]]
		except IOError:
			print('cannot open', ScenarioFile)

	def newSolutionForDisplay(self, myGraph, myCarrier, timeUnit = None):
		''' Saves all the necessary solution to display the last solution with the browser map'''
		try:
			with open(self.displayFile, 'w') as f:
				if len(self.data['Solutions']) > 0:
					self.data['Solutions'][-1]['CurrentDateTime'] = self.data['Solutions'][-1]['CurrentDateTime'].replace('\n', '')
					# txtSol   = json.dumps(self.data['Solutions'][-1])
					# txtGraph = json.dumps(myGraph) 
					# txt  = "solution = '" + txtSol   + "';\n";
					# txt += "graph    = '" + txtGraph + "';\n";
					if timeUnit == None:
						timeUnit = self.data['Solutions'][-1]['TimeUnitOfSubmission']
						data = {'Graph' : myGraph, 'Solution' : self.data['Solutions'][-1], 'Vehicles': myCarrier['Vehicles'], 'CurrentTU' : timeUnit}
					else:
						data = {'Graph' : myGraph, 'Solution' : self.data['Solutions'][-1], 'Vehicles': myCarrier['Vehicles'], 'CurrentTU': timeUnit}
					f.write(json.dumps(data))


		except IOError as er:
			print('ERROR while saving last solution in file for browser display')
			print(er)

	def printLastSolution(self, short = False):
		"""
		print the last valid solution returned by the solver
		"""
		if not self.data['Solutions']:
			print('No valid solutions from the solver yet')
		else:
			if not short:
				pp = pprint.PrettyPrinter(indent = 4)
				pp.pprint(self.data['Solutions'])
			print('\n Solution resumed : --> [nodeId, requestId] -> [] -> etc... ')
			#requestServed    = []
			#requestNotServed = []

			
			for roadId in self.data['Solutions'][-1]['Routes']:
				road = ''
				for node in self.data['Solutions'][-1]['Routes'][roadId]:
					road += '['+str(node['InstanceVertexID'])+','
					if 'RequestInstanceId' in node:
						road += str(node['RequestInstanceId'])
						#requestServed += node['RequestInstanceId']
					road += ']->'
				road = road[0:-2]
				print('roadNumber '+roadId+'   : '+ road)

	def printUserSolution(self, short = False):
		if not self.data['UserSolution']:
			print('No solution from the user')
		else:
			if not short:
				pp = pprint.PrettyPrinter(indent = 4)
				pp.pprint(self.data['UserSolution'])
			print('\n Solution resumed : --> [nodeId, requestId] -> [] -> etc... ')
			for roadId in self.data['UserSolution'][-1]['Routes']:
				road = ''
				for node in self.data['UserSolution'][-1]['Routes'][roadId]:
					road += '['+str(node['InstanceVertexID'])+','
					if 'RequestInstanceId' in node:
						road += str(node['RequestInstanceId'])
					road += ']->'
				road = road[0:-2]
				print('roadNumber '+roadId+'   : '+ road)

	def getNewChargeAt(self, node, myScenario):
		"""
			return the additional charge of the vehicle when serving the requests at the node
		"""
		newCharge = 0

		if 'RequestInstanceId' in node:
			node['RequestId'] = node['RequestInstanceId']
		if 'RequestId' in node:
			request = myScenario.getRequest(node['RequestId'])
			if request is not False:
				newCharge += request['Demand']
			else:
				# try to access an unexisting request
				return False
		return newCharge

	def insertRequest(self, requestId, roadId, position, myGraph, myCarrier, myCustomer, myScenario):
		"""
		Insert the request with the id requestId into the road with id roadId
		at the position provided
		Return True if the insertion could be done without violating time constraints
		Return False otherwise
		"""
		request = None
		if not myScenario.data or not myCarrier.data or not myCustomer.data or not myGraph.data:
			print('ERROR: input files missing')
			return False

		# 현재 들어온 new request가 이미 결정된 requst인가?
		for road in self.data['UserSolution'][-1]['Routes']:
			for node in self.data['UserSolution'][-1]['Routes'][road]:
				if 'RequestInstanceId' in node and  node['RequestInstanceId'] == int(requestId):
					print('ERROR: request '+requestId+' already in road '+road)
					return False

		
		for req in myScenario.data['Requests']:
			# extract the request from the scenario
			if req['RequestId'] == int(requestId):
				request = copy.deepcopy(req)

		if request is not None:
			position = int(position)
			vehicleType = myCarrier.getVehicleType(roadId)
			previousNode = self.data['UserSolution'][-1]['Routes'][str(int(roadId)-1)][position]
			tsStart = myCustomer.getTimeSlotOfTimeUnit(previousNode['DepartureTime'])

			newNode = {'ArrivalTime':None, 'ServiceTime':None, 'DepartureTime':None,
				'InstanceVertexID':None, 'RequestInstanceId':None}
			newNode['RequestInstanceId'] = request['RequestId']
			newNode['InstanceVertexID'] = request['Node']
			travelTime = myCarrier.getTravelTime(previousNode['InstanceVertexID'], 
				newNode['InstanceVertexID'], vehicleType, tsStart)
			travelTime = travelTime * self.convertDic[self.realTimeUnit]/self.convertDic[myCarrier.data['Unit']]
			travelTime = travelTime / self.realDurationPerTimeUnit
			newNode['ArrivalTime'] = previousNode['DepartureTime'] + travelTime
			newNode['ServiceTime'] = newNode['ArrivalTime']

			if position >= len(self.data['UserSolution'][-1]['Routes'][str(int(roadId))]):
				print('ERROR: vehicles should end their roads with a depot, not a request')
				return False
			nextNode = self.data['UserSolution'][-1]['Routes'][str(int(roadId))][position]
			tsStart = myCustomer.getTimeSlotOfTimeUnit(previousNode['DepartureTime'])
			earliestDepartureTime = newNode['ServiceTime']+request['ServiceDuration']
			latestDepartureTime = myCarrier.getLatestDepartureTU(newNode['InstanceVertexID'], nextNode['InstanceVertexID'], nextNode['ArrivalTime'], vehicleType, myCustomer)
			if latestDepartureTime != False and latestDepartureTime >= earliestDepartureTime:
				# the time for nodes before and after don't have to be modified
				newNode['DepartureTime'] = latestDepartureTime
				self.data['UserSolution'][-1]['Routes'][str(roadId)].insert(position, newNode)
			else:
				# else we minimize the time constraint violation without moving other requests
				newNode['DepartureTime'] = earliestDepartureTime
				self.data['UserSolution'][-1]['Routes'][str(roadId)].insert(position, newNode)



	def isValidToPreviousSol(self, newSolution, oldSolution, myScenario):
		"""
			Check if the newSolution is valid with regard to the previous solution.
			Check if it the newSolution does not change already executed road.
		"""
		timeOfSubmission = newSolution['TimeUnitOfSubmission']

		for roadId in oldSolution['Routes']:
			if roadId not in newSolution['Routes']:
				# the new sol must not erase existing road
				return False
			nodeNum = 0
			while nodeNum < len(oldSolution['Routes'][roadId]):
				nsNode = newSolution['Routes'][roadId][nodeNum]
				osNode = oldSolution['Routes'][roadId][nodeNum]

				if osNode['ArrivalTime'] > timeOfSubmission:
					# the rest of the node is after the timeOfSubmission
					break
				else:
					if osNode['ArrivalTime'] != nsNode['ArrivalTime']:
						return False
					if osNode['InstanceVertexID'] != nsNode['InstanceVertexID']:
						return False

					if osNode['DepartureTime'] < timeOfSubmission:
						if osNode['DepartureTime'] != nsNode['DepartureTime']:
							return False
						if osNode['RequestId'] != nsNode['RequestId']:
							return False

					else:
						if 'RequestId' in osNode:
							req = myScenario.getRequest(osNode['RequestId'])
							if req['TimeWindow']['start'] < timeOfSubmission:
								if osNode['RequestId'] not in nsNode['RequestId']:
									# the request has started to be served 
									return False
				nodeNum += 1
			return True

	def isSolutionValid(self, solution, myGraph, carrierObj, myScenario, timeslots, loadedSolution = False):
		validSolution = True

		# build the set of request that were revealed when the solution was submitted
		# revealedRequestSet = set()
		# solutionTU = solution['TimeUnitOfSubmission']
		# for request in myScenario.data['Requests']:
		# 	if request['RevealTime'] < solutionTU:
		# 		revealedRequestSet.add(request['RequestId'])

		# # check if the request served are request that were revealed
		# for roadId, road in solution['Routes'].items():
		# 	for node in road:
		# 		if 'RequestId' in node:
		# 			if node['RequestId'] not in revealedRequestSet:
		# 				validSolution = False

		if validSolution:
			if not self.isServingAcceptedRequest(solution):
				print("이건뭔문제")
				validSolution = False
			#안걸림..!
			# if the solution is loaded from a file, it can not served the accepted request.
			if validSolution or loadedSolution:
				for roadId, road in solution['Routes'].items():
					if not carrierObj.getVehicleOfId(roadId):
						print("id겟팅해오는데 문제")
						validSolution = False
						break;
					if not self.isRoadValid(roadId, road, myGraph, carrierObj, myScenario, timeslots):
						print("road자체가 valid하지않음")
						validSolution = False
						break;
		return validSolution

	def isRoadValid(self, roadId, road, myGraph, carrierObj, myScenario, timeslots):
		"""
			Verify if a single road is valid
			input: 
				1) road id =veh. id =우리가 가정. =예) 1~100 --> 루프물
				2) road = road id 따른 Value 값들 
				3) myGraph, carrierObj, myScenario ==> 그대로.. 
				4) timeslot은 myCustomer.data["TimeSlots"]  


		"""

		# ruturn을 false를 했는데,, 어떤 문장떄문에?>?
		vehicleType = carrierObj.data['Vehicles'][roadId]['VehicleType']
		previousNode = None
		vehicleCharge = 0
		requestServed = {}
		for node in road:

			if 'RequestId' in node:
				# The request must be served one time max
				if node['RequestId'] in requestServed:
					print('request served multiple times')
					return False
				else:
					requestServed[node['RequestId']] = True

			

			# The load of the road must not exceed vehicle's capacity
			additionalCharge = self.getNewChargeAt(node, myScenario)
			if additionalCharge is False:
				print('ask load of unexisting request')
				print(str(road))
				print(node)
				return False
			vehicleCharge += additionalCharge
			vehicleCapacity = carrierObj.getCapacityOfVehicle(roadId)

			# for 문 돌려서 하면됨. 
			# 체크포인트

			if vehicleCharge > vehicleCapacity:
				print('capacity of vehicle {} is exceeded, capacity : {}  charge {}'.format(roadId, vehicleCapacity, vehicleCharge))
				return False

			if previousNode is None:
				pass
			else:
				if not self.isTravelTimeValid(previousNode, node, carrierObj, vehicleType, timeslots):
					print('travel time not respected')
					return False
				#이부분 주석다시 풀어야함 체크포인트
				pass
				# if not self.isTimeWindowValid(node, myScenario, carrierObj):
				# 	return False
			previousNode = node
		return True

	def isServingAcceptedRequest(self, solution):
		"""
			return true if the solution serve all the accepted request
			false otherwise
			The solution can thus contains request not yet accepted or rejected
		"""
		serveAcceptedRequests = True
		requestInRoad = False
		# for each accepted request
		for requestId in self.acceptedrequest:
			requestInRoad = False

			for roadId in solution['Routes']:
				# look in each road if the request appears
				for node in solution['Routes'][roadId]:
					if 'RequestId' in node and int(node['RequestId']) == requestId:
						requestInRoad = True
						break
				if requestInRoad:
					break

			if not requestInRoad:
				# if accepted request not in solution, return false
				serveAcceptedRequests = False
				break

		return serveAcceptedRequests
						


#퍼포먼스 측정용
	def isTimeWindowValid(self, node, myScenario, carrierObj):
		"""
			Check if the timeWindows of the requests served at the given node of the road
			are respected
		"""

		if 'RequestInstanceId' in node:
			node['RequestId'] = node['RequestInstanceId']
		if 'RequestId' in node:
			request = myScenario.getRequest(node['RequestId'])
			if node['ArrivalTime'] > (request['TimeWindow']['end']-request['ServiceDuration']):
				return False
			elif node['DepartureTime'] - node['ServiceTime'] < request['TimeWindow']['ServiceDuration']:
				return False
			return True
		else:
			# it serves no request at this node
			if node['ArrivalTime'] > node['DepartureTime'] or node['ArrivalTime'] > node['ServiceTime']:
				return False
			if node['ServiceTime'] > node['DepartureTime']:
				return False
			return True

	def isTravelTimeValid(self, oldNode, newNode, carrierObj, vehicleType, timeslots):
		"""
			Check if the travel time between two nodes is not too short
			가설1: too short 면 좋은거임!! 그래서 
			단순 short인지 check하는 함수임 (유력)

			가설2:too short면 안좋은거임?

			어떤 time unit에서 실제 소요시간이 과연, normal time보다 작을지. 작으면 false!
			실제가 더 오래걸려야 한다.

		"""
		timeDiff = (newNode['ArrivalTime']-oldNode['DepartureTime'])*self.realDurationPerTimeUnit
		timeDiff = timeDiff*self.convertDic[self.realTimeUnit]/self.convertDic[carrierObj.data['Unit']]
		oldNodeId = oldNode['InstanceVertexID']
		newNodeId = newNode['InstanceVertexID']
		timeslot = 0

		# find the timeslot of derpature time
		for ts in timeslots:
			if ts > oldNode['DepartureTime']:
				timeslot += 1
			else:
				break
		normalTime = carrierObj.getTravelTime(oldNodeId, newNodeId, vehicleType, timeslot)
		if timeDiff < normalTime:
			# 실제 소요시간 < 예측시간
			if normalTime == 0 or timeDiff/normalTime < 0.999:
				return False
			else:
				return True
		else:
			return True

	def newUserSolution(self):
		if not not self.data['Solutions']:
			self.data['UserSolution'] = copy.deepcopy([self.data['Solutions'][-1]])

	def updateBestSolution(self, newSolution):
		''' solution is added as the last valide solution '''
		self.data["NumberOfSolutions"] += 1
		self.data["Solutions"] += [newSolution]

		# for road in newSolution['Routes']:
		# 	for node in newSolution['Routes'][road]:
		# 		if 'RequestId' in node:
		# 			self.acceptedrequest.add(int(node['RequestId']))




