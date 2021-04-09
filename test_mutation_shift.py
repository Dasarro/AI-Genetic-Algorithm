from lab1_genetic_algorithm import Point, Segment, Path, Solution, Board
import pytest


@pytest.mark.parametrize('path_before, path_after, segment_to_shift, shift_length, shift_direction', 
                         [([(0, 0), (4, 0), (4, 4), (8, 4), (8, 8)],
                          [(0, 0), (8, 0), (8, 8)], 1, 4, 1),
                          ([(0, 0), (0, 4), (4, 4), (4, 0)],
                           [(0, 0), (4, 0)], 1, 4, 0),
                          ([(0, 4), (4, 4), (4, 8), (8, 8), (8, 4), (12, 4)],
                           [(0, 4), (12, 4)], 2, 4, 0),
                          ([(0, 4), (4, 4), (4, 8), (8, 8), (8, 4), (12, 4)],
                           [(0, 4), (4, 4), (4, 6), (8, 6), (8, 4), (12, 4)], 2, 2, 0),
                          ([(6, 0), (6, 10), (5, 10), (5, 11), (6, 11)],
                           [(6, 0), (6, 11)], 2, 1, 1),
                          ([(6, 0), (6, 10), (5, 10), (5, 11), (6, 11)],
                           [(6, 0), (6, 11)], 1, 1, 1),
                          ([(0, 4), (4, 4), (4, 0), (8, 0), (8, 2), (6, 2)],
                           [(0, 4), (8, 4), (8, 2), (6, 2)], 1, 4, 1),
                          ([(0, 6), (0, 3), (3, 3), (3, 0), (6, 0), (6, 3), (4, 3), (4, 5)],
                           [(0, 6), (0, 3), (4, 3), (4, 5)], 2, 3, 1),
                          ([(0, 6), (0, 3), (3, 3), (3, 0), (6, 0), (6, 3), (4, 3), (4, 5)],
                           [(0, 6), (0, 3), (4, 3), (4, 5)], 3, 3, 1),
                          ([(0, 6), (0, 3), (3, 3), (3, 0), (6, 0), (6, 3), (4, 3), (4, 5)],
                           [(0, 6), (0, 3), (4, 3), (4, 5)], 4, 3, 0),
                          ([(0, 6), (0, 3), (3, 3), (3, 0), (6, 0), (6, 3), (4, 3), (4, 5)],
                           [(0, 6), (0, 3), (3, 3), (3, 0), (4, 0), (4, 5)], 5, 3, 0)])
def test_mutation_shift(path_before, path_after, segment_to_shift, shift_length, shift_direction):
    points = []
    for point in path_before:
        points.append(Point(point[0], point[1]))
    path_before = []
    for point_i in range(len(points) - 1):
        path_before.append(Segment(points[point_i], points[point_i + 1]))
    path_before = Path(path_before)
    
    solution = Solution()
    solution.setPaths([path_before])
    solution.mutate_shift(Board(20, 20, []), True, segment_to_shift, shift_length, shift_direction)

    points = []
    for point in path_after:
        points.append(Point(point[0], point[1]))
    path_after = []
    for point_i in range(len(points) - 1):
        path_after.append(Segment(points[point_i], points[point_i + 1]))
    path_after = Path(path_after)

    try:
        assert solution.paths[0] == path_after
    except AssertionError:
        print('After mutation:\n', solution.paths[0])
        print('Expected result:\n', path_after)
        raise
