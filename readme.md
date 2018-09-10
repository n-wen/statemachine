State Machine
=============

A tool to automatically manage states. Based on [transitions](https://github.com/pytransitions/transitions).

example:

```python
from statemachine import Machine

states = ['a', 'b', 'c']

def a2b():
    print('transit a to b')
    if random.random() < 0.5:
        print("transit success.")
        return True
    print("transit fail.")
    return False


def b2c():
    print('transit b to c')
    if random.random() < 0.5:
        print("transit success.")
        return True
    print("transit fail.")
    return False

def c2a(p1):
    print('transit c to a, params: {}'.format(p1))
    if random.random() < 0.5:
        print("transit success.")
        return True
    print("transit fail.")
    return False

transitions = [
    {'trigger': a2b, 'source': 'a', 'dest': 'b'},
    {'trigger': b2c, 'source': 'b', 'dest': 'c'},
    {'trigger': c2a, 'source': 'c', 'dest': 'a'},
]

machine = Machine(states=states, transitions=transitions, initial='a')

async def change_state():
    while True:
        await asyncio.sleep(2)
        state_to = random.choice(states)
        machine.trigger_params[c2a] = {
            'p1': 'hi'
        }
        await machine.change_state_to(state_to)

async def main():
    asyncio.ensure_future(change_state())
    f = asyncio.ensure_future(machine.run())
    await f


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

Notes:

- Auto generated paths of all nodes(states) use not optimal algorithm.
- Every arcs(trigger function in transitions) must return a bool indicates success or fail of changing state.
- Trigger function can cancel state changing( await machine.change_state_to() ) by setting machine.cancel_changing_state to True.
- await machine.change_state_to() return bool indicates success of changing state.
