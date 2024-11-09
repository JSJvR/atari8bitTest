import os
import hashlib
import os
import os.path
import re
import json
from enum import Enum
from .shared import clear_dir
from .shared import files_to_utf8

state_file = './state.json'

class Action(Enum):
    EXTRACT_ATR = 'atr', lambda: print("Eaxtract")
    DELETE_UTF8 = 'atascii', lambda: clear_dir('./utf8')
    WRITE_UTF8 = 'utf8', lambda: files_to_utf8('./atascii', './utf8')
    COMMIT = 'commit', None
    PUSH = 50, None
    WAIT = None, lambda: print('Nothing to do. Waiting')
    ERROR = None, None
    
    def __new__(cls, *args, **kwds):
          value = len(cls.__members__) + 1
          obj = object.__new__(cls)
          obj._value_ = value
          return obj
    
    def __init__(self, key, recon_action):
          self.key = key
          self.recon_action = recon_action

def md5checksum(file):
    f = open(file,'rb')
    checksum = hashlib.md5(f.read()).hexdigest()
    f.close()
    return checksum

def scandir(path, output, pattern = '.*'):
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file() and not re.search(pattern, entry.name) is None:
                checksum = md5checksum(entry.path)
                output.append({
                    'name': entry.name, 
                    'checksum': checksum
                })
    output.sort(key=lambda x: x['name'])

def get_current_state():
    state = {
        'atr': list(),
        'atascii': list(),
        'utf8': list()
    }
    
    # ATR
    scandir('./atr', state['atr'], '\\.atr$')
    
    # ATASCII
    scandir('./atascii', state['atascii'])
    
    # UTF-8
    scandir('./utf8', state['utf8'])

    # COMMIT MSG
    commit = './utf8/COMMIT.MSG'
    if os.path.isfile(commit):
        f = open(commit, encoding='utf-8')
        msg = f.read()
        f.close()
        state['commit'] = {
            'msg': msg
        }
    
    return state

def load_state():
    f = open(state_file, mode='r')
    state = json.loads(f.read())
    f.close()
    return state

def save_state(state):
    f = open(state_file, mode='w')
    f.write(json.dumps(state, indent=4))
    f.close()

def check_state(): 
    stored_state = load_state()
    current_state = get_current_state()

    if not current_state['atr']:
        return Action.ERROR
    
    if (not stored_state['atr']) or current_state['atr'][0] != stored_state['atr'][0]:
        return Action.EXTRACT_ATR

    if (stored_state['atascii'] != current_state['atascii']):
        return Action.DELETE_UTF8
    
    if not current_state['utf8']:
        return Action.WRITE_UTF8

    if (stored_state['commit'] != current_state['commit']):
        return Action.COMMIT

    return Action.WAIT

def update_state(key):
    stored_state = load_state()
    current_state = get_current_state()

    stored_state[key] = current_state[key]
    save_state(stored_state)

def tick():
    action = check_state()
    match action:
        case Action.DELETE_UTF8:
            clear_dir('./utf8')
        case Action.WRITE_UTF8:
            files_to_utf8('./atascii', './utf8')
        case Action.WAIT:
            print('Nothing to do. Waiting')
        case _:
            print(f'Don\'t know what to do with {action}')
    
    if not action.key is None:
        update_state(action.key)

    return action

def init(clobber = False):

    if clobber or not os.path.isfile(state_file):
        state = get_current_state()
        save_state(state)
    else:
        print(f'Skipping initialization. State file "{state_file}" already exists')        

if __name__ == '__main__':
    init(False)
    print(tick())