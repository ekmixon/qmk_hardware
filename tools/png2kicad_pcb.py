#!/usr/bin/env python
#
# png2kicad_pcb - converts one (or two) RGBA pngs to a .kicad_pcb file
#
# Copyright 2017 Jack Humbert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from PIL import Image, ImageOps
import numpy as np
import potrace
from shapely.geometry import Point, Polygon
import png2kicad_mod

# Text for the file header, the parameter is the name of the module, ex "LOGO".
pcb_header = """(kicad_pcb (version 4) (host pcbnew 4.0.6)

  (general
    (links 0)
    (no_connects 0)
    (area 44.9 37.5582 278.552718 120.126051)
    (thickness 1.6)
    (drawings 0)
    (tracks 0)
    (zones 0)
    (modules 1)
    (nets 1)
  )

  (page A4)
  (layers
    (0 F.Cu signal)
    (31 B.Cu signal)
    (32 B.Adhes user)
    (33 F.Adhes user)
    (34 B.Paste user)
    (35 F.Paste user)
    (36 B.SilkS user)
    (37 F.SilkS user)
    (38 B.Mask user)
    (39 F.Mask user)
    (40 Dwgs.User user)
    (41 Cmts.User user)
    (42 Eco1.User user)
    (43 Eco2.User user)
    (44 Edge.Cuts user)
    (45 Margin user)
    (46 B.CrtYd user)
    (47 F.CrtYd user)
    (48 B.Fab user)
    (49 F.Fab user)
  )

  (setup
    (last_trace_width 0.25)
    (trace_clearance 0.2)
    (zone_clearance 0.508)
    (zone_45_only no)
    (trace_min 0.2)
    (segment_width 0.2)
    (edge_width 0.15)
    (via_size 0.6)
    (via_drill 0.4)
    (via_min_size 0.4)
    (via_min_drill 0.3)
    (uvia_size 0.3)
    (uvia_drill 0.1)
    (uvias_allowed no)
    (uvia_min_size 0.2)
    (uvia_min_drill 0.1)
    (pcb_text_width 0.3)
    (pcb_text_size 1.5 1.5)
    (mod_edge_width 0.15)
    (mod_text_size 1 1)
    (mod_text_width 0.15)
    (pad_size 1.524 1.524)
    (pad_drill 0.762)
    (pad_to_mask_clearance 0.2)
    (aux_axis_origin 38.25 36.75)
    (grid_origin 38.25 36.75)
    (visible_elements 7FFFFFFF)
    (pcbplotparams
      (layerselection 0x010fc_80000001)
      (usegerberextensions true)
      (excludeedgelayer true)
      (linewidth 0.100000)
      (plotframeref false)
      (viasonmask false)
      (mode 1)
      (useauxorigin false)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15)
      (hpglpenoverlay 2)
      (psnegative false)
      (psa4output false)
      (plotreference true)
      (plotvalue true)
      (plotinvisibletext false)
      (padsonsilk false)
      (subtractmaskfromsilk false)
      (outputformat 1)
      (mirror false)
      (drillshape 0)
      (scaleselection 1)
      (outputdirectory .))
  )

  (net 0 "")

  (net_class Default "This is the default net class."
    (clearance 0.2)
    (trace_width 0.25)
    (via_dia 0.6)
    (via_drill 0.4)
    (uvia_dia 0.3)
    (uvia_drill 0.1)
  )
"""

pcb_footer = "\n)"

def main():
    import sys

    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input_name dpi")
        print("  input_name is added to \"_front.png\" (and \"_back.png\") ")
        print("  dpi is the dots per inch of the input file\"")
        sys.exit(1)

    input_name = sys.argv[1]
    dpi = int(sys.argv[2])

    module, size = png2kicad_mod.conv_image_to_module(input_name, dpi)
    module = pcb_header + module + pcb_footer
    print("Output image size: %f x %f mm" % (size[0], size[1]))
    print("Writing module file to \"%s.kicad_pcb\"" % input_name)
    with open(f"{input_name}.kicad_pcb", "w") as fid:
        fid.write(module)

if __name__ == "__main__":
    main()

