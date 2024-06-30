'''
test the min_partition module
Programmer: Dvir Borochov
Date: 10/6/24 
'''
import unittest
from shapely.algorithms.min_partition import RectilinearPolygon
from shapely.geometry import Polygon, Point, LineString
import shapely.algorithms.min_partition as p


class TestPolygonPartitioning(unittest.TestCase):
    def setUp(self):
        # Define polygons for testing
        self.polygon1 = Polygon([(2, 0), (6, 0), (6, 4), (8, 4), (8, 6), (0, 6), (0, 4), (2, 4)])
        self.polygon2 = Polygon([(1, 5), (1, 4), (3, 4), (3, 2), (5, 2), (5, 1), (8, 1), (8, 5)])
        self.polygon3 = Polygon([(0, 4), (2, 4), (2, 0), (5, 0), (5, 4), (7, 4), (7, 5), (0, 5)])
        self.polygon4 = Polygon([(1, 5), (1, 4), (3, 4), (3, 3), (2, 3), (2, 1), (5, 1), (5, 2), (8,2), (8,1), (9,1), (9,4), (8,4), (8,5)])
        self.polygon5 = Polygon([(1,1), (1,9), (9,9), (9,1)])  # Rectangle
        self.polygon6 = Polygon([(1,1), (1,9), (9,9), (9,7)])  # Not rectilinear polygon

        # Create RectilinearPolygon instances
        self.rect_polygon1 = RectilinearPolygon(self.polygon1)
        self.rect_polygon2 = RectilinearPolygon(self.polygon2)
        self.rect_polygon3 = RectilinearPolygon(self.polygon3)
        self.rect_polygon4 = RectilinearPolygon(self.polygon4)
        self.rect_polygon5 = RectilinearPolygon(self.polygon5)
        self.rect_polygon6 = RectilinearPolygon(self.polygon6)

    def test_is_rectilinear(self):
        self.assertTrue(self.rect_polygon1.is_rectilinear())
        self.assertTrue(self.rect_polygon2.is_rectilinear())
        self.assertTrue(self.rect_polygon3.is_rectilinear())
        self.assertTrue(self.rect_polygon4.is_rectilinear())
        self.assertTrue(self.rect_polygon5.is_rectilinear())
        self.assertFalse(self.rect_polygon6.is_rectilinear())

    def test_find_convex_points(self):
        convex_point1 = self.rect_polygon1.find_convex_points()
        self.assertIsInstance(convex_point1, Point)

    def test_get_grid_points(self):
        grid_points1 = self.rect_polygon1.get_grid_points()
        self.assertGreater(len(grid_points1), 0)
        self.assertTrue(all(isinstance(point, Point) for point in grid_points1))

    def test_partition_polygon(self):
        for polygon in [self.polygon1, self.polygon2, self.polygon3, self.polygon4]:
            partition_result = p.partition_polygon(polygon)
            self.assertIsInstance(partition_result, list)
            self.assertTrue(all(isinstance(line, LineString) for line in partition_result))

        # Test rectangle (should return None)
        self.assertIsNone(p.partition_polygon(self.polygon5))

        # Test non-rectilinear polygon (should return None)
        self.assertIsNone(p.partition_polygon(self.polygon6))

    def test_get_new_internal_edges(self):
        blocked_rect = Polygon([(2,4), (6,4), (6, 0), (2, 0)])
        new_internal_edges = self.rect_polygon1.get_new_internal_edges(blocked_rect)
        self.assertGreater(len(new_internal_edges), 0)
        self.assertIsInstance(new_internal_edges[0], LineString)

    def test_is_concave_vertex(self):
        coords = list(self.polygon1.exterior.coords)
        self.assertTrue(self.rect_polygon1.is_concave_vertex(2, coords))

    def test_find_matching_point(self):
        candidate_point = Point(2, 4)
        matching_and_blocks = self.rect_polygon1.find_matching_point(candidate_point, self.polygon1)
        self.assertGreater(len(matching_and_blocks), 0)
        self.assertIsInstance(matching_and_blocks[0][0], Point)
        self.assertIsInstance(matching_and_blocks[0][1], Polygon)

    def test_is_rectangle(self):
        rectangle = Polygon([(0,0), (0,1), (1,1), (1,0)])
        self.assertTrue(self.rect_polygon1.is_rectangle(rectangle))

if __name__ == '__main__':
    unittest.main()