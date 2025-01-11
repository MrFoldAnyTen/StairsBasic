import FreeCAD as App
import FreeCADGui as Gui
import Sketcher
import PartDesign
import Part
import os
import sys

# Ensure the script can find the stairClasses file
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stairClasses import Stairs


def create_tread_in_part_design(doc, tread, base_position, index, gain):
    """Create a single tread as a PartDesign::Body with a sketch and pad."""
    body = doc.addObject("PartDesign::Body", f"Tread_{index}")
    sketch = body.newObject("Sketcher::SketchObject", f"Sketch_Tread_{index}")

    # Add geometry
    l1 = sketch.addGeometry(Part.LineSegment(App.Vector(tread.riserLine.start.x, tread.riserLine.start.y, 0),
                                             App.Vector(tread.riserLine.end.x, tread.riserLine.end.y, 0)), False)
    l2 = sketch.addGeometry(Part.LineSegment(App.Vector(tread.RHLine.start.x, tread.RHLine.start.y, 0),
                                             App.Vector(tread.RHLine.end.x, tread.RHLine.end.y, 0)), False)
    l3 = sketch.addGeometry(Part.LineSegment(App.Vector(tread.backLine.start.x, tread.backLine.start.y, 0),
                                             App.Vector(tread.backLine.end.x, tread.backLine.end.y, 0)), False)
    l4 = sketch.addGeometry(Part.LineSegment(App.Vector(tread.LHLine.start.x, tread.LHLine.start.y, 0),
                                             App.Vector(tread.LHLine.end.x, tread.LHLine.end.y, 0)), False)

    # Add constraints
    sketch.addConstraint(Sketcher.Constraint("Coincident", l1, 2, l2, 1))  # Bottom-right to Top-right
    sketch.addConstraint(Sketcher.Constraint("Coincident", l2, 2, l3, 1))  # Top-right to Top-left
    sketch.addConstraint(Sketcher.Constraint("Coincident", l3, 2, l4, 1))  # Top-left to Bottom-left
    sketch.addConstraint(Sketcher.Constraint("Coincident", l4, 2, l1, 1))  # Bottom-left to Bottom-right

    # Horizontal and vertical constraints
    sketch.addConstraint(Sketcher.Constraint("Horizontal", l1))  # Bottom line
    sketch.addConstraint(Sketcher.Constraint("Horizontal", l3))  # Top line
    sketch.addConstraint(Sketcher.Constraint("Vertical", l2))  # Right line
    sketch.addConstraint(Sketcher.Constraint("Vertical", l4))  # Left line

    # Pad the sketch
    pad = body.newObject("PartDesign::Pad", f"Pad_Tread_{index}")
    pad.Profile = sketch
    pad.Length = gain

    # Position the body
    body.Placement = App.Placement(base_position + App.Vector(0, 0, (index - 1) * gain), App.Rotation(0, 0, 0))
    return body


# Main script to create stairs
def main():
    doc = App.newDocument("Stairs")
    overall_height = 3.0
    number_of_steps = 10
    angle = 35
    width = 1.0

    base_position = App.Vector(0, 0, 0)

    # Create Stairs
    stairs = Stairs(overall_height, number_of_steps, angle, width)

    # Generate treads
    for index, tread in enumerate(stairs.treads, start=1):
        create_tread_in_part_design(doc, tread, base_position, index, stairs.gain)

    # Recompute and view
    doc.recompute()
    Gui.activeDocument().activeView().viewAxometric()
    Gui.SendMsgToActiveView("ViewFit")


if __name__ == "__main__":
    main()
