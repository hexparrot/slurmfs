__author__ = "William Dizon"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "William Dizon"
__email__ = "wdchromium@gmail.com"
__status__ = "Development"

class sparser(object):
    def parse_sc(self):
        self.attr = {}

        import re
        with open('assets/scontrol.out', 'r') as scout:

            regex = re.compile(r'([^\ \=]+)\=(.*)')
            text = scout.readline()

            for line in text.split(" "):
                hits = regex.match(line)
                try:
                    self.attr[hits[1]] = hits[2]
                except TypeError as e:
                    pass #nonetype hits[1] matches

            uid_elems = self.attr['UserId'].split("(")
            self.attr['UserId'] = uid_elems[0]
            self.attr['Uid'] = uid_elems[1][0:-1]

            uid_elems = self.attr['GroupId'].split("(")
            self.attr['GroupId'] = uid_elems[0]
            self.attr['Gid'] = uid_elems[1][0:-1]

            for k in self.attr:
                try:
                    self.attr[k] = int(self.attr[k])
                except ValueError: #non int() castable
                    pass

            for k in self.attr:
                if self.attr[k] in ('N/A', 'None', '(null)', ''):
                    self.attr[k] = None

    def parse_sq(self):
        with open('assets/sq_1401154', 'r') as sqout:
            header = sqout.readline().split("|")
            items = sqout.readline().split("|")

            #pop off last item, seen as ('WORK_DIR\n', '/home/wdizon\n')
            p1 = header.pop().rstrip()
            p2 = items.pop().rstrip()

            #readd after newline removal
            header.append(p1)
            items.append(p2)

            self.attr = dict(zip(header,items))

            for k in self.attr:
                try:
                    self.attr[k] = int(self.attr[k])
                except ValueError: #non int() castable
                    pass

            for k in self.attr:
                if self.attr[k] in ('N/A', 'None', '(null)', ''):
                    self.attr[k] = None

