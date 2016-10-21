class Rules():
    def __init__(self, rule_file):
        self.rules = []
        self.index = []
        if isinstance(rule_file, str):
            try:
              ls = open(rule_file, 'r')
            except Exception as e:
              return
        else:
            ls = rule_file
        for line in ls:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            val = line.split();
            if len(val) < 4:
                continue
            self.index.append(int(val[0]))

            self.rules.append((int(val[0]), int(val[1]), float(val[2]), float(val[3])));

    def calc_minutes(self, index, left, type, cut):
        time = 0
        if index == 0:
            time = 60 * (left / self.rules[0][type])
            if type == 2 and time == 0:
                time = 60
        elif index == 1:
          if cut:
            time = 60 * (self.rules[0][1] / self.rules[0][type])
            if type == 2:
              time += 10
          else:
            time = 60 * (self.rules[0][1] / self.rules[0][type] +\
                    left / self.rules[1][type])
        elif index == 2:
          if cut:
            time = 60 * (self.rules[0][1] / self.rules[0][type] + \
                    self.rules[1][1] / self.rules[1][type]);
          else:
            time = 60 * (self.rules[0][1] / self.rules[0][type] + \
                    self.rules[1][1] / self.rules[1][type] + \
                    left / self.rules[2][type])

        elif index == 3:
          if cut:
            time = 60 * (self.rules[0][1] / self.rules[0][type] + \
                    self.rules[1][1] / self.rules[1][type] + \
                    self.rules[2][1] / self.rules[2][type]) ;
            if type == 2:
              time += 20
          else:
            time = 60 * (self.rules[0][1] / self.rules[0][type] + \
                    self.rules[1][1] / self.rules[1][type] + \
                    self.rules[2][1] / self.rules[2][type] + \
                    left / self.rules[3][type])

        elif index == 4:
          if cut:
            time = 60 * (self.rules[0][1] / self.rules[0][type] + \
                    self.rules[1][1] / self.rules[1][type] + \
                    self.rules[2][1] / self.rules[2][type] + \
                    self.rules[3][1] / self.rules[3][type]);
          else:
            time = 60 * (self.rules[0][1] / self.rules[0][type] + \
                    self.rules[1][1] / self.rules[1][type] + \
                    self.rules[2][1] / self.rules[2][type] + \
                    self.rules[3][1] / self.rules[3][type] + \
                    left / self.rules[4][type])
        elif index == 5:
          time = 60 * (self.rules[0][1] / self.rules[0][type] + \
                self.rules[1][1] / self.rules[1][type] + \
                self.rules[2][1] / self.rules[2][type] + \
                self.rules[3][1] / self.rules[3][type] + \
                self.rules[4][1] / self.rules[4][type]);
        return time

    def calc_time(self, distance, dis_control):
      if distance > dis_control * 1.1:
        return (0,0)
      left = distance
      calc_args = {}

      index = 0
      left = distance
      for r in self.rules:
        if distance >= r[0]:
          index += 1
          left = distance - r[0]

      open_minutes = self.calc_minutes(index, left, 3, dis_control <= distance)
      close_minutes = self.calc_minutes(index, left, 2, dis_control <= distance)

      return (int(round(open_minutes)), int(round(close_minutes)))


