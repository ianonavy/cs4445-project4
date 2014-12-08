from arff import ArffReader
from math import log


def info_gain(p0, n0, p1, n1):
    """Calculates info gain

    p0: # of instances such that antecedent is true
    n0: # of instances such that antecedent is false
    p1: # of instances such that consequent and antecedent are true
    n1: # of instances such that consequent is true but and antecedent is false
    """
    return p1 * (log(p1 / (p1 + n1), 2) - log(p0 / (p0 + n0), 2))


class Rule(object):

    def __init__(self, conditions, consequent):
        self.conditions = conditions
        self.consequent = consequent

    def get_antecedent(self):
        antecedent_parts = [
            "{} = {}".format(attr, val)
            for attr, val in self.conditions.items()
        ]
        return " and ".join(antecedent_parts)

    def get_consequent(self):
        return "{} = {}".format(*self.consequent)

    def __str__(self):
        return "'{} -> {}'".format(self.get_antecedent(), self.get_consequent())


class Ripper(object):

    def __init__(self, reader):
        self.reader = reader

    def get_ig_params(self, data, attr, val, target, target_val):
        """Gets the parameters for InformationGain.

        :param data: Instances as a list of dicts
        :param attr: The current attribute tested
        :param val: The value of the attribute tested
        :param target: The target attribute
        :param target_val: The value for the target in the consequent
        :return: Tuple of parameters for info_gain
        """
        matches_target = lambda d: d[target] == target_val
        matches_attr = lambda d: d[attr] == val and d[target] == target_val
        no_match_attr = lambda d: d[attr] == val and d[target] != target_val
        p0 = len(list(filter(matches_target, data)))
        n0 = len(data) - p0
        p1 = len(list(filter(matches_attr, data)))
        n1 = len(list(filter(no_match_attr, data)))
        return p0, n0, p1, n1

    def get_conditions(self, target, target_val, previous_conditions, data):
        """Recursively computes the conditions needed for

        :param target: The target attribute
        :param target_val: The value for the target in the consequent
        :param previous_conditions: dict of previous conditions found so far
        :param data: data instances that match the previous conditions
        :return: The list of conditions that maximize information gain

        """
        consequent = (target, target_val)
        print("Conditions so far: {}".format(previous_conditions))
        print("Rule so far: {}".format(Rule(previous_conditions, consequent)))
        conditions = previous_conditions

        gained_new_info = False
        max_info_gain = None
        chosen_attribute = None
        chosen_value = None

        # Get attribute with highest info gain, breaking ties arbitrarily
        for attribute, values in self.reader.attributes.items():
            for value in values:
                p0, n0, p1, n1 = self.get_ig_params(data, attribute, value,
                                                    target, target_val)
                try:
                    ig = info_gain(p0, n0, p1, n1)
                except (ValueError, ZeroDivisionError):
                    pass
                else:
                    print("Trying {} = {}\n> ".format(attribute, value), end='')
                    print("InfoGain({}, {}, {}, {}) = {}".format(
                        p0, n0, p1, n1, ig))
                    if max_info_gain is None or ig > max_info_gain:
                        max_info_gain = ig
                        chosen_attribute, chosen_value = attribute, value
                    if ig > 0:
                        gained_new_info = True

        # If chosen attribute actually gains info
        if gained_new_info:
            print('Picked {} = {}\n'.format(chosen_attribute, chosen_value))
            conditions.update({chosen_attribute: chosen_value})
            has_chosen_attr = lambda i: i[chosen_attribute] == chosen_value
            data = list(filter(has_chosen_attr, data))

            # If there's more data to check:
            if len(data) > 0:
                conditions.update(
                    self.get_conditions(target, target_val, conditions, data))
        return conditions

    def first_rule(self):
        """Calculates the first rule by choosing the least common value for the
        target attribute and greedily adding conditions.
        """
        print("Calculating first rule.")
        target = self.reader.target
        target_val = self.reader.target_counts.most_common()[-1][0]

        print("Consequent: '{} = {}'\n".format(target, target_val))
        data = self.reader.data
        conditions = self.get_conditions(target, target_val, {}, data)
        return Rule(conditions, (target, target_val))


def main():
    reader = ArffReader(open('data.arff'))
    ripper = Ripper(reader)
    print("\nFirst rule: {}".format(ripper.first_rule()))


if __name__ == '__main__':
    main()
