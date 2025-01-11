import FreeCAD
import Part
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#import stair_classes  # Import your stair classes
from stairClasses import Stairs  # Import classes from stairClasses.py


def draw_treads_in_freecad(stairs):
    """Draw the treads in FreeCAD."""
    doc = FreeCAD.newDocument("Stairs")

    for i, tread in enumerate(stairs.treads):
        # Create the four lines for each tread
        riser_line = Part.LineSegment(FreeCAD.Vector(tread.riserLine.start.x, tread.riserLine.start.y, 0),
                                      FreeCAD.Vector(tread.riserLine.end.x, tread.riserLine.end.y, 0))
        RH_line = Part.LineSegment(FreeCAD.Vector(tread.RHLine.start.x, tread.RHLine.start.y, 0),
                                   FreeCAD.Vector(tread.RHLine.end.x, tread.RHLine.end.y, 0))
        back_line = Part.LineSegment(FreeCAD.Vector(tread.backLine.start.x, tread.backLine.start.y, 0),
                                     FreeCAD.Vector(tread.backLine.end.x, tread.backLine.end.y, 0))
        LH_line = Part.LineSegment(FreeCAD.Vector(tread.LHLine.start.x, tread.LHLine.start.y, 0),
                                   FreeCAD.Vector(tread.LHLine.end.x, tread.LHLine.end.y, 0))

        # Create a Part.Shape for each line and add to the document
        riser_obj = doc.addObject("Part::Feature", f"Tread{i+1}_Riser")
        riser_obj.Shape = riser_line.toShape()

        RH_obj = doc.addObject("Part::Feature", f"Tread{i+1}_RH")
        RH_obj.Shape = RH_line.toShape()

        back_obj = doc.addObject("Part::Feature", f"Tread{i+1}_Back")
        back_obj.Shape = back_line.toShape()

        LH_obj = doc.addObject("Part::Feature", f"Tread{i+1}_LH")
        LH_obj.Shape = LH_line.toShape()

    # Recompute the document to update
    doc.recompute()


# Example usage
if __name__ == "__main__":
    overall_height = 3000
    number_of_steps = 15
    angle = 30  # Angle of the stairs in degrees
    width = 1000  # Width of the stairs

    # Create the stairs
    stairs = Stairs(overall_height, number_of_steps, angle, width)

    # Draw the stairs in FreeCAD
    draw_treads_in_freecad(stairs)
