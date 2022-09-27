__author__ = "William Dizon"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "William Dizon"
__email__ = "wdchromium@gmail.com"
__status__ = "Development"

import re

class SlurmJob(object):
    def __init__(self, data_dict):
        self.attr = data_dict

    def __str__(self):
        a = self.attr
        return f"""JobId={a['JobId']} JobName={a['JobName']} UserId={a['UserId']} Uid={a['Uid']} """ \
        f"""GroupId={a['GroupId']} Gid={a['Gid']} MCS_label={a['MCS_label']} Priority={a['Priority']} """ \
        f"""Nice={a['Nice']} Account={a['Account']} QOS={a['QOS']} JobState={a['JobState']} """ \
        f"""Reason={a['Reason']} Dependency={a['Dependency']} Requeue={a['Requeue']} """ \
        f"""Restarts={a['Restarts']} BatchFlag={a['BatchFlag']} Reboot={a['Reboot']} """ \
        f"""ExitCode={a['ExitCode']} RunTime={a['RunTime']} TimeLimit={a['TimeLimit']} """ \
        f"""TimeMin={a['TimeMin']} SubmitTime={a['SubmitTime']} EligibleTime={a['EligibleTime']} """ \
        f"""AccrueTime={a['AccrueTime']} StartTime={a['StartTime']} EndTime={a['EndTime']} """ \
        f"""Deadline={a['Deadline']} PreemptEligibleTime={a['PreemptEligibleTime']} """ \
        f"""PreemptTime={a['PreemptTime']} SuspendTime={a['SuspendTime']} """ \
        f"""SecsPreSuspend={a['SecsPreSuspend']} LastSchedEval={a['LastSchedEval']} """ \
        f"""Scheduler={a['Scheduler']} Partition={a['Partition']} AllocNode:Sid={a['AllocNode:Sid']} """ \
        f"""ReqNodeList={a['ReqNodeList']} ExcNodeList={a['ExcNodeList']} NodeList={a['NodeList']} """ \
        f"""BatchHost={a['BatchHost']} NumNodes={a['NumNodes']} NumCPUs={a['NumCPUs']} """ \
        f"""NumTasks={a['NumTasks']} CPUs/Task={a['CPUs/Task']} ReqB:S:C:T={a['ReqB:S:C:T']} """ \
        f"""TRES={a['TRES']} Socks/Node={a['Socks/Node']} NtasksPerN:B:S:C={a['NtasksPerN:B:S:C']} """ \
        f"""CoreSpec={a['CoreSpec']} MinCPUsNode={a['MinCPUsNode']} MinMemoryCPU={a['MinMemoryCPU']} """ \
        f"""MinTmpDiskNode={a['MinTmpDiskNode']} Features={a['Features']} DelayBoot={a['DelayBoot']} """ \
        f"""OverSubscribe={a['OverSubscribe']} Contiguous={a['Contiguous']} Licenses={a['Licenses']} """ \
        f"""Network={a['Network']} Command={a['Command']} WorkDir={a['WorkDir']} StdErr={a['StdErr']} """ \
        f"""StdIn={a['StdIn']} StdOut={a['StdOut']} Power={a['Power']}"""

    @classmethod
    def parse_sc(cls, fn):
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
    def parse_sc_node(cls, fn):
        attr = {}
        regex = re.compile(r'([a-zA-Z_]+)=([^ \ ]*)')
        os_regex = re.compile(r'OS=(.+?) +[A-Za-z]+=')

        with open(fn, 'r') as scout:
            text = scout.readline()
            matches = re.findall(regex,text.rstrip('\n'))

            for k,v in matches:
                attr[k] = v

            match = re.findall(os_regex, text)[0]
            attr["OS"] = match

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
                try:
                    attrs[k] = float(attrs[k])
                except ValueError: #string not float castable, treat as string and reduce
                    if attrs[k] in ('N/A', 'n/a', 'n/s', 'None', '(null)', ''):
                        attrs[k] = None

        return attrs

