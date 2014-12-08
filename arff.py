from collections import Counter


class ArffReader(object):
    """Parser for arff files."""

    def __init__(self, arff_file):
        """Initializes a reader with arff file."""
        self.arff_file = arff_file
        self.parse()

    def parse(self):
        in_data = False
        attributes = {}
        attributes_order = []  # more efficient than collections.OrderedDict
        instances = []
        data = []
        self.target_counts = Counter()
        for line in self.arff_file:
            line = line.strip()
            if in_data:
                instance = line.split(',')
                instances.append(instance)
                data.append(dict(zip(attributes_order, instance)))
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
                attributes[name] = values
                attributes_order.append(name)
                self.target = name  # always last one
            elif '@data' in line:
                in_data = True

        self.attributes = attributes
        self.instances = instances
        self.data = data
        del self.attributes[self.target]


if __name__ == '__main__':
    # Example
    a = ArffReader(open('data.arff'))
    print(a.attributes)
    print(a.data)
    print(a.target_counts)
