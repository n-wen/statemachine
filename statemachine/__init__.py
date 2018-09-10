from transitions import Machine as _Machine
import asyncio
import logging

logger = logging.getLogger(__name__)


class Machine(_Machine):
    state_to = None
    sm_transitions = []
    path_cache = {}
    transitions_path = {}
    trigger_cache = {}
    state_lock = False
    trigger_params = {}

    def __init__(self, transitions, **kwargs):
        self.sm_transitions = transitions
        _transitions = []
        for t in transitions:
            _transitions.append({
                'trigger': t['trigger'].__name__,
                'source': t['source'],
                'dest': t['dest']
            })
            if t['source'] not in self.transitions_path:
                self.transitions_path[t['source']] = []
            self.transitions_path[t['source']].append(t['dest'])
            self.trigger_cache['{}2{}'.format(t['source'], t['dest'])] = t['trigger']
        if 'initial' in kwargs:
            self.state_to = kwargs['initial']
        super(Machine, self).__init__(transitions=_transitions, **kwargs)
        self.find_all_path()

    async def change_state_to(self, to):
        if not self.state_lock:
            self.state_to = to
        else:
            raise Exception("state lock exists.")
        while self.state != to:
            await asyncio.sleep(1)


    def get_trigger(self, source, dest):
        return self.trigger_cache['{}2{}'.format(source, dest)]

    def find_path(self, start, stop):
        def _find_path(graph, start, end, path=None):
            path = path + [start] if path is not None else [start]
            if start == end:
                return path
            if start not in graph:
                return None
            for node in graph[start]:
                if node not in path:
                    newpath = _find_path(graph, node, end, path)
                    if newpath: return newpath
            return None

        paths = _find_path(self.transitions_path, start, stop)
        ret = []
        for index, state in enumerate(paths[:-1]):
            ret.append(self.get_trigger(state, paths[index + 1]))
        return ret

    def find_all_path(self):
        for start in self.states:
            for stop in self.states:
                if start == stop:
                    continue
                self.path_cache['{}2{}'.format(start, stop)] = self.find_path(start, stop)

    def path(self, from_state, to_state):
        return self.path_cache["{}2{}".format(from_state, to_state)]

    async def run(self):
        """
        maintain state consistency
        :return:
        """
        while True:
            try:
                await asyncio.sleep(1)
                if self.state == self.state_to:
                    continue
                self.state_lock = True
                for fun in self.path(self.state, self.state_to):
                    r = None
                    if fun in self.trigger_params and self.trigger_params.get(fun, None):
                        r = fun(**self.trigger_params.get(fun))
                    else:
                        r = fun()
                    if r:  # set new state
                        getattr(self, fun.__name__).__call__()
                        self.state_lock = False
                    else:
                        break
            except Exception as e:
                logger.error(" error:{}".format(e))
