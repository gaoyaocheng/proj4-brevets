class Rules():
    def __init__(self, rule_file):
        self.rules = [];
        if isinstance(rule_file, str):
            ls = open(rule_file, 'r')
        else:
            ls = rule_file
        for line in ls:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            val = line.split();
            if len(val) < 3:
                continue

            self.rules.append((int(val[0]), float(val[1]), float(val[2])));






