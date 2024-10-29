#event( 종류 뮨자열, 실제 값 )
from sdl2 import *

def start_event(e):
    return e[0] == 'START'

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

#상태 머신을 처리, 관리해 주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o  #boy의 self가 전달이 됨 self.o 상태머신과 연결된 캐릭터 객체
        self.event_que = [] #발생하는 이벤트를 담는 곳
        pass


    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def draw(self, o):
        self.cur_state.draw(self.o)
        pass

    def update(self):
        #현재 상태를 업데이트 해 줘야 됨
        self.cur_state.do(self.o)  # Idle.do()
        #이벤트가 발생했는지 확인하고 거기에 따라서 상태 변환을 수행
        if self.event_que: #리스트에 요소가 있으면 true
            e = self.event_que.pop(0) #리스트 어펜드 -> 맨 뒤에 추가, 꺼낼 때는 맨 앞을 꺼내야 됨
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e): #e가 지금 check_event이면? space_dawn(e) ?
                    self.cur_state.exit(self.o, e)
                    print(f'    exit from{self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    print(f'    enter into {self.cur_state}')
                    return


    def start(self, start_state):
        #현재 상태를 시작 상태로 만듦
        self.cur_state = start_state   #Idle
        self.cur_state.enter(self.o, ('START', 0)) #더미 이벤트
        print(f'    enter into {self.cur_state}')


    def add_event(self, e):
        self.event_que.append(e) #상태 머신용 이벤트 추가
        print(f'    DEBUG: new event {e} is added.')
        pass

    def handle_event(self, event):
        pass

