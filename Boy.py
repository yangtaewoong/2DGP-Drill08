from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_a

from state_machine import StateMachine, space_down, time_out, right_down, left_down, left_up, right_up, start_event, a_key_down


class Idle:
    @staticmethod
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.dir = -1
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.dir = 1
            boy.face_dir = 1

        boy.frame = 0
        boy.dir = 0

        #시작시간을 기록
        #boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        print('Boy Idle Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        #if get_time() - boy.start_time > 5:
            #이벤트를 발생
            #boy.state_machine.add_event(('TIME_OUT', 0))


    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:   #오른쪽 방향을 보고 있는 상태
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                     3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
                                          -3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)

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
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir *3
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame*100, boy.action* 100, 100, 100,
            boy.x, boy.y
        )
        pass

class AutoRun:
    @staticmethod
    def enter(boy, e):
        if a_key_down(e):
            boy.action = 1 if boy.face_dir == 1 else 0
            boy.dir = boy.face_dir
            boy.frame = 0
            boy.start_time = get_time()
        elif left_down(e) or left_up(e):
            boy.dir = -1
            boy.face_dir = -1
            boy.action = 0
        elif right_down(e) or right_up(e):
            boy.dir = 1
            boy.face_dir = 1
            boy.action = 1
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 6

        if boy.x < 10 or boy.x > 790:
            boy.dir *= -1
            boy.face_dir = boy.dir
            boy.action = 1 if boy.dir == 1 else 0

        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))
            if boy.dir == 1:
                boy.action = 3
            elif boy.dir == -1:
                boy.action = 2

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            boy.x, boy.y,
            200,200
        )
        pass


class Boy:
    image = None

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.action = 3
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            # 상태 변환 표기
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, a_key_down: AutoRun},
                Run: {right_down: Idle, left_down:Idle, right_up: Idle, left_up:Idle},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
                AutoRun: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle}

            }
        )
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')

    def update(self):
        self.state_machine.update()
        self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
            # INPUT : 실제입력이벤트값
        # TIME_OUT : 시간 종료

    def draw(self):
        self.state_machine.draw()
