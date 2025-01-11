import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Line({self.start}, {self.end})"


class Tread:
    def __init__(self, stairs, origin_x: float, origin_y: float):
        """Initialize a tread using parameters from the Stairs instance."""
        self.going = stairs.going
        self.width = stairs.width

        # Define lines for each part of the tread (viewed from above)
        self.riserLine = Line(Point(origin_x, origin_y), Point(origin_x + self.width, origin_y))  # Front edge
        self.RHLine = Line(Point(origin_x + self.width, origin_y), Point(origin_x + self.width, origin_y + self.going))  # Right edge
        self.backLine = Line(Point(origin_x + self.width, origin_y + self.going), Point(origin_x, origin_y + self.going))  # Back edge
        self.LHLine = Line(Point(origin_x, origin_y + self.going), Point(origin_x, origin_y))  # Left edge

    def __repr__(self):
        return f"Tread(Width={self.width}, Going={self.going})"


class Stairs:
    def __init__(self, overall_height, number_of_steps, angle, width):
        """Initialize the stairs with parameters."""
        self.overall_height = overall_height
        self.number_of_steps = number_of_steps
        self.angle = angle
        self.width = width

        # Calculate derived values
        self.gain = overall_height / number_of_steps  # Height of each step
        self.going = self.gain / math.tan(math.radians(angle))  # Horizontal depth of each tread

        self.treads = []  # List to hold all the treads
        self.create_treads()

    def create_treads(self):
        """Generate the treads based on the number of steps."""
        x, y = 0, 0  # Start at the bottom-left corner
        for _ in range(self.number_of_steps):
            tread = Tread(self, origin_x=x, origin_y=y)
            self.treads.append(tread)
            y += self.going  # Move up by the going for the next tread

    def __repr__(self):
        return f"Stairs(Height={self.overall_height}, Steps={self.number_of_steps}, Width={self.width}, Angle={self.angle})"
