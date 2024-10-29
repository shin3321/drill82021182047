from pico2d import *
from state_machine import *

class Idle:
    @staticmethod
    def enter(boy, e):
        if right_up(e) or left_down(e):
            boy.action = 3
            boy.frame = 0
            boy.face_dir = 1

        elif left_up(e) or right_down(e) or start_event(e):
            boy.action = 2
            boy.frame = 0
            boy.face_dir = -1

        boy.dir = 0

        #시작 시간을 기록
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) %1
        if get_time() - boy.start_time > 1:
            #이벤트 발생
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class Sleep:
    @staticmethod
    def enter(boy, e):
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 1
        pass
    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
             boy.image.clip_composite_draw(
                boy.frame * 100, 300, 100, 100, 3.141592/2, '', #좌우 상하 반전은 하지 않겠다
                boy.x-25, boy.y-25, 100, 100)

        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100, -3.141592 / 2, '',  # 좌우 상하 반전은 하지 않겠다
                boy.x + 25, boy.y - 25, 100, 100)

        pass

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
            boy.dir = 1

        elif left_down(e) or right_up(e):
            boy.action = 0
            boy.dir = -1

        boy.frame = 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 2
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100, boy.x , boy.y)



        pass


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3

        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)   # 어떤 객체를 위한 상태 머신인지 알려 줄 필요가 있다
        self.state_machine.start(Idle)        # 객체를 생설한 것이 아니고 직접 클래스 이름을 사용
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep},
                Run :{right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Sleep: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle}
            }
        )


    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        #input event
        #state_machine event로 변경해 줘야 됨
        self.state_machine.add_event(
            ('INPUT', event)
        )
        pass

    def draw(self):
        self.state_machine.draw(self)

