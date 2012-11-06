Presentation
============

Crystalpy is a Python program which can generate several kinds of periodic crystal mesh geometries for Gmsh:

* 2D or 3D
* rectangular or triangular (hexagonal) crystals

It can also:

* generate 2D SVG representations of those geometries
* define physical points in the meshes

Several types of inclusions can be defined:

* filled or not with a material
* circular, elliptic or rectangular
* inside or outside the host material

Crystalpy supports unit tests with nosetests.

Usage
=====

* Define the geometry of your crystal in mesh.py
* Run `python mesh.py`

Versions
========

* v. 1:   Can generate periodic 2D meshes, with multiple inclusion types
* v. 1.1: Add support for SVG output and triangular crystals
* v. 2:   Add support for 3D structures
* v. 2.1: Add support for elliptic inclusions
* v. 2.2: Add support for rectangular inclusions
* v. 2.3: Add support for plots
* v. 2.4: Add unit tests; fix periodicity conditions
* v. 2.5: Add support for physical points; fix 2D crystal generation
* v. 2.6: Add support for physical lines; fix 2D image generation
* v. 2.7: Add usage explanations; fix crystal position
