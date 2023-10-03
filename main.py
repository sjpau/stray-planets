import pygame
import sys
import debug
import moderngl
import defs.finals as finals
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode(finals.display_resolution['1280x720'], pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption(finals.CAPTION)
from array import array
from defs.lvl import get_states
from loader.loader import glsl_to_string
from utils.utils import surface_to_gl_texture

class Game(object):
    def __init__(self, gl_program, gl_context, render_obj, state):
        self.done = False
        self.gl_program = gl_program
        self.gl_context = gl_context
        self.render_obj = render_obj
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.state = state
        self.desired_next_state = self.state.desired_next_state
        self.surface = pygame.display.get_surface()

    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self, state):
        self.state.on_exit()
        state.preload(state_persistent_data=self.state.state_persistent_data)
        if state.ready:
            self.state.done = False
            persistent = self.state.persist
            self.state = state
            self.state.startup(persistent)
            self.state.on_enter()

    def update(self, dt):
        self.desired_next_state = self.state.desired_next_state
        if self.state.quit:
            self.state.state_persistent_data.save()
            self.done = True
        elif self.state.done:
            self.state.done = False
            self.flip_state(states[self.desired_next_state])
            self.switch_music = True
        if self.state.handle['level update']:
            self.state.update(dt)

    def draw(self):
        canvas = self.state.draw()
        self.surface.blit(pygame.transform.scale(canvas, self.surface.get_size()), (0,0))
        if debug.status:
            debug.display(self.surface, int(self.clock.get_fps()))
        return self.surface

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            surf = self.draw()
            frame_tex = surface_to_gl_texture(surf, self.gl_context)
            frame_tex.use(0)
            self.gl_program['tex'] = 0
            self.render_obj.render(mode=moderngl.TRIANGLE_STRIP)

            pygame.display.flip()
            frame_tex.release()

def main() -> None:
    context = moderngl.create_context()

    quad_buffer = context.buffer(data=array('f', 
    [
        -1.0, 1.0, 0.0, 0.0,  # toplfet
        1.0, 1.0, 1.0, 0.0,   # topright
        -1.0, -1.0, 0.0, 1.0, # bottomleft
        1.0, -1.0, 1.0, 1.0,  # bottomright
    ]
    ))
    vertex_shader = glsl_to_string('shaders/vertex.glsl')
    fragment_shader = glsl_to_string('shaders/fragment.glsl')

    program = context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
    render_obj = context.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'textcoord')])
    states = get_states()

    app = Game(program, context, render_obj, states['blank']) 
    app.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
