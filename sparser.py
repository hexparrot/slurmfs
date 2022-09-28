__author__ = "William Dizon"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "William Dizon"
__email__ = "wdchromium@gmail.com"
__status__ = "Development"

import re
import time

class SlurmJob(object):
    def __init__(self, data_dict):
        self.attr = data_dict

    def __str__(self):
        a = self.attr
        t = "%Y-%m-%dT%H:%M:%S"
        d = "%H:%M:%S"
        return f"""JobId={a['JobId']} JobName={a['JobName']} UserId={a['UserId']} Uid={a['Uid']} """ \
        f"""GroupId={a['GroupId']} Gid={a['Gid']} MCS_label={a['MCS_label']} Priority={a['Priority']} """ \
        f"""Nice={a['Nice']} Account={a['Account']} QOS={a['QOS']} JobState={a['JobState']} """ \
        f"""Reason={a['Reason']} Dependency={a['Dependency']} Requeue={a['Requeue']} """ \
        f"""Restarts={a['Restarts']} BatchFlag={a['BatchFlag']} Reboot={a['Reboot']} """ \
        f"""ExitCode={a['ExitCode']} RunTime={time.strftime(d,a['RunTime'])} """ \
        f"""TimeLimit={time.strftime(d,a['TimeLimit'])} TimeMin={a['TimeMin']} """ \
        f"""SubmitTime={time.strftime(t,a['SubmitTime'])} EligibleTime={time.strftime(t,a['EligibleTime'])} """ \
        f"""AccrueTime={time.strftime(t,a['AccrueTime'])} StartTime={time.strftime(t,a['StartTime'])} """ \
        f"""EndTime={time.strftime(t,a['EndTime'])} Deadline={a['Deadline']} """ \
        f"""PreemptEligibleTime={time.strftime(t,a['PreemptEligibleTime'])} PreemptTime={a['PreemptTime']} """ \
        f"""SuspendTime={a['SuspendTime']} SecsPreSuspend={a['SecsPreSuspend']} """ \
        f"""LastSchedEval={time.strftime(t,a['LastSchedEval'])} Scheduler={a['Scheduler']} """ \
        f"""Partition={a['Partition']} AllocNode:Sid={a['AllocNode:Sid']} """ \
        f"""ReqNodeList={a['ReqNodeList']} ExcNodeList={a['ExcNodeList']} NodeList={a['NodeList']} """ \
        f"""BatchHost={a['BatchHost']} NumNodes={a['NumNodes']} NumCPUs={a['NumCPUs']} """ \
        f"""NumTasks={a['NumTasks']} CPUs/Task={a['CPUs/Task']} ReqB:S:C:T={a['ReqB:S:C:T']} """ \
        f"""TRES={a['TRES']} Socks/Node={a['Socks/Node']} NtasksPerN:B:S:C={a['NtasksPerN:B:S:C']} """ \
        f"""CoreSpec={a['CoreSpec']} MinCPUsNode={a['MinCPUsNode']} MinMemoryCPU={a['MinMemoryCPU']} """ \
        f"""MinTmpDiskNode={a['MinTmpDiskNode']} Features={a['Features']} DelayBoot={time.strftime(d,a['DelayBoot'])} """ \
        f"""OverSubscribe={a['OverSubscribe']} Contiguous={a['Contiguous']} Licenses={a['Licenses']} """ \
        f"""Network={a['Network']} Command={a['Command']} WorkDir={a['WorkDir']} StdErr={a['StdErr']} """ \
        f"""StdIn={a['StdIn']} StdOut={a['StdOut']} Power={a['Power']}"""

    @classmethod
    def scontrol_parse(cls, fn):
        with open(fn, 'r') as scout:
            text = scout.read()
            if text.startswith("JobId"):
                return cls.parse_sc_job(text)
            elif text.startswith("PartitionName"):
                return cls.parse_sc_partition(text)
            elif text.startswith("NodeName"):
                return cls.parse_sc_node(text)
            elif text.startswith("ACCOUNT"):
                return cls.parse_sq(text)
            else:
                raise NotImplementedError

    @classmethod
    def parse_sc_job(cls, text):
        attr = {}
        regex = re.compile(r'([^\ \=]+)\=(.*)')

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
    def parse_sc_partition(cls, text):
        attr = {}
        regex = re.compile(r'([^\ \=]+)\=(.*)')

        for line in text.split(" "):
            hits = regex.match(line)
            try:
                attr[hits[1]] = hits[2]
            except TypeError as e:
                pass #nonetype hits[1] matches

        return cls.clean_datatypes(attr)

    @classmethod
    def parse_sc_node(cls, text):
        attr = {}
        regex = re.compile(r'([a-zA-Z_]+)=([^ \ ]*)')
        os_regex = re.compile(r'OS=(.+?) +[A-Za-z]+=')

        matches = re.findall(regex,text.rstrip('\n'))

        for k,v in matches:
            attr[k] = v

        match = re.findall(os_regex, text)[0]
        attr["OS"] = match

        return cls.clean_datatypes(attr)

    @classmethod
    def parse_sq(cls, text):
        header_line, item_line = text.split()
        header = header_line.split("|")
        items = item_line.split("|")

        #pop off last item, seen as ('WORK_DIR\n', '/home/wdizon\n')
        p1 = header.pop().rstrip()
        p2 = items.pop().rstrip()

        #readd after newline removal
        header.append(p1)
        items.append(p2)

        return cls.clean_datatypes(dict(zip(header,items)))

    @staticmethod
    def clean_datatypes(attrs):
        TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
        DURATION_FORMAT = "%H:%M:%S"
        for k in attrs:
            try:
                attrs[k] = int(attrs[k])
            except ValueError: #non int() castable
                try:
                    attrs[k] = float(attrs[k])
                except ValueError: #string not float castable, treat as string and reduce
                    if attrs[k] in ('N/A', 'n/a', 'n/s', 'None', 'NONE', '(null)', ''):
                        attrs[k] = None
                    elif attrs[k] in ('NO'):
                        attrs[k] = False
                    elif ':' in attrs[k]:
                        if '-' in attrs[k]:
                            try:
                                attrs[k] = time.strptime(attrs[k], TIME_FORMAT)
                            except ValueError: #if not a timestring
                                pass
                        else:
                            try:
                                attrs[k] = time.strptime(attrs[k], DURATION_FORMAT)
                            except ValueError: #if not a timestring
                                pass

        return attrs

