from collections import Counter


class ArffReader(object):
    """Parser for arff files."""

    def __init__(self, arff_file):
        """Initializes a reader with arff file."""
        self.arff_file = arff_file
        self.attributes = {}
        self.instances = []
        self.data = []  # same as instances but as list of dicts
        self.target_counts = Counter()
        self.parse()

    def parse(self):
        in_data = False
        attributes_order = []  # more efficient than collections.OrderedDict
        for line in self.arff_file:
            line = line.strip()
            if in_data:
                instance = line.split(',')
                self.instances.append(instance)
                self.data.append(dict(zip(attributes_order, instance)))
                self.target_counts[instance[-1]] += 1
            if '@relation' in line:
                name = line.split()[1]
                name_no_single_quotes = name[1:-1]
                self.relation_name = name_no_single_quotes
            elif '@attribute' in line:
                _, name, values = line.split()
                if values != 'numeric':
                    values_no_brackets = values[1:-1]
                    values = values_no_brackets.split(',')
                self.attributes[name] = values
                attributes_order.append(name)
                self.target = name  # always last one
            elif '@data' in line:
                in_data = True

        del self.attributes[self.target]


if __name__ == '__main__':
    # Example
    a = ArffReader(open('data.arff'))
    print(a.attributes)
    print(a.data)
    print(a.target_counts)
