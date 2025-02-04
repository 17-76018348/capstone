# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import vrpAPI_pb2 as vrpAPI__pb2


class SimulatorMessagesStub(object):
  """request the simulator can send to the simulator
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.isReady = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/isReady',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.BoolMessage.FromString,
        )
    self.isReadyForOffline = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/isReadyForOffline',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.BoolMessage.FromString,
        )
    self.isReadyForOnline = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/isReadyForOnline',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.BoolMessage.FromString,
        )
    self.loadJson = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/loadJson',
        request_serializer=vrpAPI__pb2.JsonMessage.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.loadNewRequests = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/loadNewRequests',
        request_serializer=vrpAPI__pb2.JsonMessage.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.currentTimeUnit = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/currentTimeUnit',
        request_serializer=vrpAPI__pb2.TimeUnitMessage.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.pauseSimulation = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/pauseSimulation',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.DoubleMessage.FromString,
        )
    self.continueSimulation = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/continueSimulation',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.DoubleMessage.FromString,
        )
    self.testConnection = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/testConnection',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.setCurrentSolution = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/setCurrentSolution',
        request_serializer=vrpAPI__pb2.JsonMessage.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.shutdown = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/shutdown',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.startSimulation = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/startSimulation',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.DoubleMessage.FromString,
        )
    self.startOfflineSimulation = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/startOfflineSimulation',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.DoubleMessage.FromString,
        )
    self.startOnlineSimulation = channel.unary_unary(
        '/vrpAPI.SimulatorMessages/startOnlineSimulation',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.DoubleMessage.FromString,
        )


class SimulatorMessagesServicer(object):
  """request the simulator can send to the simulator
  """

  def isReady(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def isReadyForOffline(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def isReadyForOnline(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def loadJson(self, request, context):
    """send json object as a string
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def loadNewRequests(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def currentTimeUnit(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def pauseSimulation(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def continueSimulation(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def testConnection(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def setCurrentSolution(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def shutdown(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def startSimulation(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def startOfflineSimulation(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def startOnlineSimulation(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SimulatorMessagesServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'isReady': grpc.unary_unary_rpc_method_handler(
          servicer.isReady,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.BoolMessage.SerializeToString,
      ),
      'isReadyForOffline': grpc.unary_unary_rpc_method_handler(
          servicer.isReadyForOffline,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.BoolMessage.SerializeToString,
      ),
      'isReadyForOnline': grpc.unary_unary_rpc_method_handler(
          servicer.isReadyForOnline,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.BoolMessage.SerializeToString,
      ),
      'loadJson': grpc.unary_unary_rpc_method_handler(
          servicer.loadJson,
          request_deserializer=vrpAPI__pb2.JsonMessage.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'loadNewRequests': grpc.unary_unary_rpc_method_handler(
          servicer.loadNewRequests,
          request_deserializer=vrpAPI__pb2.JsonMessage.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'currentTimeUnit': grpc.unary_unary_rpc_method_handler(
          servicer.currentTimeUnit,
          request_deserializer=vrpAPI__pb2.TimeUnitMessage.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'pauseSimulation': grpc.unary_unary_rpc_method_handler(
          servicer.pauseSimulation,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.DoubleMessage.SerializeToString,
      ),
      'continueSimulation': grpc.unary_unary_rpc_method_handler(
          servicer.continueSimulation,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.DoubleMessage.SerializeToString,
      ),
      'testConnection': grpc.unary_unary_rpc_method_handler(
          servicer.testConnection,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'setCurrentSolution': grpc.unary_unary_rpc_method_handler(
          servicer.setCurrentSolution,
          request_deserializer=vrpAPI__pb2.JsonMessage.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'shutdown': grpc.unary_unary_rpc_method_handler(
          servicer.shutdown,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'startSimulation': grpc.unary_unary_rpc_method_handler(
          servicer.startSimulation,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.DoubleMessage.SerializeToString,
      ),
      'startOfflineSimulation': grpc.unary_unary_rpc_method_handler(
          servicer.startOfflineSimulation,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.DoubleMessage.SerializeToString,
      ),
      'startOnlineSimulation': grpc.unary_unary_rpc_method_handler(
          servicer.startOnlineSimulation,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.DoubleMessage.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'vrpAPI.SimulatorMessages', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class SolverMessagesStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.acceptRequest = channel.unary_unary(
        '/vrpAPI.SolverMessages/acceptRequest',
        request_serializer=vrpAPI__pb2.JsonMessage.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.notifyEndOffline = channel.unary_unary(
        '/vrpAPI.SolverMessages/notifyEndOffline',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.notifyEndOnline = channel.unary_unary(
        '/vrpAPI.SolverMessages/notifyEndOnline',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.sendBestSolution = channel.unary_unary(
        '/vrpAPI.SolverMessages/sendBestSolution',
        request_serializer=vrpAPI__pb2.JsonMessage.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.testConnection = channel.unary_unary(
        '/vrpAPI.SolverMessages/testConnection',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.Empty.FromString,
        )
    self.getTimeUnit = channel.unary_unary(
        '/vrpAPI.SolverMessages/getTimeUnit',
        request_serializer=vrpAPI__pb2.Empty.SerializeToString,
        response_deserializer=vrpAPI__pb2.TimeUnitMessage.FromString,
        )


class SolverMessagesServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def acceptRequest(self, request, context):
    """send the request that is now mark as accepted
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def notifyEndOffline(self, request, context):
    """notify the simulator that the solver finished the offline
    and that no more offline solution will come
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def notifyEndOnline(self, request, context):
    """notify the simulator that the solver finished the online
    and that no more online solution will come
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def sendBestSolution(self, request, context):
    """a json message with the new best solution send to the simulator
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def testConnection(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getTimeUnit(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SolverMessagesServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'acceptRequest': grpc.unary_unary_rpc_method_handler(
          servicer.acceptRequest,
          request_deserializer=vrpAPI__pb2.JsonMessage.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'notifyEndOffline': grpc.unary_unary_rpc_method_handler(
          servicer.notifyEndOffline,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'notifyEndOnline': grpc.unary_unary_rpc_method_handler(
          servicer.notifyEndOnline,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'sendBestSolution': grpc.unary_unary_rpc_method_handler(
          servicer.sendBestSolution,
          request_deserializer=vrpAPI__pb2.JsonMessage.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'testConnection': grpc.unary_unary_rpc_method_handler(
          servicer.testConnection,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.Empty.SerializeToString,
      ),
      'getTimeUnit': grpc.unary_unary_rpc_method_handler(
          servicer.getTimeUnit,
          request_deserializer=vrpAPI__pb2.Empty.FromString,
          response_serializer=vrpAPI__pb2.TimeUnitMessage.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'vrpAPI.SolverMessages', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
