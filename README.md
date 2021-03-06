[![Build Status](https://travis-ci.org/mmcauliffe/python-acoustic-similarity.svg?branch=master)](https://travis-ci.org/mmcauliffe/python-acoustic-similarity)[![Coverage Status](https://coveralls.io/repos/mmcauliffe/python-acoustic-similarity/badge.svg)](https://coveralls.io/r/mmcauliffe/python-acoustic-similarity)

python-acoustic-similarity
==================

This package contains functions for converting wav files into auditory 
representations and calculating distance between them.

Auditory representations currently supported are mel-frequency cepstrum
coefficients (MFCCs) and amplitude envelopes.

Distance metrics currently implemented are dynamic time warping and inverse
cross-correlation.

Installation
==================

1. This package requires numpy and scipy to be installed.  Precompiled 
Windows binaries can be found at http://www.lfd.uci.edu/~gohlke/pythonlibs/.
Further information is available at http://www.scipy.org/install.html

2. Clone the repository or download the zip file.

3.  In the root directory of the repository, enter `python setup.py install`.

Higher level wrappers
==================

In `acousticsim/main.py` there are several wrapper functions for convenience.

Each of these functions takes keyword arguments corresponding to how auditory
representations should be constructed and what distance function to use.

**acoustic_similarity_mapping** takes a mapping of paths as its argument.
This argument should be a list of pairs or triplets of fully specified filenames.
Pairs will compute the distance between the two files, and triplets will compute
an AXB style design, where distances are computed between the first element and the second and
between the third element and the second.  In this case, the numerical output
will be a ratio of the third element's distance to the second divided by the
first element's distance to the second.  The return value is a dictionary
with the pairs/triplets as keys, and the numerical output as the values.

**acoustic_similarity_directories** takes two arguments which are fully specified paths
to two directories.  It then constructs a path mapping of all the files in
the first directory to all the files in the second directory.  The return
value is a single value, which the average distance of all those calculated.

**analyze_directory** takes a single directory as an argument and creates a
path mapping of all the files compared to all other files. The return value is a dictionary
with the file pairs as keys, and the numerical output as the values.


