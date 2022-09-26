__author__ = "William Dizon"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "William Dizon"
__email__ = "wdchromium@gmail.com"
__status__ = "Development"

class SlurmJob(object):
    def __init__(self):
        self.attr = {}

    @classmethod
    def parse_sc(cls, fn):
        import re

        attr = {}
        regex = re.compile(r'([^\ \=]+)\=(.*)')

        with open(fn, 'r') as scout:
            text = scout.readline()

            for line in text.split(" "):
                hits = regex.match(line)
                try:
                    attr[hits[1]] = hits[2]
                except TypeError as e:
                    pass #nonetype hits[1] matches

        uid_elems = attr['UserId'].split("(")
        attr['UserId'] = uid_elems[0]
        attr['Uid'] = uid_elems[1][0:-1]

        uid_elems = attr['GroupId'].split("(")
        attr['GroupId'] = uid_elems[0]
        attr['Gid'] = uid_elems[1][0:-1]

        return cls.clean_datatypes(attr)

    @classmethod
    def parse_sq(cls, fn):
        with open(fn, 'r') as sqout:
            header = sqout.readline().split("|")
            items = sqout.readline().split("|")

            #pop off last item, seen as ('WORK_DIR\n', '/home/wdizon\n')
            p1 = header.pop().rstrip()
            p2 = items.pop().rstrip()

            #readd after newline removal
            header.append(p1)
            items.append(p2)

        return cls.clean_datatypes(dict(zip(header,items)))

    @staticmethod
    def clean_datatypes(attrs):
        for k in attrs:
            try:
                attrs[k] = int(attrs[k])
            except ValueError: #non int() castable
                pass

        for k in attrs:
            if attrs[k] in ('N/A', 'None', '(null)', ''):
                attrs[k] = None

        return attrs

