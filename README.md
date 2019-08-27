# evolvesaveeditor
A save editor for the game "Evolve"

[![Travis Build Status](https://travis-ci.org/mattgiltaji/evolvesaveeditor.svg?branch=master)](https://travis-ci.org/mattgiltaji/evolvesaveeditor)
[![Appveyor Build Status](https://ci.appveyor.com/api/projects/status/csp5r4mtud3fy4i5/branch/master?svg=true)](https://ci.appveyor.com/project/mattgiltaji/evolvesaveeditor/branch/master)
[![Coverage Status](https://coveralls.io/repos/github/mattgiltaji/evolvesaveeditor/badge.svg?branch=master)](https://coveralls.io/github/mattgiltaji/evolvesaveeditor?branch=master)
![GitHub License](https://img.shields.io/github/license/mattgiltaji/evolvesaveeditor)

Evolve is a game by [pmotschmann](https://github.com/pmotschmann/Evolve) and is playable at https://pmotschmann.github.io/Evolve/

### Features
This save editor can currently do these things:
   * Adjust prestige currencies (Plasmids, Phages, and Dark)
   * Fill resources to maximum (or a big number for resources without a max)
   * Update resources' assigned containers and crates (when Freight Yard and/or Container Port are built)
   * Adjust building counts (but won't add the first building of its kind as that breaks things)
   * Update number of citizens to maximum supported by housing buildings
   * Update number of soldiers to maximum supported by barracks buildings and heals all troops.
   * Adjust A.R.P.A. research projects to 99% complete
   * Update genetic sequencing to 5 seconds from completion
   
### How To Use
To use this save editor:
   1. Have version 3.6 or higher [Python](https://www.python.org/downloads/) installed on your local machine.
   1. Export save from Settings tab in Evolve.
   1. Copy & Paste that exported save data into a file on your local machine.
   1. Save and close the file.
   1. Run the evolvesaveeditor.py script in your favorite command line and pass in the path to the save file, like so:
      ```
      python .\evolvesaveeditor.py "c:\path\to\save\file.txt"
      ```
   1. Open the save file on your local machine and copy the contents.
   1. Paste the contents into the import/export textarea on the settings tab in Evolve.
   1. Click the "Import Game" button on the settings tab in Evolve.
