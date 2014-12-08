from collections import defaultdict

class ArffReader(object):
    """Parser for arff files."""

    def __init__(self, arff_file):
        """Initializes a reader with arff file."""
        self.arff_file = arff_file
        self.parse()

    def parse(self):
        in_data = False
        attributes = {}
        data = []
        self.target_counts = defaultdict(lambda: 0)
        for line in self.arff_file:
            line = line.strip()
            if in_data:
                instance = line.split(',')
                data.append(instance)
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
                self.target = name  # always last one
            elif '@data' in line:
                in_data = True
        self.attributes = attributes
        self.data = data

    def to_list_of_lists(self):
        return self.data

'''    
if __name__ == '__main__':
    # Example
    a = ArffReader(open('data.arff'))
    print(a.attributes)
    print(a.to_list_of_lists())
    print(a.target_counts)
'''
