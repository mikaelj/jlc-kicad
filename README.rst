===========================
Tiny JLCPCB Tools for KiCad
===========================

Tools for KiCad for using JLCPCB's assembly-service.

jlcpcb-library.sh
=================
Thin wrapper around the JLC2KiCadLib tool (https://github.com/matthewlai/JLCKicadTools) that actually performs the downloading and conversion.

This adds functionality to read parts from a file, automatically setting SMT attribute if needed, plus an optionaal patch system for fixing footprint files.

Usage::

    jlcpcb-library.sh <parts-file> <library name> [patches dir]

Example invocation, creating the directory Foo containing the schematics library and footprint library::

    jlcpcb-library.sh foo-parts.txt Foo foo-patches

Note: the library will be overwritten each time, so don't make any changes to the files after running the tool -- use the patches system.

parts-file
~~~~~~~~~~
Contains ``Cxxxxx`` LSC part numbers, one per line. Comments are allowed and start with '#', eiter on a separate line or the same row.

Example::
    
    # 5V-regulator
    C97643 # (E) Step-down 4,75-40V 1A SOT-23-6
    # Connectors
    C2897378 # EXTENDED 5 pin female socket header 2,54 through hole.

library-name
~~~~~~~~~~~~~
Name of the library in KiCad, and also the filename.

Example: ``AwesomeProject``

patches-dir
~~~~~~~~~~~~
Optional directory of patches for the footprint files (```.kicad_mod```` files), for fixing e.g. wrong placement.

Example::

    AwesomeProject-patches:
        PG-DSO-8_L5.0-W4.0-P1.27-LS6.0-BL.kicad_mod.patch

Contents of ``PG-DSO-8_L5.0-W4.0-P1.27-LS6.0-BL.kicad_mod.patch`` - a fix for 3D model placement on footprint::

    --- Larmpryl/Larmpryl/PG-DSO-8_L5.0-W4.0-P1.27-LS6.0-BL.kicad_mod.original	2023-03-18 17:43:48
    +++ Larmpryl/Larmpryl/PG-DSO-8_L5.0-W4.0-P1.27-LS6.0-BL.kicad_mod	2023-03-18 17:44:23
    @@ -28,8 +28,8 @@
         (effects (font (size 1 1) (thickness 0.15)))
       )
       (model /Users/mikaelj/code/goride/nano33/larmpryl/libs/Larmpryl/Larmpryl/packages3d/PG-DSO-8_L5.0-W4.0-P1.27-LS6.0-BL.wrl
    -    (at (xyz 0.02 0.014 0.00195))
    +    (at (xyz 0.0 0.0 0.0))
         (scale (xyz 1 1 1))
         (rotate (xyz 0 0 -90))
       )
    -)
    \ No newline at end of file
    +)


jlcpcb-postprocess.py
=====================
For use with the KiCad JLCPCB fabrication toolkit.  Processes BOM file and positions file to match the JLCPCB input format.

---------------

Copyright and stuff: use as you wish, please let me know if you find it useful. :-)

