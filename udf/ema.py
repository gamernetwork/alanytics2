import sys
import json
from agent import Agent, Handler
import udf_pb2

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()

# Computes the exponential moving average of the data it receives.
# The options it has are:
#    alpha - EMA decrease weighting
#    field - the field to operate on
#    as - the name of the average field, default 'avg'
#
class EMAHandler(Handler):

    class state(object):
        def __init__(self, alpha):
            self.alpha = alpha
            self._avg = 0.0

        def update(self, value):
            self._avg = self._avg + self.alpha * ( value - self._avg )
            return self._avg

        def snapshot(self):
            return {
                    'alpha' : self.alpha,
                    'avg' : self._avg,
            }

        def restore(self, data):
            self.alpha = int(data['alpha'])
            self._avg = float(data['avg'])

    def __init__(self, agent):
        self._agent = agent
        self._field = None
        self._alpha = 0.0
        self._as = 'avg'
        self._state = {}


    def info(self):
        response = udf_pb2.Response()
        response.info.wants = udf_pb2.STREAM
        response.info.provides = udf_pb2.STREAM
        response.info.options['field'].valueTypes.append(udf_pb2.STRING)
        response.info.options['alpha'].valueTypes.append(udf_pb2.DOUBLE)
        response.info.options['as'].valueTypes.append(udf_pb2.STRING)

        return response

    def init(self, init_req):
        success = True
        msg = ''
        for opt in init_req.options:
            if opt.name == 'field':
                self._field = opt.values[0].stringValue
            elif opt.name == 'alpha':
                self._alpha = opt.values[0].doubleValue
            elif opt.name == 'as':
                self._as = opt.values[0].stringValue

        if self._field is None:
            success = False
            msg += ' must supply field name'
        if self._as == '':
            success = False
            msg += ' invalid as name'

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]

        return response

    def snapshot(self):
        data = {}
        for group, state in self._state.iteritems():
            data[group] = state.snapshot()

        response = udf_pb2.Response()
        response.snapshot.snapshot = json.dumps(data)

        return response

    def restore(self, restore_req):
        success = False
        msg = ''
        try:
            data = json.loads(restore_req.snapshot)
            for group, snapshot in data.iteritems():
                self._state[group] = EMAHandler.state(0)
                self._state[group].restore(snapshot)
            success = True
        except Exception as e:
            success = False
            msg = str(e)

        response = udf_pb2.Response()
        response.restore.success = success
        response.restore.error = msg

        return response

    def begin_batch(self, begin_req):
        raise Exception("not supported")

    def point(self, point):
        response = udf_pb2.Response()
        response.point.CopyFrom(point)
        response.point.ClearField('fieldsInt')
        response.point.ClearField('fieldsString')
        response.point.ClearField('fieldsDouble')

        value = point.fieldsDouble[self._field]
        if point.group not in self._state:
            self._state[point.group] = EMAHandler.state(self._alpha)
        avg = self._state[point.group].update(value)

        response.point.fieldsDouble[self._as] = avg
        self._agent.write_response(response)

    def end_batch(self, end_req):
        raise Exception("not supported")


if __name__ == '__main__':
    a = Agent()
    h = EMAHandler(a)
    a.handler = h

    logger.info("Starting Agent")
    a.start()
    a.wait()
    logger.info("Agent finished")

