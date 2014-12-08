CS 4445 Homework 4
==================

Ian Naval and Laurentiu Pavel

Requirements: python 3+ (comes with most UNIX-based systems)

## Running

### RIPPER

    python3 ripper.py data.arff

1. Classification Rules using RIPPER

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


---------------------------------------------------------
### Apriori

    python Apriori.py



2. Association rules using Apriori

1.1. The "join condition" is the condition needed to be satisfied in the Fk-1xFk-1
in order to be able to merge the two subsets. Basically it goes through the first
k-2 elements for each subset and if they are not the same, they do not obey the
"join" condition. If they are the same, check that the k-1 element is different
for each of the subsets (not having the same attribute with differnet values).
If this conditions are obeyed, then the condition is satisfied

1.2. The subset condition is the condition that makes sure that after merging, the
obtained subset does not contain combinations of other subsets that were already
checked not to have enough support. This makes sure that the counting doesn't
start before all the pruning has been done which minimizes the number of times it
is needed to go through all the elements in the dataset and therefore reduces the
time make the computations

1.3. In general, a level is computed in the function createNextLevel() in the Apriori.py.
1.3.1 The join condition has been implemented in the function isOneDifferent(), which
takes 2 subsets and check if they obey the join condition as it was described at 1.
1.3.2 The subset conditoin is checked in the function isValidNewTuple(). This function
takes the combinations of the the subsets of the newly created subset and makes sure
they have not already been categorized as not having enough support. Only if this
condition doesn't hold, then compute the support.
1.3.3 The support for remaining itemsets is taken care of in the function checkSupport()
which loops through all the data instances and checks if there is an expected match.

1.4 The termination condition can be found in the while loop of the function apriori().
The generation will stop when there is a level that doesn't have any rules with enough
support. 


2. lift = confidence / prob(consequence) = confidence/(consequnceCount/totalTransactions)
   leverage = prob(premise & consequence) - (prob(premise) * prob(consequence))
   conviction = prob(premise) * prob(!consequence) / prob(premise & !consequence)

On this dataset, the code is building the following rule and it calculates the following
values for lift, leverage, and conviction
[('persons', '4')]->[('maint', 'high')]
confidence: 0.666666666667
leverage:0.0227272727273
conviction:2.11111111111

3. Observation: In this dataset, on the last dataset, both subsets have the same frequency.
Therefore just flip a coin( in this example take the latest one will be taken for 
simplicity)
3.1 and 3.2. The following content is auto-generated by solveThirdTask in Apriori.py. It
contains the rule followed by the confidence and leverage
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '2'), ('safety', 'med')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '2'), ('safety', 'high')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '2'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0371900826446
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '2'), ('buying', 'low')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '4'), ('safety', 'low')]
confidence: 0.0
leverage:-0.0309917355372
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '4'), ('safety', 'med')]
confidence: 0.75
leverage:0.111570247934
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '4'), ('maint', 'vhigh')]
confidence: 0.666666666667
leverage:0.0723140495868
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '4'), ('maint', 'med')]
confidence: 0.0
leverage:-0.0247933884298
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '4'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0371900826446
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '4'), ('class', 'acc')]
confidence: 1.0
leverage:0.117768595041
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '4'), ('buying', 'high')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', '4'), ('buying', 'med')]
confidence: 0.5
leverage:0.099173553719
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', 'more'), ('safety', 'med')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', 'more'), ('maint', 'vhigh')]
confidence: 0.0
leverage:-0.0247933884298
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', 'more'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('persons', 'more'), ('buying', 'med')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('safety', 'low'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0433884297521
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('safety', 'low'), ('buying', 'med')]
confidence: 0.0
leverage:-0.0309917355372
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('safety', 'med'), ('maint', 'vhigh')]
confidence: 0.285714285714
leverage:0.047520661157
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('safety', 'med'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0309917355372
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('safety', 'med'), ('class', 'acc')]
confidence: 0.6
leverage:0.105371900826
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('safety', 'med'), ('buying', 'med')]
confidence: 0.5
leverage:0.099173553719
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('safety', 'high'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('safety', 'high'), ('buying', 'low')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('maint', 'vhigh'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0371900826446
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('maint', 'vhigh'), ('class', 'acc')]
confidence: 0.666666666667
leverage:0.0723140495868
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('maint', 'vhigh'), ('buying', 'med')]
confidence: 0.333333333333
leverage:0.0537190082645
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('maint', 'high'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('maint', 'med'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('maint', 'low'), ('class', 'unacc')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('class', 'unacc'), ('buying', 'high')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('class', 'unacc'), ('buying', 'med')]
confidence: 0.0
leverage:-0.0433884297521
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('class', 'unacc'), ('buying', 'low')]
confidence: 0.0
leverage:-0.0185950413223
----------------------------
[('persons', '4'), ('safety', 'med'), ('class', 'acc'), ('buying', 'med')] ==> [('class', 'acc'), ('buying', 'med')]
confidence: 0.75
leverage:0.111570247934


4. lowerBoundMinSupport - used as lower bound for the minimum support. However, the 
   			  min support may decrease so that enough rules are found
upperBoundMinSupport - it is used for prunning rules for upper bound min support
delta - the amount with which the support is decreased when more rules are needed
metricType - the metric used (can be CONFIDENCE, LIFT, LEVERAGE, CONVICTION)
minMetric - the minimum confidence of a rule
numRules - the required number of rules