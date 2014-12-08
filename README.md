CS 4445 Homework 4
==================

Ian Naval and Laurentiu Pavel

Requirements: python 3+ (comes with most UNIX-based systems)

## Running

### RIPPER

    python3 ripper.py data.arff

1. You can see the step-by-step in this sample output:

    Calculating first rule.
    Consequent: 'class = good'

    Conditions so far: {}
    Rule so far: ' -> class = good'
    Trying maint = med
    > InfoGain(2, 20, 2, 4) = 3.748938235832283
    Trying buying = high
    > InfoGain(2, 20, 1, 3) = 1.4594316186372978
    Trying buying = low
    > InfoGain(2, 20, 1, 4) = 1.1375035237499356
    Trying persons = 4
    > InfoGain(2, 20, 2, 9) = 2.000000000000001
    Trying safety = high
    > InfoGain(2, 20, 2, 3) = 4.275007047499871
    Picked safety = high

    Conditions so far: {'safety': 'high'}
    Rule so far: 'safety = high -> class = good'
    Trying maint = med
    > InfoGain(2, 3, 2, 0) = 2.6438561897747244
    Trying buying = high
    > InfoGain(2, 3, 1, 1) = 0.3219280948873622
    Trying buying = low
    > InfoGain(2, 3, 1, 2) = -0.2630344058337941
    Trying persons = 4
    > InfoGain(2, 3, 2, 0) = 2.6438561897747244
    Trying safety = high
    > InfoGain(2, 3, 2, 3) = 0.0
    Picked maint = med

    Conditions so far: {'safety': 'high', 'maint': 'med'}
    Rule so far: 'safety = high and maint = med -> class = good'
    Trying maint = med
    > InfoGain(2, 0, 2, 0) = 0.0
    Trying buying = high
    > InfoGain(2, 0, 1, 0) = 0.0
    Trying buying = low
    > InfoGain(2, 0, 1, 0) = 0.0
    Trying persons = 4
    > InfoGain(2, 0, 2, 0) = 0.0
    Trying safety = high
    > InfoGain(2, 0, 2, 0) = 0.0

First rule: 'safety = high and maint = med -> class = good'


As you can see, the 2nd step has a tie between `maint = med` and `person = 4`.
The code breaks ties arbitrarily since the ordering depends on the internal
ordering of a Python dictionary, which is undefined.

2. The pruning step for this rule keeps part of the training set that was not
used to construct the rule as a validation set. It uses the metric "(p-n)/(p+n)"
where p is the number of positive examples covered by the first rule in the
validation set, and n is the number of negative examples. It then calculates
this metric for each final sequence of conditions and keeps the pruned version
which maximizes the metric.