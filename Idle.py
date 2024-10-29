class Idle:
     @staticmethod
     def enter(boy):
        print('Boy Idle Enter')
     @staticmethod
     def exit(boy):
        print('Boy Idle Exit')
     @staticmethod
     def do(boy):
        boy.frame = (boy.frame + 1) % 8
     @staticmethod
     def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)