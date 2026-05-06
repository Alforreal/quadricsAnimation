from manim import *
import numpy as np


class AxesTemplate(Scene):
    def construct(self):
        # The starting cube:
        Cube = [np.matrix('1; 0; 0'), #0
                np.matrix('0; 1; 0'), #1
                np.matrix('1; 1; 0'), #2
                np.matrix('0; 0; 1'), #3
                np.matrix('1; 0; 1'), #4
                np.matrix('0; 1; 1'), #5
                np.matrix('1; 1; 1'), #6
                np.matrix('0; 0; 0')  #7
                ]

        graph = Axes(
            x_range=[-1,10,1],
            y_range=[-1,10,1],
            x_length=9,
            y_length=6,
            axis_config={"include_tip":False}
        )
        # projection_matrix = np.matrix('1 0 0; 0 1 0; 0 0 0')
        # Cube_projection = []
        # for i in range(5):
        #     Cube_projection.append(projection_matrix * Cube[i])
        # print("Cube_projection: " + str(Cube_projection))
        print("item: " + str(Cube[7][0][0]))
        print("item2: " + str(Cube[7][1][0]))
        # lines = VGroup(
        #     Line(start=[Cube[7][0], Cube[7][1]], end=[Cube[0][0], Cube[0][1]], buff=0),
        #     Line(start=[Cube[7][0], Cube[7][1]], end=[Cube[3][0], Cube[3][1]], buff=0),
        #     Line(start=[Cube[7][0], Cube[7][1]], end=[Cube[1][0], Cube[1][1]], buff=0),
        #     Line(start=[Cube[0][0], Cube[0][1]], end=[Cube[4][0], Cube[4][1]], buff=0),
        #     Line(start=[Cube[0][0], Cube[0][1]], end=[Cube[2][0], Cube[2][1]], buff=0),
        #     Line(start=[Cube[4][0], Cube[4][1]], end=[Cube[6][0], Cube[6][1]], buff=0),
        #     Line(start=[Cube[4][0], Cube[4][1]], end=[Cube[3][0], Cube[3][1]], buff=0),
        #     Line(start=[Cube[3][0], Cube[3][1]], end=[Cube[5][0], Cube[5][1]], buff=0),
        #     Line(start=[Cube[5][0], Cube[5][1]], end=[Cube[1][0], Cube[1][1]], buff=0),
        #     Line(start=[Cube[5][0], Cube[5][1]], end=[Cube[6][0], Cube[6][1]], buff=0),
        #     Line(start=[Cube[6][0], Cube[6][1]], end=[Cube[2][0], Cube[2][1]], buff=0),
        #     Line(start=[Cube[2][0], Cube[2][1]], end=[Cube[1][0], Cube[1][1]], buff=0)
        # )

        labels = graph.get_axis_labels()
        self.add(graph, labels)
        # self.play(Create(lines))
