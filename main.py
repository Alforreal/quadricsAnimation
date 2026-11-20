from manim import *
import numpy as np


SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
FPS = 120 # set so high to be able to slow down animations with less reprecussions
MUNIT_WIDTH = 14.22
MUNIT_HEIGHT = 8
POINT_COLOUR = BLUE_C
LINE_COLOUR_3D = GREEN_C
LINE_COLOUR_2D = PURE_RED
TEXT_COLOUR = BLACK
ANGLE_COLOUR = BLUE_E

def get_len(mobject):
    return (mobject.get_right()[0] - mobject.get_left()[0])

def get_height(mobject):
    return (mobject.get_top()[1] - mobject.get_bottom()[1])


# Deprecated function!
def better_sigmoid_base(a, x, l, s):
    return a*np.exp(-1*a*(np.floor(x/s)-l/(2*s)))/(1 + a*np.exp(-1*a*(np.floor(x/s)-l/(2*s))))**2

# Also deprecated function! Use general_easing_sigmoid
def better_sigmoid_angle(a, n, t, s, m = 360, fps = FPS): # a - amplitude [-], n - variable [degrees], t - duration [seconds], m - total rotation [degrees]
    l = t*fps # Conversion from seconds to frames
    k = np.arange(l)
    sum = better_sigmoid_base(a, k, l, s).sum()
    return m/sum * better_sigmoid_base(a, n, l, s) # The function is cumulative! So to use it, set angle = 0, then do angle += better_sigmoid_angle(...)

    '''
    Full mathematical formula in LaTex, try copy-pasting in Desmos:
    \frac{m}{\sum_{n=0}^{l-1}\left(\frac{a\cdot e^{-a\left(n-\frac{l}{2}\right)}}{\left(1+e^{-a\left(n-\frac{l}{2}\right)}\right)^{2}}\right)}\frac{a\cdot e^{-a\left(\left\lfloor x \right\rfloor-\frac{l}{2}\right)}}{\left(1+e^{-a\left(\left\lfloor x \right\rfloor-\frac{l}{2}\right)}\right)^{2}}\left\{0\le x\le l\right\}
    
    Here n is the same as n in the funciton, and x is continuous, hence the flooring
    Fun fact: calculating the integral for the function should get the value of m, but if you put the formula above into an integral, you won't get
    the properly correct answer. Funnily enough if you replace all the n's in the equation with x's you will get the correct value.
    Desmos shenanigans amirite?)
    '''

def general_easing_sigmoid(a, t, m, s, x, fps=FPS): # a - amplitude, t - duration [s], m - maximum value, s - frames per step, n - variable
    l=t*fps
    return m / (1 + np.exp(-a*(np.floor(x/s)-l/(2*s))))
    '''
    Formula in LaTex:
    \frac{m}{1+e^{-a\left(\operatorname{floor}\left(\frac{x}{s}\right)-\frac{l}{2s}\right)}}\left\{0\le x\le l\right\}
    
    In the actual function 
    It's a bit easier than the first iterations of the function, and it's a bit more general, so it helps quite a bit. 
    '''


class NewIntroLine(Scene):
    
    def construct(self):
        start_point = np.array([0, 0, 0])
        end_point = np.array([1, 1, 0])
        moved_point_scale = np.array([2, 2, 0])
        
        line = Line(start=start_point, end=end_point, color=LINE_COLOUR_2D)
        self.play(Create(line))
        self.wait(1)
        self.play(line.animate.put_start_and_end_on(start_point, moved_point_scale))
        step = 1 # number of frames per render
        i = 0 # starting value for the frame
        runtime = 2 # duration of animation
        while i < runtime*FPS:
            angle = general_easing_sigmoid(a=0.06, x=i, t=runtime, s=step, m=360) * DEGREES
            rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                        [np.sin(angle), np.cos(angle), 0],
                                        [0, 0, 1]])
            self.play(line.animate.put_start_and_end_on(start_point, rotation_matrix @ moved_point_scale), run_time = step/FPS, rate_func=linear)
            i += step


        shift_positions = [np.array([-2, 0, 0]), np.array([0, -2, 0]), np.array([2, 0, 0]), np.array([0, 2, 0])]
        new_point_start = start_point
        new_point_end = moved_point_scale
        for i in range(0, 4):
            new_point_start += shift_positions[i]
            new_point_end += shift_positions[i]
            self.play(line.animate.put_start_and_end_on(new_point_start, new_point_end), run_time=0.5)

        self.wait(0.5)
        self.play(Uncreate(line), run_tme=1.5)
        self.wait(1)

class NewIntroShapes(Scene):
    def construct(self):
        pos_rect = np.array([-2, 0, 0])
        scale_rect = 2
        # position_list=[
        #     [pos_rect[0]-scale_rect/2, pos_rect[1]-scale_rect/2, 0], # Bottom left
        #     [pos_rect[0]-scale_rect/2, pos_rect[1]+scale_rect/2, 0], # Top left
        #     [pos_rect[0]+scale_rect/2, pos_rect[1]-scale_rect/2, 0], # Bottom right
        #     [pos_rect[0]+scale_rect/2, pos_rect[1]+scale_rect/2, 0] # Top right
        # ]
        rect = Rectangle()
        triangle = Triangle()
        circle = Circle()

        self.play(Create(rect))

class BasicShapeIntro(ThreeDScene):
    def construct(self):
        cube_size = 2
        graph_x_length = 10.5
        graph_y_length = 10.5
        graph_z_length = 6.5

        initial_rotation_phi = 75 * DEGREES
        initial_rotation_theta = 30 * DEGREES
        rotation_rate = 0.03
        self.set_camera_orientation(theta=initial_rotation_theta, phi=initial_rotation_phi) #  
        
        Graph = ThreeDAxes(
            x_range=(-graph_x_length/2, graph_x_length/2, cube_size),
            y_range=(-graph_y_length/2, graph_y_length/2, cube_size),
            z_range=(-graph_z_length/2, graph_z_length/2, cube_size),
            x_length=graph_x_length,
            y_length=graph_y_length,
            z_length=graph_z_length,
            axis_config={'include_tip': True},
            z_axis_config={'include_tip': True},
        )
        
        Graph.set_color(TEXT_COLOUR)

        Cube = [np.array([cube_size, 0, 0]), #0
                np.array([0, cube_size, 0]), #1
                np.array([cube_size, cube_size, 0]), #2
                np.array([0, 0, cube_size]), #3
                np.array([cube_size, 0, cube_size]), #4
                np.array([0, cube_size, cube_size]), #5
                np.array([cube_size, cube_size, cube_size]), #6
                np.array([0, 0, 0])  #7
                ]
        
        Dots = VGroup()
        for i in range(0, 8):
            Dots.add(Dot3D(point=Cube[i], color=POINT_COLOUR))
        
        Labels = VGroup(
            Text('(0, 0, 0)', font_size=24, color=TEXT_COLOUR).next_to(Dots[7], IN).rotate(angle=initial_rotation_phi, axis=[1, 0, 0]).rotate(angle=135 * DEGREES, axis=[0, 0, 1]),
            Text('(1, 1, 1)', font_size=24, color=TEXT_COLOUR).next_to(Dots[6], IN).rotate(angle=initial_rotation_phi, axis=[1, 0, 0]).rotate(angle=135 * DEGREES, axis=[0, 0, 1]),
            Text('(1, 0, 0)', font_size=24, color=TEXT_COLOUR).next_to(Dots[0], IN).rotate(angle=initial_rotation_phi, axis=[1, 0, 0]).rotate(angle=135 * DEGREES, axis=[0, 0, 1]),
            Text('(0, 1, 0)', font_size=24, color=TEXT_COLOUR).next_to(Dots[1], IN).rotate(angle=initial_rotation_phi, axis=[1, 0, 0]).rotate(angle=135 * DEGREES, axis=[0, 0, 1]),
            Text('(0, 0, 1)', font_size=24, color=TEXT_COLOUR).next_to(Dots[3], IN).rotate(angle=initial_rotation_phi, axis=[1, 0, 0]).rotate(angle=135 * DEGREES, axis=[0, 0, 1]),
            Text('(1, 1, 0)', font_size=24, color=TEXT_COLOUR).next_to(Dots[2], IN).rotate(angle=initial_rotation_phi, axis=[1, 0, 0]).rotate(angle=135 * DEGREES, axis=[0, 0, 1]),
            Text('(1, 0, 1)', font_size=24, color=TEXT_COLOUR).next_to(Dots[4], IN).rotate(angle=initial_rotation_phi, axis=[1, 0, 0]).rotate(angle=135 * DEGREES, axis=[0, 0, 1]),
            Text('(0, 1, 1)', font_size=24, color=TEXT_COLOUR).next_to(Dots[5], IN).rotate(angle=initial_rotation_phi, axis=[1, 0, 0]).rotate(angle=135 * DEGREES, axis=[0, 0, 1]),
        )

        Lines = VGroup(
            Line(start=Cube[7], end=Cube[0], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[7], end=Cube[3], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[7], end=Cube[1], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[0], end=Cube[4], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[0], end=Cube[2], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[4], end=Cube[6], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[4], end=Cube[3], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[3], end=Cube[5], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[5], end=Cube[1], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[5], end=Cube[6], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[6], end=Cube[2], buff=0, color=LINE_COLOUR_3D, stroke_width=6),
            Line(start=Cube[2], end=Cube[1], buff=0, color=LINE_COLOUR_3D, stroke_width=6)
        )

        self.begin_ambient_camera_rotation(rate=rotation_rate, about='theta')
        self.play(Create(Graph), run_time=1.5)
        self.play(FadeIn(Dots), Write(Labels), run_time=2)     
        self.play(Create(Lines), run_time=1.5)    
        self.wait(6)





class BasicShape2D(ThreeDScene):
    def construct(self):
        cube_size = 2
        graph_x_length = 12
        graph_y_length = 7
        graph_z_length = 3*cube_size + 0.5
        rotation_theta = 5 * DEGREES
        rotation_phi = -20 * DEGREES
        font_size_tex = 36
        Graph = Axes(
            x_range=(-1/2*graph_x_length+1/2*cube_size, 1/2*graph_x_length+1/2*cube_size, cube_size),
            y_range=(-1/2*graph_y_length+1/2*cube_size, 1/2*graph_y_length+1/2*cube_size, cube_size),
            x_length=graph_x_length,
            y_length=graph_y_length,
            axis_config={'include_tip': True},
        ).set_color(TEXT_COLOUR)

        label_2D_x = Graph.get_x_axis_label(Tex("x", color=TEXT_COLOUR))
        label_2D_y = Graph.get_y_axis_label(Text("y", color=TEXT_COLOUR).scale(0.7))

        Graph_3D = ThreeDAxes(
            x_range=(-1/2*graph_x_length+1/2*cube_size, 1/2*graph_x_length+1/2*cube_size, cube_size),
            y_range=(-1/2*graph_y_length+1/2*cube_size, 1/2*graph_y_length+1/2*cube_size, cube_size),
            z_range=(-graph_z_length+3/2*cube_size, 3/2*cube_size, cube_size),
            x_length=graph_x_length,
            y_length=graph_y_length,
            z_length=graph_z_length,
            axis_config={'include_tip': True},
        ).set_color(TEXT_COLOUR)

        label_3D = Graph_3D.get_z_axis_label(Tex("z", color=BLACK)).rotate(angle=180 * DEGREES, axis=[1, 0, 0])


        Cube = [np.array([1/2*cube_size, -1/2*cube_size, -cube_size]), #0
                np.array([-1/2*cube_size, 1/2*cube_size, -cube_size]), #1
                np.array([1/2*cube_size, 1/2*cube_size, -cube_size]), #2
                np.array([-1/2*cube_size, -1/2*cube_size, 0]), #3
                np.array([1/2*cube_size, -1/2*cube_size, 0]), #4
                np.array([-1/2*cube_size, 1/2*cube_size, 0]), #5
                np.array([1/2*cube_size, 1/2*cube_size, 0]), #6
                np.array([-1/2*cube_size, -1/2*cube_size, -cube_size])  #7
                ]
        
        # foreground projection of the cube:
        Lines_front = VGroup(
            Line(start=[Cube[7][0], Cube[7][1], 0], end=[Cube[0][0], Cube[0][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[7][0], Cube[7][1], 0], end=[Cube[3][0], Cube[3][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[7][0], Cube[7][1], 0], end=[Cube[1][0], Cube[1][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[0][0], Cube[0][1], 0], end=[Cube[4][0], Cube[4][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[0][0], Cube[0][1], 0], end=[Cube[2][0], Cube[2][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[4][0], Cube[4][1], 0], end=[Cube[6][0], Cube[6][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[4][0], Cube[4][1], 0], end=[Cube[3][0], Cube[3][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[3][0], Cube[3][1], 0], end=[Cube[5][0], Cube[5][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[5][0], Cube[5][1], 0], end=[Cube[1][0], Cube[1][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[5][0], Cube[5][1], 0], end=[Cube[6][0], Cube[6][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[6][0], Cube[6][1], 0], end=[Cube[2][0], Cube[2][1], 0], buff=0, color=LINE_COLOUR_2D),
            Line(start=[Cube[2][0], Cube[2][1], 0], end=[Cube[1][0], Cube[1][1], 0], buff=0, color=LINE_COLOUR_2D)
        )

        Rotation_matrix_x = np.array([[1, 0, 0],
                                     [0, np.cos(rotation_theta), -np.sin(rotation_theta)],
                                     [0, np.sin(rotation_theta), np.cos(rotation_theta)]])
        
        Rotation_matrix_y = np.array([[np.cos(rotation_phi), 0, np.sin(rotation_phi)],
                                     [0, 1, 0],
                                     [-np.sin(rotation_phi), 0, np.cos(rotation_phi)]])

        # background projection of the cube:
        Lines_back = VGroup(
            Line(start=Cube[7], end=Cube[0], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[7], end=Cube[3], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[7], end=Cube[1], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[0], end=Cube[4], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[0], end=Cube[2], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[4], end=Cube[6], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[4], end=Cube[3], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[3], end=Cube[5], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[5], end=Cube[1], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[5], end=Cube[6], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[6], end=Cube[2], buff=0, color=LINE_COLOUR_2D),
            Line(start=Cube[2], end=Cube[1], buff=0, color=LINE_COLOUR_2D)
        )

        Rotation_Tex = VGroup(
            Tex(r"$R_x(\theta)= \begin{pmatrix}1 & 0 & 0 \\0 & \cos{\theta} & -\sin{\theta} \\ 0 & \sin{\theta} & \cos{\theta}\end{pmatrix}$", font_size=font_size_tex, color=TEXT_COLOUR),
            Tex(r"$R_y(\theta)= \begin{pmatrix}\cos{\theta} & 0 & \sin{\theta} \\0 & 1 & 0\\-\sin{\theta} & 0 & \cos{\theta}\end{pmatrix}$", font_size=font_size_tex, color=TEXT_COLOUR),
            Tex(r"$R_z(\theta)= \begin{pmatrix}\cos{\theta} & -\sin{\theta} & 0 \\\sin{\theta} & \cos{\theta} & 0\\ 0 & 0 & 1\end{pmatrix}$", font_size=font_size_tex, color=TEXT_COLOUR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-1/4*MUNIT_WIDTH, 0, 0])

        self.play(Create(Lines_front))
        self.wait(1)
        self.play(Create(Graph), Write(label_2D_x), Write(label_2D_y))
        self.add_fixed_orientation_mobjects(Graph.get_x_axis(), label_2D_x)

        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()
        self.play(
            phi.animate.set_value(-93.2 * DEGREES),
            Create(Lines_back),
            Create(Graph_3D),
            Write(label_3D),
            label_2D_x.animate.shift(1/4*IN)
        )
        self.wait(1)
        self.play(
            phi.animate.set_value(0),
            Uncreate(Lines_back),
            Uncreate(Graph_3D),
            Unwrite(label_3D),
        )
        self.play(
            Unwrite(label_2D_x),
            Unwrite(label_2D_y),
            Uncreate(Graph)
        )

        self.wait(1)
        for i in range(0, 8):
            Cube[i] = Rotation_matrix_x @ Cube[i]
            Cube[i] = Rotation_matrix_y @ Cube[i]
        
        self.play(
            Lines_front[0].animate.put_start_and_end_on(start=[Cube[7][0], Cube[7][1], 0], end=[Cube[0][0], Cube[0][1], 0]),
            Lines_front[1].animate.put_start_and_end_on(start=[Cube[7][0], Cube[7][1], 0], end=[Cube[3][0], Cube[3][1], 0]),
            Lines_front[2].animate.put_start_and_end_on(start=[Cube[7][0], Cube[7][1], 0], end=[Cube[1][0], Cube[1][1], 0]),
            Lines_front[3].animate.put_start_and_end_on(start=[Cube[0][0], Cube[0][1], 0], end=[Cube[4][0], Cube[4][1], 0]),
            Lines_front[4].animate.put_start_and_end_on(start=[Cube[0][0], Cube[0][1], 0], end=[Cube[2][0], Cube[2][1], 0]),
            Lines_front[5].animate.put_start_and_end_on(start=[Cube[4][0], Cube[4][1], 0], end=[Cube[6][0], Cube[6][1], 0]),
            Lines_front[6].animate.put_start_and_end_on(start=[Cube[4][0], Cube[4][1], 0], end=[Cube[3][0], Cube[3][1], 0]),
            Lines_front[7].animate.put_start_and_end_on(start=[Cube[3][0], Cube[3][1], 0], end=[Cube[5][0], Cube[5][1], 0]),
            Lines_front[8].animate.put_start_and_end_on(start=[Cube[5][0], Cube[5][1], 0], end=[Cube[1][0], Cube[1][1], 0]),
            Lines_front[9].animate.put_start_and_end_on(start=[Cube[5][0], Cube[5][1], 0], end=[Cube[6][0], Cube[6][1], 0]),
            Lines_front[10].animate.put_start_and_end_on(start=[Cube[6][0], Cube[6][1], 0], end=[Cube[2][0], Cube[2][1], 0]),
            Lines_front[11].animate.put_start_and_end_on(start=[Cube[2][0], Cube[2][1], 0], end=[Cube[1][0], Cube[1][1], 0])
        )

        self.play(Lines_front.animate.move_to([1/4*MUNIT_WIDTH, 0, 0]), Write(Rotation_Tex))
        self.wait(1)
        self.play(Uncreate(Lines_front), Unwrite(Rotation_Tex))

        self.wait(2)

class RotationMatrixExplanation(MovingCameraScene):
    def construct(self):
        vector_size = 3
        graph_x_length = 75
        graph_y_length = 48
        label_font_size = 40
        theta = -40 * DEGREES
        text_nudge = 1/3
        camera_shift = 1/5*MUNIT_WIDTH
        arrange_buff = 0.25
        scaling_factor = 4.1
        new_font_size = label_font_size*scaling_factor

        Graph = Axes(
            x_range=(-1/2*graph_x_length, 1/2*graph_x_length, vector_size),
            y_range=(-1/2*graph_y_length, 1/2*graph_y_length, vector_size),
            x_length=graph_x_length,
            y_length=graph_y_length,
            axis_config={'include_tip': False},
        ).set_color(TEXT_COLOUR)

        i_hat = Vector([vector_size, 0], color=LINE_COLOUR_3D)
        j_hat = Vector([0, vector_size], color=LINE_COLOUR_3D)
        vector_group = VGroup(i_hat, j_hat)

        
        # Work with x:
        i_hat_label = Tex(r"$\boldsymbol{\hat{\imath}}$",
                          font_size=label_font_size,
                          color=TEXT_COLOUR).next_to(i_hat, 1/2*DOWN)
        i_hat_label_copy = i_hat_label.copy()
        x_line = Line(start=[-1, 0, 0], end=[1, 0, 0])
        skewed_x_line = Line(start=[-np.cos(theta), -np.sin(theta), 0], end=[np.cos(theta), np.sin(theta), 0])
        x_angle = Angle(x_line, skewed_x_line, quadrant=(1, 1), color=ANGLE_COLOUR, other_angle=True)

        line_triangle_x = Line(start=[vector_size*np.cos(theta), vector_size*np.sin(theta), 0],
                               end=[vector_size*np.cos(theta), 0, 0],
                               color=LINE_COLOUR_3D,
                               stroke_width=i_hat.stroke_width)
        line_triangle_x_copy = line_triangle_x.copy()

        right_angle_x = RightAngle(line_triangle_x, x_line, quadrant=(-1, -1), color=ANGLE_COLOUR, length = 0.3)

        theta_label_x = Tex(r"$\boldsymbol{\theta}$",
                            font_size=label_font_size,
                            color=ANGLE_COLOUR
                            ).next_to(x_angle, RIGHT).shift([0, -0.07, 0])
        one_label_x = Tex(r"$1$",
                          font_size=label_font_size,
                          color=ANGLE_COLOUR
                          ).move_to([1/2*vector_size*np.cos(theta) + text_nudge*LEFT[0],
                                     1/2*vector_size*np.sin(theta) + text_nudge*DOWN[1], 0])
        

        opposite_x = Tex(r"$\sin{\theta}$",font_size=label_font_size,color=ANGLE_COLOUR)
        opposite_x.move_to([line_triangle_x.get_x() + 1/2*get_len(opposite_x) + 1/2*text_nudge,
                            line_triangle_x.get_y(), 0])
        opposite_x_copy = opposite_x.copy()

        adjacent_x = Tex(r"$\cos{\theta}$", font_size=label_font_size, color=ANGLE_COLOUR)
        adjacent_x.move_to([1/2*vector_size*np.cos(theta), 1/2*get_height(adjacent_x) + 1/2*text_nudge, 0])
        adjacent_x_copy = adjacent_x.copy()

        x_new_vector = Tex(r"$\begin{pmatrix} \cos{\theta}\\ \sin{\theta} \end{pmatrix}$",
                        font_size=label_font_size,
                        color=ANGLE_COLOUR
                        )
        x_new_vector.move_to([vector_size*np.cos(theta) + 1/2*get_len(x_new_vector),
                              vector_size*np.sin(theta) - 1/2*get_height(x_new_vector), 0])
        
        i_hat_identity = VGroup(Tex(r"$ \begin{pmatrix}1\\0\end{pmatrix}$",
                                    font_size=label_font_size,
                                    color=ANGLE_COLOUR),
                                Tex(r"$\rightarrow$",
                                    font_size=label_font_size,
                                    color=ANGLE_COLOUR),
                                Tex(r"$\begin{pmatrix}\cos{\theta}\\ \sin{\theta} \end{pmatrix}$",
                                    font_size=label_font_size,
                                    color=ANGLE_COLOUR)
                        ).arrange(RIGHT)
        i_hat_identity.move_to([-1/2*MUNIT_WIDTH + 1/2*get_len(i_hat_identity) + text_nudge,
                                1/2*MUNIT_HEIGHT - 1/2*get_height(i_hat_identity) - text_nudge, 0])

        
        
        # Work with y:
        j_hat_label = Tex(r"$\boldsymbol{\hat{\jmath}}$",
                          font_size=label_font_size,
                          color=TEXT_COLOUR).next_to(j_hat, 1/2*LEFT)
        j_hat_label_copy = j_hat_label.copy()
        skewed_y_line = Line(start=[np.sin(theta), -np.cos(theta), 0], end=[-np.sin(theta), np.cos(theta), 0])
        y_angle = VGroup(Angle(x_line, skewed_y_line, quadrant=(1, 1), color=ANGLE_COLOUR, radius=0.5),
                         Angle(x_line, skewed_y_line, quadrant=(1, 1), color=ANGLE_COLOUR, radius=0.6))

        line_triangle_y = Line(start=[-vector_size*np.sin(theta), vector_size*np.cos(theta), 0],
                               end=[-vector_size*np.sin(theta), 0, 0],
                               color=LINE_COLOUR_3D,
                               stroke_width=j_hat.stroke_width)
        
        right_angle_y = RightAngle(line_triangle_y, x_line, quadrant=(-1, -1), color=ANGLE_COLOUR, length = 0.3)

        theta_label_y_90 = Tex(r"$\boldsymbol{90-\theta}$",
                            font_size=label_font_size/1.5,
                            color=ANGLE_COLOUR
                            )
        theta_label_y_90.next_to(y_angle, 1/5*RIGHT).shift([0, 1/2*get_height(theta_label_y_90), 0])
            
        one_label_y = Tex(r"$1$",
                          font_size=label_font_size,
                          color=ANGLE_COLOUR
                          )
        one_label_y_copy = one_label_y.copy()
        
        extended_line_triangle_y = line_triangle_y.copy()
        extended_line_triangle_y.put_start_and_end_on(line_triangle_y.get_start() + [0, 1, 0], line_triangle_y.get_end() - [0, -1, 0])

        extended_j_hat = Line(start=ORIGIN, end=[-3/2*vector_size*np.sin(theta), 3/2*vector_size*np.cos(theta), 0])
        y_angle_opp = Angle(extended_line_triangle_y,
                            extended_j_hat,
                            quadrant=(1, -1),
                            color=ANGLE_COLOUR,
                            other_angle=True,
                            radius=0.5)

        x_label_y = Tex(r"$\boldsymbol{x}$",
                            font_size=label_font_size,
                            color=LINE_COLOUR_2D,
                            ).next_to(y_angle_opp, 1/2*DOWN).shift([-0.07, 0, 0])

        explanation_text_components = MathTex(
            r"x", # 0
            r"90", # 1
            r"(", # 2
            r"90", # 3
            r"-", # 4
            r"\theta", # 5
            r")", # 6
            r"180", # 7
            r"=", # 8
            font_size=label_font_size, color=TEXT_COLOUR
        )

        '''x+90+(90-\theta)=180'''
        explanation_text_1 = VGroup(
            explanation_text_components[0],
            MathTex(r"+", font_size=label_font_size, color=TEXT_COLOUR),
            explanation_text_components[1],
            MathTex(r"+", font_size=label_font_size, color=TEXT_COLOUR),
            explanation_text_components[2],
            explanation_text_components[3],
            explanation_text_components[4],
            explanation_text_components[5],
            explanation_text_components[6],
            explanation_text_components[8],
            explanation_text_components[7],
        ).arrange(RIGHT, aligned_edge=ORIGIN)
        explanation_text_1.move_to([1/4*MUNIT_WIDTH + camera_shift,
                                    1/4*MUNIT_HEIGHT, 0])
        
        '''x=180-90-(90-\theta)'''
        explanation_text_2 = VGroup(
            explanation_text_components[0], #0
            explanation_text_components[8], #1
            explanation_text_components[7], #2
            MathTex(r"-", font_size=label_font_size, color=TEXT_COLOUR), #3
            explanation_text_components[1], #4
            MathTex(r"-", font_size=label_font_size, color=TEXT_COLOUR), #5
            explanation_text_components[2], #6
            explanation_text_components[3], #7
            explanation_text_components[4], #8
            explanation_text_components[5], #9
            explanation_text_components[6], #10        
        )

        '''x=180-90-90+\theta'''
        explanation_text_3 = VGroup(
            explanation_text_components[0], #0
            explanation_text_components[8], #1
            explanation_text_components[7], #2
            explanation_text_2[3], #3
            explanation_text_components[1], #4
            explanation_text_2[5], #5
            explanation_text_components[3], #6
            MathTex(r"+", font_size=label_font_size, color=TEXT_COLOUR), #7
            explanation_text_components[5] #8
        )
        '''x=\theta'''
        explanation_text_4 = VGroup(
            explanation_text_components[0], #0
            explanation_text_components[8], #1
            explanation_text_components[5] #2
        )

        theta_label_y = Tex(r"$\boldsymbol{\theta}$",
                            font_size=label_font_size,
                            color=ANGLE_COLOUR,
                            ).move_to(x_label_y)
        
        adjacent_y = Tex(r"$\cos{\theta}$",font_size=label_font_size,color=ANGLE_COLOUR)
        adjacent_y.move_to([line_triangle_y.get_x() + 1/2*get_len(adjacent_y) + 1/2*text_nudge,
                            line_triangle_y.get_y(), 0])
        adjacent_y_copy = adjacent_y.copy()

        opposite_y = VGroup(Tex(r"$-$", font_size=label_font_size, color=ANGLE_COLOUR),
                            Tex(r"$\sin{\theta}$", font_size=label_font_size, color=ANGLE_COLOUR))
        opposite_y[1].move_to([-1/2*vector_size*np.sin(theta), 1/2*get_height(opposite_y) + 1/2*text_nudge, 0])

        '''\theta=-30 ^\circ\\
            \sin \theta= \\
            \cos \theta= \\
        '''
        explanation_text_5 = VGroup(
            VGroup(
                Tex(r"$\theta=$", font_size=label_font_size, color=TEXT_COLOUR),
                DecimalNumber(number=theta * 180/np.pi, num_decimal_places=0, font_size=label_font_size, color=TEXT_COLOUR),
                Tex(r"$^\circ$", font_size=label_font_size, color=TEXT_COLOUR)
            ).arrange(RIGHT),
            VGroup(
                Tex(r"$\sin \theta = $", font_size=label_font_size, color=TEXT_COLOUR),
                DecimalNumber(number=np.sin(theta), num_decimal_places=2, font_size=label_font_size, color=TEXT_COLOUR),
                Tex(r"$<0$", font_size=label_font_size, color=TEXT_COLOUR)
            ).arrange(RIGHT),
            # VGroup(
            #     Tex(r"$\cos \theta = $", font_size=label_font_size, color=TEXT_COLOUR),
            #     DecimalNumber(number=np.cos(theta), num_decimal_places=2, font_size=label_font_size, color=TEXT_COLOUR)
            # ).arrange(RIGHT)
        ).arrange(DOWN)
        explanation_text_5[0][2].shift([-1/2*arrange_buff, 1/2*get_height(explanation_text_5[0][1]), 0])

        explanation_text_5.move_to([1/2*MUNIT_WIDTH-1/2*get_len(explanation_text_5) - text_nudge,
                                    line_triangle_y.get_y(), 0])

        brace_y = Brace(
            Line(start=[0, vector_size*np.cos(theta), 0], end=[-vector_size*np.sin(theta), vector_size*np.cos(theta), 0]),
            direction=[0, 1, 0],
            sharpness=1,
            buff=0,
            color=LINE_COLOUR_2D
            )
        brace_label = Tex(r"$x>0$", font_size=label_font_size, color=LINE_COLOUR_2D)
        brace_label.move_to(brace_y.get_tip()).shift([0, 1/2*get_height(brace_label) + 1/2*text_nudge, 0])
        y_new_vector = Tex(r"$\begin{pmatrix} -\sin{\theta}\\ \cos{\theta} \end{pmatrix}$",
                        font_size=label_font_size,
                        color=ANGLE_COLOUR
                        )
        y_new_vector.move_to([-vector_size*np.sin(theta) + 1/2*get_len(y_new_vector),
                              vector_size*np.cos(theta) + 1/2*get_height(y_new_vector), 0])
        
        j_hat_identity = VGroup(Tex(r"$ \begin{pmatrix}0\\1\end{pmatrix}$",
                                    font_size=label_font_size,
                                    color=ANGLE_COLOUR),
                                Tex(r"$\rightarrow$",
                                    font_size=label_font_size,
                                    color=ANGLE_COLOUR),
                                Tex(r"$\begin{pmatrix}-\sin{\theta}\\ \cos{\theta} \end{pmatrix}$",
                                    font_size=label_font_size,
                                    color=ANGLE_COLOUR)
                        ).arrange(RIGHT)


        # Explanation of the matrix:
        
        identities = VGroup(i_hat_identity, j_hat_identity)
        
        vector_a = Vector(direction=[2*vector_size, 3*vector_size, 0],
                          color=LINE_COLOUR_2D,
                          max_tip_length_to_length_ratio=0.1,
                          max_stroke_width_to_length_ratio=20)
        
        a_label = Tex(r"$\begin{pmatrix} a \\ b \end{pmatrix}$", font_size=new_font_size, color=TEXT_COLOUR)
        a_label.move_to([2*vector_a.get_x()+1/2*get_len(a_label)-text_nudge,
                         2*vector_a.get_y()+1/2*get_height(a_label)+text_nudge, 0])
        
        rotated_a = vector_a.copy()
        rotated_a_label = Tex(r"$\begin{pmatrix} ? \\ ? \end{pmatrix}$", font_size=new_font_size, color=TEXT_COLOUR)
        transformed_a_label = MathTex(r"\begin{pmatrix} a' \\ b' \end{pmatrix}", font_size=new_font_size, color=TEXT_COLOUR)
        rotated_a_label.move_to([a_label.get_x()*np.cos(theta) - a_label.get_y()*np.sin(theta),
                                 a_label.get_x()*np.sin(theta) + a_label.get_y()*np.cos(theta), 0])
        
        line_a = Line(start=[-vector_a.get_x(), -vector_a.get_y(), 0], end=vector_a)
        skewed_line_a = Line(start=[-1*(vector_a.get_x()*np.cos(theta) - vector_a.get_y()*np.sin(theta)),
                                    -1*(vector_a.get_x()*np.sin(theta) + vector_a.get_y()*np.cos(theta)), 0],
                            end=[vector_a.get_x()*np.cos(theta) - vector_a.get_y()*np.sin(theta),
                                 vector_a.get_x()*np.sin(theta) + vector_a.get_y()*np.cos(theta), 0])
        angle_a = Angle(line_a, skewed_line_a,
                        color=ANGLE_COLOUR,
                        quadrant=(1, 1),
                        radius=0.3*scaling_factor,
                        other_angle=True,
                        stroke_width=4*scaling_factor)
        angle_a_label = Tex(r"$\boldsymbol{\theta}$", font_size=scaling_factor*label_font_size, color=ANGLE_COLOUR)
        angle_a_label.move_to([angle_a.get_x() + 1/2*get_len(angle_a_label) + text_nudge,
                               angle_a.get_y() + 1/2*get_height(angle_a_label) + 1/2*text_nudge, 0])
        '''
        \begin{pmatrix}a\\b\end{pmatrix}=a \times \hat{\imath} \,+ \,b \times \hat{\jmath}\\

        \begin{pmatrix}a\\b\end{pmatrix}=a \times \begin{pmatrix}1\\0\end{pmatrix} \,+\, b \times \begin{pmatrix}0\\1\end{pmatrix}\\

        \begin{pmatrix}a'\\b' \end{pmatrix}= a\begin{pmatrix}\cos{\theta}\\\sin{\theta}\end{pmatrix} + b \begin{pmatrix}-\sin{\theta}\\\cos{\theta}\end{pmatrix}\\

        \begin{pmatrix}a'\\b' \end{pmatrix} =\begin{pmatrix}a \times \cos{\theta}\\ a \times \sin{\theta}\end{pmatrix}+\begin{pmatrix}b \times (-\sin{\theta}) \\ b \times \cos{\theta}\end{pmatrix}\\

        \begin{pmatrix}a'\\b' \end{pmatrix}=\begin{pmatrix}a \times \cos{\theta} - b \times \sin{\theta}\\a \times \sin{\theta} + b \times \cos{\theta}\end{pmatrix}\\

        \begin{pmatrix}a'\\b' \end{pmatrix} =\begin{pmatrix}\cos{\theta} & -\sin{\theta}\\\sin{\theta} & \cos{\theta}\end{pmatrix} \begin{pmatrix}a\\b \end{pmatrix}
        '''

        # \begin{pmatrix}a\\b\end{pmatrix}=a \times \hat{\imath} \,+ \,b \times \hat{\jmath}\\
        ab_definition_first = VGroup(
            VGroup(
                MathTex(r"(", font_size=2.5*new_font_size, color=TEXT_COLOUR),
                VGroup(
                    MathTex(r"a", font_size=new_font_size, color=TEXT_COLOUR),
                    MathTex(r"b", font_size=new_font_size, color=TEXT_COLOUR),
                ).arrange(DOWN, aligned_edge=LEFT, buff=new_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT),
                MathTex(r")", font_size=2.5*new_font_size, color=TEXT_COLOUR),
            ),

            MathTex(r"=", font_size=new_font_size, color=TEXT_COLOUR),
        
            VGroup(
                MathTex(r"a", font_size=new_font_size, color=TEXT_COLOUR),
                MathTex(r"\times", font_size=new_font_size, color=TEXT_COLOUR),
                MathTex(r"\hat{\imath}", font_size=new_font_size, color=TEXT_COLOUR),
                MathTex(r"+", font_size=new_font_size, color=TEXT_COLOUR),
                MathTex(r"b", font_size=new_font_size, color=TEXT_COLOUR),
                MathTex(r"\times", font_size=new_font_size, color=TEXT_COLOUR),
                MathTex(r"\hat{\jmath}", font_size=new_font_size, color=TEXT_COLOUR),
            ).arrange(RIGHT, aligned_edge=DOWN, buff=1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH)
        )
        ab_definition_first[2][6].shift([0, -1/4*get_height(ab_definition_first[2][6]), 0])
        ab_definition_first[0][0].shift([-1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH - text_nudge, 0, 0])
        ab_definition_first[0][2].shift([1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH + text_nudge, 0, 0])
        ab_definition_first.arrange(RIGHT, aligned_edge=ORIGIN, buff=1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH)
        ab_definition_first.move_to([MUNIT_WIDTH*scaling_factor*(1/4+1/6), 1/4*MUNIT_HEIGHT*scaling_factor, 0])
        
        # \begin{pmatrix}a\\b\end{pmatrix}=a \times \begin{pmatrix}1\\0\end{pmatrix} \,+\, b \times \begin{pmatrix}0\\1\end{pmatrix}\\
        ab_definition_second = VGroup(
            ab_definition_first[0],
            ab_definition_first[1],
            ab_definition_first[2][0],
            ab_definition_first[2][1],
            MathTex(r"\begin{pmatrix}1\\0\end{pmatrix}", font_size=new_font_size, color=TEXT_COLOUR).move_to(ab_definition_first[2][2]),
            ab_definition_first[2][3],
            ab_definition_first[2][4],
            ab_definition_first[2][5],
            MathTex(r"\begin{pmatrix}0\\1\end{pmatrix}", font_size=new_font_size, color=TEXT_COLOUR).move_to(ab_definition_first[2][6]),
        )

        #\begin{pmatrix}a'\\b' \end{pmatrix}= a\begin{pmatrix}\cos{\theta}\\\sin{\theta}\end{pmatrix} + b \begin{pmatrix}-\sin{\theta}\\\cos{\theta}\end{pmatrix}\\
        ab_definition_third = VGroup(
            VGroup(
                ab_definition_second[0][0],
                VGroup(
                    MathTex(r"a'", font_size=new_font_size, color=TEXT_COLOUR),
                    MathTex(r"b'", font_size=new_font_size, color=TEXT_COLOUR),
                ).arrange(DOWN, aligned_edge=LEFT, buff=new_font_size),
                ab_definition_second[0][2],
            ),
            ab_definition_second[1],
            ab_definition_second[2],
            ab_definition_second[3],
            VGroup(
                MathTex(r"(", font_size=2.5*new_font_size, color=TEXT_COLOUR),
                VGroup(
                    MathTex(r"\cos{\theta}", font_size=new_font_size, color=TEXT_COLOUR),
                    MathTex(r"\sin{\theta}", font_size=new_font_size, color=TEXT_COLOUR),
                ).arrange(DOWN, aligned_edge=ORIGIN, buff=new_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT),
                MathTex(r")", font_size=2.5*new_font_size, color=TEXT_COLOUR),
            ),
            ab_definition_second[5],
            ab_definition_second[6],
            ab_definition_second[7],
            VGroup(
                MathTex(r"(", font_size=2.5*new_font_size, color=TEXT_COLOUR),
                VGroup(
                    VGroup(
                        MathTex(r"-", font_size=new_font_size, color=TEXT_COLOUR),
                        MathTex(r"\sin{\theta}", font_size=new_font_size, color=TEXT_COLOUR)
                    ).arrange(RIGHT, aligned_edge=ORIGIN, buff=1/4*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH),
                    MathTex(r"\cos{\theta}", font_size=new_font_size, color=TEXT_COLOUR),
                ).arrange(DOWN, aligned_edge=ORIGIN, buff=new_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT),
                MathTex(r")", font_size=2.5*new_font_size, color=TEXT_COLOUR),
            ),
        )
        ab_definition_third[4][0].shift([-1/2*get_len(ab_definition_third[4]) - text_nudge, 0, 0])
        ab_definition_third[4][2].shift([1/2*get_len(ab_definition_third[4]) + text_nudge, 0, 0])
        ab_definition_third[8][0].shift([-1/2*get_len(ab_definition_third[8]) - text_nudge, 0, 0])
        ab_definition_third[8][2].shift([1/2*get_len(ab_definition_third[8]) + text_nudge, 0, 0])
        ab_definition_third[8][1][0].shift([0, -1/4*get_height(ab_definition_third[8][1][1]), 0])

        #\begin{pmatrix}a'\\b' \end{pmatrix} =\begin{pmatrix}a \times \cos{\theta}\\ a \times \sin{\theta}\end{pmatrix}+\begin{pmatrix}b \times (-\sin{\theta}) \\ b \times \cos{\theta}\end{pmatrix}\\
        a_times = VGroup(
            ab_definition_third[2],
            ab_definition_third[3]
        )
        a_times_copy = VGroup(
            ab_definition_third[2].copy(),
            ab_definition_third[3].copy()
        )

        b_times = VGroup(
            ab_definition_third[6],
            ab_definition_third[7]
        )
        b_times_copy = VGroup(
            ab_definition_third[6].copy(),
            ab_definition_third[7].copy()
        )
        brackets_sin = VGroup(
            MathTex(r"(", font_size=new_font_size, color=TEXT_COLOUR),
            MathTex(r")", font_size=new_font_size, color=TEXT_COLOUR)
        )

        #\begin{pmatrix}a'\\b' \end{pmatrix}=\begin{pmatrix}a \times \cos{\theta} - b \times \sin{\theta}\\a \times \sin{\theta} + b \times \cos{\theta}\end{pmatrix}\\
        plus_sign = ab_definition_third[5].copy()
        
        ab_definition_fourth_top = VGroup(
            ab_definition_third[8][1][0],
            b_times
        )
        
        ab_definition_fourth_bottom = VGroup(
            ab_definition_third[8][1][1],
            b_times_copy
        )

        ab_definition_fourth = VGroup(
            ab_definition_third[0],
            ab_definition_third[1],
            ab_definition_third[4][0],
            ab_definition_third[4][1],
            a_times,
            a_times_copy,
            plus_sign,
            ab_definition_fourth_top,
            ab_definition_fourth_bottom,
            ab_definition_third[8][2]
        )

        # Finishing touch for the explanation: showing that the matrix is the result of multiplication:
        expalation_arrow_length = 2
        explanation_arrow = Arrow(color=TEXT_COLOUR)

        matrix_multiplication = VGroup(
            VGroup(
                MathTex(r"(", font_size=3*new_font_size, color=TEXT_COLOUR),
                VGroup(
                    MathTex(r"a", font_size=new_font_size, color=TEXT_COLOUR),
                    MathTex(r"b", font_size=new_font_size, color=TEXT_COLOUR),
                ).arrange(DOWN, aligned_edge=ORIGIN, buff=new_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT),
                MathTex(r")", font_size=3*new_font_size, color=TEXT_COLOUR)
            ),
            VGroup(
                MathTex(r"(", font_size=3*new_font_size, color=TEXT_COLOUR),
                VGroup(
                    VGroup(
                        MathTex(r"\cos{\theta},", font_size=new_font_size, color=TEXT_COLOUR),
                        MathTex(r"\sin{\theta},", font_size=new_font_size, color=TEXT_COLOUR),
                    ).arrange(DOWN, aligned_edge=ORIGIN, buff=new_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT),
                    VGroup(
                        MathTex(r"-sin{\theta}", font_size=new_font_size, color=TEXT_COLOUR),
                        MathTex(r"cos{\theta}", font_size=new_font_size, color=TEXT_COLOUR)
                    ).arrange(DOWN, aligned_edge=ORIGIN, buff=new_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT),
                ).arrange(RIGHT, aligned_edge=ORIGIN, buff=new_font_size/SCREEN_WIDTH*MUNIT_WIDTH),
                MathTex(r")", font_size=3*new_font_size, color=TEXT_COLOUR)
            ).arrange(RIGHT, aligned_edge=ORIGIN, buff=1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH)
        )
        matrix_multiplication_squares = VGroup(
            Rectangle(color=LINE_COLOUR_2D),
            Rectangle(color=LINE_COLOUR_2D)
        )

        ### ANIMATIONS ###
        # Initiation and rotation:
        self.play(Create(Graph))
        self.play(Create(i_hat), Create(j_hat), Write(i_hat_label), Write(j_hat_label))
        self.play(Rotate(vector_group, angle=theta, about_point=ORIGIN),
                  i_hat_label.animate.move_to([1/2*vector_size*np.cos(theta) + text_nudge*LEFT[0], 1/2*vector_size*np.sin(theta) + text_nudge*DOWN[1], 0]),
                  j_hat_label.animate.move_to([-1/2*vector_size*np.sin(theta) + text_nudge*LEFT[0], 1/2*vector_size*np.cos(theta) + text_nudge*UP[1], 0]),
                  )
        self.wait(2)
        # Working with x:
        self.play(
                  Create(x_angle),
                  Write(theta_label_x),
                  Create(line_triangle_x),
                  Create(right_angle_x),
                  Transform(i_hat_label, one_label_x)
        )
        self.wait(1)
        self.play(
            Write(adjacent_x),
            Write(opposite_x)
        )
        self.wait(1)
        self.add(opposite_x_copy, adjacent_x_copy)
        self.play(
            adjacent_x.animate.move_to([x_new_vector.get_x(),
                                        x_new_vector.get_y() + 1/2*get_height(x_new_vector) - 1/2*get_height(adjacent_x) - 0.04, 0]),
            opposite_x.animate.move_to([x_new_vector.get_x(),
                                        x_new_vector.get_y() - 1/2*get_height(x_new_vector) + get_height(opposite_x), 0]),
        )
        self.play(
            Write(x_new_vector),
            FadeOut(adjacent_x),
            FadeOut(opposite_x),
            run_time=1
        )
        self.wait(1)
        i_hat_label_copy.move_to(i_hat_label)
        self.play(
            x_new_vector.animate.move_to(i_hat_identity[2]),
            Write(i_hat_identity[0]),
            Write(i_hat_identity[1]),
            Unwrite(adjacent_x_copy),
            Unwrite(opposite_x_copy),
            Transform(i_hat_label, i_hat_label_copy, replace_mobject_with_target_in_scene=True),
            Uncreate(line_triangle_x),
            Uncreate(right_angle_x)
        )
        self.add(i_hat_identity[2])
        self.remove(x_new_vector)
        self.wait(1)


        # Working with y:
        right_angle_ij = RightAngle(i_hat, j_hat, quadrant=(1, 1), color=LINE_COLOUR_2D, length=0.5)
        one_label_y.move_to(j_hat_label)
        self.play(
            Create(line_triangle_y),
            Create(right_angle_y),
        )
        self.wait(1)
        self.play(
            Create(right_angle_ij)
        )
        self.wait(1)
        self.play(
            Uncreate(right_angle_ij)
        )
        self.wait(1)
        self.play(
            Create(y_angle),
            Write(theta_label_y_90),
            Transform(j_hat_label, one_label_y),
            run_time=0.7
        )
        self.wait(1)
        self.play(
            Create(y_angle_opp),
            Write(x_label_y),
            self.camera.frame.animate.shift([camera_shift, 0, 0]),
            i_hat_identity.animate.shift([camera_shift, 0, 0])
        )
        self.wait(1)        
        self.play(FadeIn(explanation_text_1))
        self.wait(1)
        explanation_text_2[3].move_to(explanation_text_1[1])
        explanation_text_2[5].move_to(explanation_text_1[3])
        self.play(
            Unwrite(explanation_text_1[1]),
            Unwrite(explanation_text_1[3]),
            explanation_text_2.animate.arrange(RIGHT,
                                               buff=arrange_buff,
                                               aligned_edge=ORIGIN
                                               ).move_to([1/4*MUNIT_WIDTH + camera_shift, 1/4*MUNIT_HEIGHT, 0])
        )
        self.wait(1)
        self.remove(explanation_text_1[1])
        explanation_text_3[7].move_to(explanation_text_2[8])
        self.play(
            Unwrite(explanation_text_2[6]),
            Unwrite(explanation_text_2[10]),
            Transform(explanation_text_2[8], explanation_text_3[7]),
        )
        self.play(
            explanation_text_3.animate.arrange(RIGHT,
                                               buff=arrange_buff,
                                               aligned_edge=ORIGIN
                                               ).move_to([1/4*MUNIT_WIDTH + camera_shift, 1/4*MUNIT_HEIGHT, 0])
        )
        self.wait(1)
        self.play(
            Unwrite(explanation_text_3[2]),
            Unwrite(explanation_text_3[3]),
            Unwrite(explanation_text_3[4]),
            Unwrite(explanation_text_3[5]),
            Unwrite(explanation_text_3[6]),
            Unwrite(explanation_text_3[7]),
            Unwrite(explanation_text_2[8]),
            explanation_text_4.animate.arrange(RIGHT,
                                               buff=arrange_buff,
                                               aligned_edge=ORIGIN
                                               ).move_to([1/4*MUNIT_WIDTH + camera_shift, 1/4*MUNIT_HEIGHT, 0])
        )
        self.wait(1)
        self.play(
            Transform(x_label_y, theta_label_y)
        )
        self.wait(1)
        self.play(
            Unwrite(explanation_text_4),
            self.camera.frame.animate.shift([-camera_shift, 0, 0]),
            i_hat_identity.animate.shift([-camera_shift, 0, 0]),
            Unwrite(theta_label_y_90),
            Uncreate(y_angle)
        )
        self.wait(1)
        self.play(
            Write(adjacent_y),
            Write(opposite_y[1]),
        )
        self.wait(1)
        opposite_x.move_to([line_triangle_x_copy.get_x() + 1/2*get_len(opposite_x) + 1/2*text_nudge,
                            line_triangle_x_copy.get_y(), 0])
        self.play(
            Write(explanation_text_5),
        )
        self.wait(1)
        self.play(
            Write(brace_y),
            Write(brace_label)
        )
        self.wait(1)
        opposite_y[0].move_to([opposite_y[1].get_x()-1/2*get_len(opposite_y[1])-1/2*text_nudge,
                               1/2*text_nudge+1/4*get_height(opposite_y[1]), 0])
        self.play(
            Write(opposite_y[0]),
            opposite_y.animate.move_to(opposite_y[1])
        )
        self.wait(1)
        self.play(
            Unwrite(brace_y),
            Unwrite(brace_label),
            Unwrite(explanation_text_5)
        )
        self.wait(1)
        self.add(adjacent_y_copy)
        opposite_y_copy = opposite_y.copy()
        self.add(opposite_y_copy)
        self.play(
            adjacent_y.animate.move_to([y_new_vector.get_x(),
                                        y_new_vector.get_y() - 1/2*get_height(y_new_vector) + 1/2*get_height(adjacent_y) - 0.015, 0]),
            opposite_y.animate.move_to([y_new_vector.get_x(),
                                        y_new_vector.get_y() + 1/2*get_height(y_new_vector) - 1/2*get_height(opposite_y) + 0.026, 0]),
        )
        self.play(
            Write(y_new_vector),
            FadeOut(adjacent_y),
            FadeOut(opposite_y)
        )
        self.wait(1)
        j_hat_identity.next_to(i_hat_identity, DOWN)
        j_hat_label_copy.move_to(j_hat_label)
        self.play(
            y_new_vector.animate.move_to(j_hat_identity[2]),
            Write(j_hat_identity[0]),
            Write(j_hat_identity[1]),
            Unwrite(adjacent_y_copy),
            Unwrite(opposite_y_copy),
            Transform(j_hat_label, j_hat_label_copy, replace_mobject_with_target_in_scene=True),
            Uncreate(line_triangle_y),
            Uncreate(right_angle_y),
            Unwrite(theta_label_y),
            Uncreate(y_angle_opp),
            Unwrite(x_label_y)
        )

        # Explanation of the matrix:
        self.wait(1)
        self.remove(y_new_vector)
        self.play(
            Unwrite(theta_label_x),
            Unwrite(i_hat_label),
            Unwrite(j_hat_label),
            # Uncreate(i_hat),
            # Uncreate(j_hat),
            Rotate(i_hat, angle=-theta, about_point=ORIGIN),
            Rotate(j_hat, angle=-theta, about_point=ORIGIN),
            Uncreate(x_angle),
            Unwrite(i_hat_label_copy),
            Unwrite(j_hat_label_copy),
            self.camera.frame.animate.scale(scaling_factor),
            identities.animate.scale(scaling_factor).shift([-1/2*(scaling_factor*MUNIT_WIDTH-MUNIT_WIDTH)+1/2*get_len(identities)*scaling_factor,
                                                            1/2*(scaling_factor*MUNIT_HEIGHT-MUNIT_HEIGHT)-1/2*get_height(identities)*scaling_factor, 0])
        )
        self.wait(1)
        self.play(
            Create(vector_a),
            Write(a_label)
        )
        self.wait(1)
        self.add(rotated_a)
        self.play(
            Rotate(rotated_a, angle=theta, about_point=ORIGIN),
            Write(rotated_a_label),
            Create(angle_a),
            Write(angle_a_label)
        )
        self.wait(1)
        self.play(
            self.camera.frame.animate.shift([1/6*scaling_factor*MUNIT_WIDTH, 0, 0]),
            identities.animate.shift([1/6*scaling_factor*MUNIT_WIDTH, 0, 0])
        )

        self.wait(1)
        self.play(Write(ab_definition_first))
        self.wait(1)
        self.play(
            Transform(ab_definition_first[2][2], ab_definition_second[4]),
            Transform(ab_definition_first[2][6], ab_definition_second[8]),
        )
        self.remove(ab_definition_first[2][2])
        self.remove(ab_definition_first[2][6])
        self.play(
            ab_definition_second.animate.arrange(RIGHT, aligned_edge=ORIGIN, buff=1/2*label_font_size/SCREEN_WIDTH*scaling_factor*MUNIT_WIDTH).move_to(ab_definition_first)
        )
        self.wait(1)
        ab_definition_third[0][1][0].move_to(ab_definition_second[0][1][0])
        ab_definition_third[0][1][1].move_to(ab_definition_second[0][1][1])
        ab_definition_third[4].move_to(ab_definition_second[4])
        ab_definition_third[8].move_to(ab_definition_second[8])
        transformed_a_label.move_to(rotated_a_label)
        self.play(
            Transform(ab_definition_second[0][1][0], ab_definition_third[0][1][0]),
            Transform(ab_definition_second[0][1][1], ab_definition_third[0][1][1]),
            Transform(rotated_a_label, transformed_a_label)
        )
        self.wait(1)
        self.play(
            Transform(ab_definition_second[4], ab_definition_third[4]),
            Transform(ab_definition_second[8], ab_definition_third[8]),
        )
        self.remove(ab_definition_second[0][1][0])
        self.remove(ab_definition_second[0][1][1])
        self.remove(ab_definition_second[4])
        self.remove(ab_definition_second[8])
        self.play(
            ab_definition_third.animate.arrange(RIGHT, aligned_edge=ORIGIN, buff=1/2*label_font_size/SCREEN_WIDTH*scaling_factor*MUNIT_WIDTH).move_to(ab_definition_second)
        )
        self.wait(1)
        a_times_copy.move_to(a_times)
        b_times_copy.move_to(b_times)
        brackets_sin[0].move_to([ab_definition_third[8][1][0].get_left()]).shift([-1/4*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH, 0, 0])
        brackets_sin[1].move_to(ab_definition_third[8][1][0].get_right()).shift([1/4*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH, 0, 0])
        self.add(a_times_copy)
        self.add(b_times_copy)
        self.play(
            ab_definition_third[4][0].animate.move_to(ab_definition_third[2]),

            a_times.animate.move_to([
                ab_definition_third[4][1][0].get_x()-1/2*get_len(ab_definition_third[4][1][0])-1/2*get_len(a_times)-1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH,
                ab_definition_third[4][1][0].get_y()-1/2*get_height(ab_definition_third[4][1][0])+1/2*get_height(a_times), 0
                # ab_definition_third[4][1][0].get_y()-1/4*get_height(ab_definition_third[4][1][0]), 0
            ]),

            a_times_copy.animate.move_to([
                ab_definition_third[4][1][1].get_x()-1/2*get_len(ab_definition_third[4][1][1])-1/2*get_len(a_times_copy)-1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH,
                ab_definition_third[4][1][1].get_y()-1/2*get_height(ab_definition_third[4][1][1])+1/2*get_height(a_times_copy), 0
                # ab_definition_third[4][1][1].get_y()-1/4*get_height(ab_definition_third[4][1][1]), 0
            ]),

            ab_definition_third[8][0].animate.move_to(ab_definition_third[6]),
            ab_definition_third[8][2].animate.shift([get_len(brackets_sin[1]), 0, 0]),

            b_times.animate.move_to([
                brackets_sin[0].get_x()-1/2*get_len(brackets_sin[0])-1/2*get_len(b_times)-1/4*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH,
                ab_definition_third[8][1][0].get_y()-1/2*get_height(ab_definition_third[8][1][0])+1/2*get_height(b_times), 0
            ]),

            b_times_copy.animate.move_to([
                ab_definition_third[8][1][1].get_x()-1/2*get_len(ab_definition_third[8][1][1])-1/2*get_len(b_times_copy)-1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH,
                ab_definition_third[8][1][1].get_y()-1/2*get_height(ab_definition_third[8][1][1])+1/2*get_height(b_times_copy), 0
            ]),
            Write(brackets_sin)
        )
        self.wait(1)
        self.play(
            Unwrite(brackets_sin),
            b_times.animate.move_to([
                ab_definition_third[8][1][0][1].get_x()-1/2*get_len(ab_definition_third[8][1][0][1])-1/2*get_len(b_times)-1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH,
                b_times.get_y(), 0
            ]),
            ab_definition_third[8][1][0][0].animate.move_to([
                b_times.get_left()[0] + 1/2*get_len(ab_definition_third[8][1][0][0]),
                b_times.get_left()[1], 0
            ]),
            ab_definition_third[8][2].animate.shift([-get_len(brackets_sin[1]), 0, 0]),
        )
        self.wait(1)
        plus_sign.move_to([
            ab_definition_third[4][1][1].get_right()[0]+1/2*get_len(plus_sign)+1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH,
            ab_definition_third[4][1][1].get_right()[1], 0])
        self.play(
            Unwrite(ab_definition_third[5]),
            Unwrite(ab_definition_third[4][2]),
            Unwrite(ab_definition_third[8][0]),
            Write(plus_sign),
            ab_definition_fourth_top.animate.next_to(ab_definition_third[4][1][0], buff=1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH),
            ab_definition_fourth_bottom.animate.next_to(plus_sign, buff=1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH),
            ab_definition_third[8][2].animate.shift([-get_len(plus_sign)-2*get_len(ab_definition_third[4][2])-1/2*new_font_size/SCREEN_WIDTH*MUNIT_WIDTH, 0, 0])
        )
        # self.wait(1)
        self.play(
            ab_definition_fourth.animate.move_to([
                (1/2+1/6)*MUNIT_WIDTH*scaling_factor-1/2*get_len(ab_definition_fourth)-new_font_size/SCREEN_WIDTH*MUNIT_WIDTH,
                ab_definition_fourth.get_y(), 0
            ])
        )
        self.wait(2)


class Test(Scene):
    def construct(self):
        label_font_size=40
        
        Text = VGroup(
            Tex(r"$($", font_size=3*label_font_size, color=TEXT_COLOUR), #0
            VGroup( #1
                Tex(r"$\cos{\theta}$", font_size=label_font_size, color=TEXT_COLOUR),
                Tex(r"$\sin{\theta}$", font_size=label_font_size, color=TEXT_COLOUR),
            ).arrange(DOWN, aligned_edge=LEFT, buff=label_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT),
            Tex(r"$)$", font_size=3*label_font_size, color=TEXT_COLOUR) #2
        ).arrange(RIGHT, aligned_edge=ORIGIN, buff=0.1)

        TransofrmedText = VGroup(
                VGroup( #0
                    Tex(r"$a \times $", font_size=label_font_size, color=TEXT_COLOUR), #00
                    Text[1][0] #01
                ),
                VGroup(#1
                    Tex(r"$a\times$", font_size=label_font_size, color=TEXT_COLOUR),#10
                    Text[1][1]#11
                )
        )

        self.play(Write(Text))
        self.wait(1)
        TransofrmedText[0][0].next_to(Text[0][0], LEFT)
        TransofrmedText[1][0].next_to(Text[0][0], LEFT)
        self.play(
            Write(TransofrmedText[0][0]),
            Write(TransofrmedText[1][0])
        )
        self.play(
            TransofrmedText[0].animate.arrange(RIGHT, aligned_edge=DOWN, buff=0.1).move_to(Text[1][0]),
            TransofrmedText[1].animate.arrange(RIGHT, aligned_edge=DOWN, buff=0.1).move_to(Text[1][1])
        )

        self.play(
            TransofrmedText.animate.arrange(DOWN, aligned_edge=LEFT, buff=label_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT),
        )
        self.play(
            Text[0].animate.next_to(TransofrmedText, [-label_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT, 0, 0]),
            Text[2].animate.next_to(TransofrmedText, [label_font_size/SCREEN_HEIGHT*MUNIT_HEIGHT, 0, 0])
        )

        self.wait(2)
        eq = MathTex(r"\text{\tiny $x^2 + y^2 = z^2$}")
        self.play(Write(eq))
        self.wait(1)


with tempconfig({"disable_caching": True, "preview": True}):
    scene = NewIntroShapes()
    scene.render()
