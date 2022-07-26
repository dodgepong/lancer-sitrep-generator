# lancer-sitrep-generator
Automatic sitrep roster generator for the Lancer RPG system

## Usage

Requires Python 3+

To run, run `python3 generator.py`. This will create a roster for a random sitrep and 4 PCs.

To specify a sitrep, add `--sitrep <SITREP>` where `<SITREP>` is either Gauntlet, Holdout, Recon, Extraction, Escort, or Control.

To specify a player count. add `--players X` where X is your player count.

### Full command usage:
```
usage: generator.py [-h] [--sitrep SITREP] [--players PLAYERS]

Generate sitrep NPC compositions for Lancer

optional arguments:
  -h, --help            show this help message and exit
  --sitrep SITREP, -s SITREP
                        Name of sitrep to generate. Options are: Gauntlet, Holdout, Recon, Extraction, Escort, Control
  --players PLAYERS, -p PLAYERS
                        Number of player characters to generate the sitrep for
```

## Generator Restrictions

The generator attempts to create a sitrep according to the following requirements:

* A standard encounter budget is considered to be an amount of NPC structure/activations between 1.5x-2x the player count
    * For double-budget encounters, this increases to 3x-4x.
    * This heuristic is different from the Core book's recommendation, and is based on a great deal of testing by the Lancer GM community.
* No more than 50% of all structure + activations will come from strikers/artillery.
* Grunts are only ever added in groups of 2 or more. You will never get a sitrep that has only 1 grunt of a given class.
* For the sake of managing GM cognitive load, the generator uses between 3-5 classes per sitrep, and does not add classes with different templates to the same sitrep.
* No more than 1 Commander and/or 1 Ultra will be added to a sitrep, as these templates are most often reserved for "boss" or "leader" figures.