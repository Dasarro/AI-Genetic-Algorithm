import tkinter as tk
from random import randint, random, randrange, uniform
import time
import pytest
from copy import deepcopy
from statistics import mean, stdev


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y


class Board:
    def __init__(self, width: int, height: int, point_pairs: list):
        self.width = width
        self.height = height
        self.point_pairs = point_pairs

    def __str__(self):
        pairs = ''
        for pair in self.point_pairs:
            pairs += f'[{pair[0]}, {pair[1]}] '
        return f'Width and height of the board: {self.width} X {self.height}\nPoint pairs: {pairs}'


class Segment:
    def __init__(self, start_point: Point, end_point: Point):
        self.start_point = start_point
        self.end_point = end_point

    def __str__(self):
        return f'[{self.start_point}, {self.end_point}]'

    def __eq__(self, other):
        if not isinstance(other, Segment):
            return NotImplemented
        return self.start_point == other.start_point and self.end_point == other.end_point


def pathfinding(start_point: Point, end_point: Point, board: Board,
                direction_probability: float = 0.65, given_segments: list = None, cap: int = 13):
    segments = given_segments if given_segments else []
    segments_count = len(segments)
    total_length = 0
    last_horizontal = None
    for segment in segments:
        if (segment.start_point.x == segment.end_point.x):
            total_length += abs(segment.start_point.y - segment.end_point.y)
            last_horizontal = False
        else:
            total_length += abs(segment.start_point.x - segment.end_point.x)
            last_horizontal = True
    while (segments_count == 0 or segments[segments_count - 1].end_point != end_point):
        current_start = start_point if segments_count == 0 else segments[segments_count - 1].end_point
        axis_choice = random()
        direction_choice = random()
        if (segments_count >= cap):
            if (last_horizontal and current_start.y != end_point.y):
                current_end = Point(current_start.x, end_point.y)
                segment_length = abs(current_start.y - end_point.y)
                last_horizontal = False
            elif (not last_horizontal and current_start.x != end_point.x):
                current_end = Point(end_point.x, current_start.y)
                segment_length = abs(current_start.x - end_point.x)
                last_horizontal = True
            else:
                # current start is actually treated as endpoint of previous segment
                previous_start = segments[segments_count - 1].start_point
                if (last_horizontal):
                    total_length -= abs(previous_start.x - current_start.x)
                    current_start.x = end_point.x
                    total_length += abs(previous_start.x - current_start.x)
                else:
                    total_length -= abs(previous_start.y - current_start.y)
                    current_start.y = end_point.y
                    total_length += abs(previous_start.y - current_start.y)
                return segments, total_length

        elif (segments_count == 0):
            if (direction_choice < direction_probability):
                orientation_x = end_point.x - current_start.x
                orientation_y = end_point.y - current_start.y
                if (orientation_x != 0 and orientation_y != 0):
                    if (axis_choice < 0.5):
                        # X axis
                        if (orientation_x > 0):
                            # Right
                            distance_to_edge = (board.width - 1) - current_start.x
                            segment_length = randrange(1, distance_to_edge + 1)
                            current_end = Point(current_start.x + segment_length, current_start.y)
                        else:
                            # Left
                            distance_to_edge = current_start.x
                            segment_length = randrange(1, distance_to_edge + 1)
                            current_end = Point(current_start.x - segment_length, current_start.y)
                        last_horizontal = True
                    else:
                        # Y axis
                        if (orientation_y > 0):
                            # Down
                            distance_to_edge = (board.height - 1) - current_start.y
                            segment_length = randrange(1, distance_to_edge + 1)
                            current_end = Point(current_start.x, current_start.y + segment_length)
                        else:
                            # Up
                            distance_to_edge = current_start.y
                            segment_length = randrange(1, distance_to_edge + 1)
                            current_end = Point(current_start.x, current_start.y - segment_length)
                        last_horizontal = False
                elif (orientation_x == 0):
                    # Y axis
                    distance_to_end = abs(end_point.y - current_start.y)
                    segment_length = randrange(1, distance_to_end + 1)
                    if (orientation_y > 0):
                        # Down
                        current_end = Point(current_start.x, current_start.y + segment_length)
                    else:
                        # Up
                        current_end = Point(current_start.x, current_start.y - segment_length)
                    last_horizontal = False
                else:
                    # X axis
                    distance_to_end = abs(end_point.x - current_start.x)
                    segment_length = randrange(1, distance_to_end + 1)
                    if (orientation_x > 0):
                        # Right
                        current_end = Point(current_start.x + segment_length, current_start.y)
                    else:
                        # Left
                        current_end = Point(current_start.x - segment_length, current_start.y)
                    last_horizontal = True
            else:
                if ((axis_choice < 0.25 and current_start.x != board.width - 1) or
                        (axis_choice < 0.5 and current_start.x == 0)):
                    # X axis right
                    distance_to_edge = (board.width - 1) - current_start.x
                    segment_length = randrange(1, distance_to_edge + 1)
                    current_end = Point(current_start.x + segment_length, current_start.y)
                    last_horizontal = True
                elif (axis_choice < 0.5 and (current_start.x != 0 or current_start.x == board.width - 1)):
                    # X axis left
                    distance_to_edge = current_start.x
                    segment_length = randrange(1, distance_to_edge + 1)
                    current_end = Point(current_start.x - segment_length, current_start.y)
                    last_horizontal = True
                elif ((axis_choice < 0.75 and current_start.y != board.height - 1) or current_start.y == 0):
                    # Y axis down
                    distance_to_edge = (board.height - 1) - current_start.y
                    segment_length = randrange(1, distance_to_edge + 1)
                    current_end = Point(current_start.x, current_start.y + segment_length)
                    last_horizontal = False
                else:
                    # Y axis up
                    distance_to_edge = current_start.y
                    segment_length = randrange(1, distance_to_edge + 1)
                    current_end = Point(current_start.x, current_start.y - segment_length)
                    last_horizontal = False
        else:
            if (direction_choice < direction_probability):
                orientation_x = end_point.x - current_start.x
                orientation_y = end_point.y - current_start.y
                if (last_horizontal):
                    # Y axis
                    if (orientation_x == 0):
                        distance_to_end = abs(end_point.y - current_start.y)
                        segment_length = randrange(1, distance_to_end + 1)
                        if (orientation_y > 0):
                            # Down
                            current_end = Point(current_start.x, current_start.y + segment_length)
                        else:
                            # Up
                            current_end = Point(current_start.x, current_start.y - segment_length)
                    elif (orientation_y > 0
                            or (orientation_y == 0 and axis_choice < 0.5 and current_start.y != board.height - 1)
                            or current_start.y == 0):
                        # Down
                        distance_to_edge = (board.height - 1) - current_start.y
                        segment_length = randrange(1, distance_to_edge + 1)
                        current_end = Point(current_start.x, current_start.y + segment_length)
                    else:
                        # Up
                        distance_to_edge = current_start.y
                        segment_length = randrange(1, distance_to_edge + 1)
                        current_end = Point(current_start.x, current_start.y - segment_length)
                    last_horizontal = False
                else:
                    # X axis
                    if (orientation_y == 0):
                        distance_to_end = abs(end_point.x - current_start.x)
                        segment_length = randrange(1, distance_to_end + 1)
                        if (orientation_x > 0):
                            # Right
                            current_end = Point(current_start.x + segment_length, current_start.y)
                        else:
                            # Left
                            current_end = Point(current_start.x - segment_length, current_start.y)
                    elif (orientation_x > 0
                            or (orientation_x == 0 and axis_choice < 0.5 and current_start.x != board.width - 1)
                            or current_start.x == 0):
                        # Right
                        distance_to_edge = (board.width - 1) - current_start.x
                        segment_length = randrange(1, distance_to_edge + 1)
                        current_end = Point(current_start.x + segment_length, current_start.y)
                    else:
                        # Left
                        distance_to_edge = current_start.x
                        segment_length = randrange(1, distance_to_edge + 1)
                        current_end = Point(current_start.x - segment_length, current_start.y)
                    last_horizontal = True
            else:
                if (last_horizontal):
                    if ((axis_choice < 0.5 and current_start.y != board.height - 1) or current_start.y == 0):
                        # Y axis down
                        distance_to_edge = (board.height - 1) - current_start.y
                        segment_length = randrange(1, distance_to_edge + 1)
                        current_end = Point(current_start.x, current_start.y + segment_length)
                    else:
                        # Y axis up
                        distance_to_edge = current_start.y
                        segment_length = randrange(1, distance_to_edge + 1)
                        current_end = Point(current_start.x, current_start.y - segment_length)
                    last_horizontal = False
                else:
                    if ((axis_choice < 0.5 and current_start.x != board.width - 1) or current_start.x == 0):
                        # X axis down
                        distance_to_edge = (board.width - 1) - current_start.x
                        segment_length = randrange(1, distance_to_edge + 1)
                        current_end = Point(current_start.x + segment_length, current_start.y)
                    else:
                        # X axis left
                        distance_to_edge = current_start.x
                        segment_length = randrange(1, distance_to_edge + 1)
                        current_end = Point(current_start.x - segment_length, current_start.y)
                    last_horizontal = True
        segments.append(Segment(current_start, current_end))
        segments_count += 1
        total_length += segment_length
    return segments, total_length


class Path:
    def __init__(self, segments: list = None):
        self.segments = segments
        self.length = None if segments is None else self.calculate_length()

    def create_random(self, start_point: Point, end_point: Point, board: Board, direction_probability: float = 0.75):
        segments, total_length = pathfinding(start_point, end_point, board, direction_probability)
        self.segments = segments
        self.length = total_length

    def calculate_length(self):
        total_length = 0
        for segment in self:
            if (segment.start_point.x == segment.end_point.x):
                total_length += abs(segment.start_point.y - segment.end_point.y)
            else:
                total_length += abs(segment.start_point.x - segment.end_point.x)
        return total_length

    def __str__(self):
        segments = ''
        for segment in self.segments:
            segments += str(segment)
        return segments

    def __iter__(self):
        for segment in self.segments:
            yield segment

    def __eq__(self, other):
        if not isinstance(other, Path):
            return NotImplemented
        return self.segments == other.segments and self.length == other.length


class Solution:
    def __init__(self):
        self.paths = []
        self.fitness = 0

    def setPaths(self,
                 paths: list,
                 length_weight: float = 1,
                 segment_weight: float = 20,
                 intersection_weight: float = 1000):
        self.paths = paths
        self.fitness = self.calculate_fitness(length_weight, segment_weight, intersection_weight)

    def random_solve(self,
                     board: Board,
                     length_weight: float = 1,
                     segment_weight: float = 20,
                     intersection_weight: float = 1000):
        paths = []
        for pair in board.point_pairs:
            path = Path()
            path.create_random(pair[0], pair[1], board)
            paths.append(path)
        self.setPaths(paths, length_weight, segment_weight, intersection_weight)

    def __intersect(self, S1: Segment, S2: Segment):
        A, B = S1.start_point, S1.end_point
        C, D = S2.start_point, S2.end_point
        if (A.x == B.x == C.x == D.x):
            min1 = min(A.y, B.y)
            max1 = max(A.y, B.y)

            min2 = min(C.y, D.y)
            max2 = max(C.y, D.y)

            minIntersection = max(min1, min2)
            maxIntersection = min(max1, max2)

            if (minIntersection <= maxIntersection):
                return abs(minIntersection - maxIntersection) + 1
            else:
                return 0
        elif (A.y == B.y == C.y == D.y):
            min1 = min(A.x, B.x)
            max1 = max(A.x, B.x)

            min2 = min(C.x, D.x)
            max2 = max(C.x, D.x)

            minIntersection = max(min1, min2)
            maxIntersection = min(max1, max2)

            if (minIntersection <= maxIntersection):
                return abs(minIntersection - maxIntersection) + 1
            else:
                return 0
        else:
            dx0 = B.x - A.x
            dx1 = D.x - C.x
            dy0 = B.y - A.y
            dy1 = D.y - C.y

            p0 = dy1 * (D.x - A.x) - dx1 * (D.y - A.y)
            p1 = dy1 * (D.x - B.x) - dx1 * (D.y - B.y)
            p2 = dy0 * (B.x - C.x) - dx0 * (B.y - C.y)
            p3 = dy0 * (B.x - D.x) - dx0 * (B.y - D.y)

            return int((p0 * p1 <= 0) & (p2 * p3 <= 0))

    def __calculate_intersections(self):
        intersections = 0
        for i, pathA in enumerate(self.paths):
            for pathB in self.paths[i+1:]:
                for segmentA in pathA:
                    for segmentB in pathB:
                        intersections += self.__intersect(segmentA, segmentB)
        for path in self.paths:
            for j, segmentA in enumerate(path):
                for segmentB in path.segments[j+3:]:
                    intersections += self.__intersect(segmentA, segmentB)
        return intersections

    def __iter__(self):
        for path in self.paths:
            yield path

    def __eq__(self, other):
        if not isinstance(other, Solution):
            return NotImplemented
        return self.paths == other.paths

    def calculate_fitness(self, length_weight: float, segment_weight: float, intersection_weight: float):
        fitness = 0
        for path in self:
            fitness += segment_weight * len(path.segments)
            fitness += length_weight * path.length
        fitness += intersection_weight * self.__calculate_intersections()
        return fitness

    def crossover_with_random_genes(self,
                                    second_parent: 'Solution',
                                    length_weight: float = 1,
                                    segment_weight: float = 20,
                                    intersection_weight: float = 1000):
        if (len(self.paths) != len(second_parent.paths)):
            raise ValueError('Wrong sizes of crossover parents')
        child = Solution()
        new_paths = []
        for i in range(len(self.paths)):
            if (random() < 0.5):
                new_paths.append(deepcopy(self.paths[i]))
            else:
                new_paths.append(deepcopy(second_parent.paths[i]))
        child.setPaths(new_paths, length_weight, segment_weight, intersection_weight)
        return child

    def crossover_with_even_genes_distribution(self,
                                               second_parent: 'Solution',
                                               length_weight: float = 1,
                                               segment_weight: float = 20,
                                               intersection_weight: float = 1000):
        if (len(self.paths) != len(second_parent.paths)):
            raise ValueError('Wrong sizes of crossover parents')
        child = Solution()
        if (random() < 0.5):
            child.setPaths(deepcopy(self.paths[0:len(self.paths)//2]) +
                           deepcopy(second_parent.paths[len(self.paths)//2:]),
                           length_weight, segment_weight, intersection_weight)
        else:
            child.setPaths(deepcopy(second_parent.paths[0:len(self.paths)//2]) +
                           deepcopy(self.paths[len(self.paths)//2:]),
                           length_weight, segment_weight, intersection_weight)
        return child

    def mutate_reroll(self, board: Board, given_path: list = None,
                      length_weight: float = 1, segment_weight: float = 20, intersection_weight: float = 1000):
        path_to_mutate = given_path if given_path else self.paths[randrange(0, len(self.paths))]
        mutation_start = randrange(0, len(path_to_mutate.segments))
        segments_to_replace = path_to_mutate.segments[mutation_start:]
        start_point = segments_to_replace[0].start_point
        end_point = path_to_mutate.segments[len(path_to_mutate.segments) - 1].end_point
        new_segments, new_length = pathfinding(start_point, end_point, board,
                                               given_segments=path_to_mutate.segments[:mutation_start])
        path_to_mutate.segments = new_segments
        path_to_mutate.length = new_length
        self.fitness = self.calculate_fitness(length_weight, segment_weight, intersection_weight)

    def mutate_shift(self, board: Board, only_shift=False, segment_to_shift=None,
                     shift_length=None, shift_direction=None, reroll_prob: float = 0.15,
                     length_weight: float = 1, segment_weight: float = 20, intersection_weight: float = 1000):
        path_to_mutate = self.paths[randrange(0, len(self.paths))]
        reroll = random() < reroll_prob
        if (len(path_to_mutate.segments) >= 3 and (only_shift or not reroll)):
            segment_i = randrange(1, len(path_to_mutate.segments) - 1) if segment_to_shift is None else segment_to_shift
            segment_to_shift = path_to_mutate.segments[segment_i]
            if (segment_to_shift.start_point.x == segment_to_shift.end_point.x):
                left_edge = segment_to_shift.start_point.x
                right_edge = board.width - 1 - segment_to_shift.start_point.x
                if (shift_direction == 0 or ((((random() < 0.5 and left_edge != 0) or right_edge == 0) and shift_direction != 1))):
                    shift = randrange(1, left_edge + 1) if shift_length is None else shift_length
                    segment_to_shift.start_point.x -= shift
                    segment_to_shift.end_point.x -= shift
                else:
                    shift = randrange(1, right_edge + 1) if shift_length is None else shift_length
                    segment_to_shift.start_point.x += shift
                    segment_to_shift.end_point.x += shift
            else:
                upper_edge = segment_to_shift.start_point.y
                lower_edge = board.height - 1 - segment_to_shift.start_point.y
                if (shift_direction == 0 or ((((random() < 0.5 and upper_edge != 0) or lower_edge == 0) and shift_direction != 1))):
                    shift = randrange(1, upper_edge + 1) if shift_length is None else shift_length
                    segment_to_shift.start_point.y -= shift
                    segment_to_shift.end_point.y -= shift
                else:
                    shift = randrange(1, lower_edge + 1) if shift_length is None else shift_length
                    segment_to_shift.start_point.y += shift
                    segment_to_shift.end_point.y += shift
            previous_segment = path_to_mutate.segments[segment_i - 1]
            next_segment = path_to_mutate.segments[segment_i + 1]
            deletions = 0
            if (previous_segment.start_point == previous_segment.end_point):
                if (segment_i - 3 >= 0 and segment_to_shift.end_point == path_to_mutate.segments[segment_i - 3].end_point):
                    path_to_mutate.segments[segment_i + 1].start_point = path_to_mutate.segments[segment_i - 3].start_point
                    del path_to_mutate.segments[segment_i - 3:segment_i + 1]
                    deletions = 4
                elif (segment_i - 2 >= 0 and segment_to_shift.end_point == path_to_mutate.segments[segment_i - 2].start_point):
                    path_to_mutate.segments[segment_i + 1].start_point = path_to_mutate.segments[segment_i - 2].start_point
                    del path_to_mutate.segments[segment_i - 2:segment_i + 1]
                    deletions = 3
                elif (segment_i - 2 >= 0):
                    segment_to_shift.start_point = path_to_mutate.segments[segment_i - 2].start_point
                    del path_to_mutate.segments[segment_i - 2:segment_i]
                    deletions = 2
                else:
                    del path_to_mutate.segments[segment_i - 1]
                    deletions = 1

            if (next_segment.start_point == next_segment.end_point):
                segment_i -= deletions
                if (segment_i + 3 < len(path_to_mutate.segments) and
                        segment_to_shift.start_point == path_to_mutate.segments[segment_i + 3].start_point):
                    path_to_mutate.segments[segment_i - 1].end_point = path_to_mutate.segments[segment_i + 3].end_point
                    del path_to_mutate.segments[segment_i:segment_i + 4]
                elif ((segment_i + 2 < len(path_to_mutate.segments)) and
                        segment_to_shift.start_point == path_to_mutate.segments[segment_i + 2].end_point):
                    path_to_mutate.segments[segment_i - 1].end_point = path_to_mutate.segments[segment_i + 2].end_point
                    del path_to_mutate.segments[segment_i:segment_i + 3]
                elif (segment_i + 2 < len(path_to_mutate.segments)):
                    segment_to_shift.end_point = path_to_mutate.segments[segment_i + 2].end_point
                    del path_to_mutate.segments[segment_i + 1:segment_i + 3]
                else:
                    del path_to_mutate.segments[segment_i + 1]

            path_to_mutate.length = path_to_mutate.calculate_length()
            self.fitness = self.calculate_fitness(length_weight, segment_weight, intersection_weight)

        elif reroll and not only_shift:
            self.mutate_reroll(board, path_to_mutate, length_weight, segment_weight, intersection_weight)


class Population:
    def __init__(self, size: int = 300):
        self.solutions = []
        self.size = size

    def __iter__(self):
        for solution in self.solutions:
            yield solution

    def initialize(self, board: Board):
        for _ in range(self.size):
            solution = Solution()
            solution.random_solve(board)
            self.solutions.append(solution)

    def evaluate(self):
        return sorted(self.solutions, key=lambda x: x.fitness)

    def selection_roulette(self):
        max_fitness = self.evaluate()[len(self.solutions) - 1].fitness
        fitness_sum = sum([max_fitness - solution.fitness for solution in self])
        pick = uniform(0, fitness_sum)
        current = 0
        for solution in self:
            current += max_fitness - solution.fitness
            if (current >= pick):
                return solution

    def selection_tournament(self, tournament_size):
        tournament_members = []
        best_fitness = None
        best_position = -1
        for i in range(tournament_size):
            individual = self.solutions[randrange(0, len(self.solutions))]
            tournament_members.append(individual)
            if (best_fitness is None or individual.fitness < best_fitness):
                best_fitness = individual.fitness
                best_position = i
        result = tournament_members[best_position]
        return result


def random_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return f'#{r:02X}{g:02X}{b:02X}'


def draw(canvas, point_scale, solution, board):
    # colors = [random_color() for pair in board.point_pairs]
    colors = ['#FF0000', '#FF00FF', '#00FF00', '#00FFFF', '#FFFF00',
              '#0000FF', '#FF8800', '#88FF00', '#8800FF', '#0088FF']
    flat_paths = []
    for path in solution:
        flat_path = []
        for segment in path:
            flat_path.extend([segment.start_point.x + 1,
                              segment.start_point.y + 1,
                              segment.end_point.x + 1,
                              segment.end_point.y + 1])
        flat_paths.append(flat_path)

    for x in range(1, board.width + 1):
        for y in range(1, board.height + 1):
            canvas.create_oval(x * point_scale + point_scale // 4,
                               y * point_scale + point_scale // 4,
                               x * point_scale - point_scale // 4,
                               y * point_scale - point_scale // 4,
                               fill='#5D5D5D')

    color_counter = 0
    for point_pair in board.point_pairs:
        for point in point_pair:
            canvas.create_oval((point.x + 1) * point_scale + point_scale // 4,
                               (point.y + 1) * point_scale + point_scale // 4,
                               (point.x + 1) * point_scale - point_scale // 4,
                               (point.y + 1) * point_scale - point_scale // 4,
                               fill=colors[color_counter],
                               outline=colors[color_counter])
        color_counter += 1
    for i, path in enumerate(flat_paths):
        canvas.create_line(*[coord * point_scale for coord in path], fill=colors[i], width=point_scale // 4)


def visualisation(board: Board, path: Path, point_scale: int = 75):
    window = tk.Tk()
    height = (board.height + 1) * point_scale
    width = (board.width + 1) * point_scale
    canvas = tk.Canvas(window, bg='#2D2D2D', height=height, width=width)
    draw(canvas, point_scale, path, board)
    canvas.pack()

    menu_bar = tk.Menu(window)
    menu = tk.Menu(menu_bar, tearoff=0)
    menu.add_command(label='Redraw', command=(lambda: draw(canvas, point_scale, path, board)))
    menu_bar.add_cascade(label='Options', menu=menu)
    window.config(menu=menu_bar)

    window.protocol('WM_DELETE_WINDOW', exit)
    window.mainloop()


def genetic_algorithm(board: Board,
                      crossover_prob: float,
                      mutation_prob: float,
                      population_size: int,
                      selection_tournament: bool,
                      reroll_prob: float,
                      iteration_count: int,
                      fitness_length_weight: float,
                      fitness_segment_weight: float,
                      fitness_intersection_weight: float,
                      tournament_size: int = 0):
    population = Population(population_size)
    population.initialize(board)
    best_solution = population.evaluate()[0]
    start = time.time()
    i = 0
    j = 0
    try:
        # while (time.time() - start < 25):
        while (i < iteration_count):
            i += 1
            new_generation = []
            while (len(new_generation) < population_size):
                if (tournament_size > 0 and selection_tournament is True):
                    S1 = population.selection_tournament(tournament_size)
                else:
                    S1 = population.selection_roulette()
                if (random() < crossover_prob):
                    if (tournament_size > 0 and selection_tournament is True):
                        S2 = population.selection_tournament(tournament_size)
                    else:
                        S2 = population.selection_roulette()
                    offspring = S1.crossover_with_random_genes(S2, fitness_length_weight,
                                                               fitness_segment_weight,
                                                               fitness_intersection_weight)
                else:
                    offspring = deepcopy(S1)
                if (random() < mutation_prob):
                    offspring.mutate_shift(board, reroll_prob=reroll_prob,
                                           length_weight=fitness_length_weight,
                                           segment_weight=fitness_segment_weight,
                                           intersection_weight=fitness_intersection_weight)
                new_generation.append(offspring)
                if (offspring.fitness < best_solution.fitness):
                    best_solution = offspring
                    print('New best:', offspring.fitness, 'Number of generations: ', i)

            population.solutions = new_generation
            if ((time.time() - start) // 5 > j):
                print(f'{int(time.time() - start)}s')
                j += 1
    except KeyboardInterrupt:
        print('Program execution interrupted')
    print('---------------- Genetic algorithm finished ----------------')
    print(f'Time: {time.time() - start}s')
    print('Number of generations: ', i)
    print('Best fitness:', best_solution.fitness)
    print(*[solution.fitness for solution in population.evaluate()])
    return best_solution


def read_config(task_number: int):
    try:
        with open(f'./lab1_test_problems/lab1_test_problems/zad{task_number}.txt') as file:
            dimensions = file.readline().strip().split(sep=';')
            width, height = dimensions[0], dimensions[1]
            pairs = []
            for line in file:
                coordinates = line.strip().split(sep=';')
                pair = (Point(int(coordinates[0]), int(coordinates[1])), Point(int(coordinates[2]), int(coordinates[3])))
                pairs.append(pair)
            return Board(int(width), int(height), pairs)
    except FileNotFoundError:
        print('Config file with given name does not exist!')
        raise


def random_search(task_number: int = 1,
                  fitness_length_weight: float = 1,
                  fitness_segment_weight: float = 20,
                  fitness_intersection_weight: float = 1000,
                  corresponding_population_size: int = 300,
                  corresponding_iteration_count: int = 75):
    board = read_config(task_number)
    start = time.time()
    min_sol = None
    i = 0

    while (i < corresponding_population_size * corresponding_iteration_count):
        solution = Solution()
        solution.random_solve(board)
        if (min_sol is None or solution.fitness < min_sol.fitness):
            min_sol = solution
        i += 1

    print(f'Time: {time.time() - start}s')
    print('Best fitness:', min_sol.fitness)
    visualisation(board, min_sol, 30)


def main(task_number: int = 1,
         crossover_prob: float = 0.6,
         mutation_prob: float = 0.35,
         population_size: int = 300,
         selection_tournament: bool = True,
         reroll_prob: float = 0.6,
         iteration_count: int = 75,
         fitness_length_weight: float = 1,
         fitness_segment_weight: float = 20,
         fitness_intersection_weight: float = 1000,
         tournament_size: int = 4):
    board = read_config(task_number)

    best_solution = genetic_algorithm(board,
                                      crossover_prob,
                                      mutation_prob,
                                      population_size,
                                      selection_tournament,
                                      reroll_prob,
                                      iteration_count,
                                      fitness_length_weight,
                                      fitness_segment_weight,
                                      fitness_intersection_weight,
                                      tournament_size)

    # for path in solution:
    #     print(path)
    #     print(path.length)
    #     print()

    visualisation(board, best_solution, 30)


if __name__ == '__main__':
    # random_search(fitness_length_weight=1,
    #               fitness_segment_weight=20,
    #               fitness_intersection_weight=1000,
    #               corresponding_iteration_count=75,
    #               corresponding_population_size=300)

    main(task_number=1,
         crossover_prob=0.6,
         mutation_prob=0.35,
         population_size=300,
         selection_tournament=True,
         reroll_prob=0.6,
         iteration_count=500,
         fitness_length_weight=1,
         fitness_segment_weight=20,
         fitness_intersection_weight=1000,
         tournament_size=4)
