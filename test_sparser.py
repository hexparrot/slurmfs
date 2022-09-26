#!/usr/bin/env python3
__author__ = "William Dizon"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "William Dizon"
__email__ = "wdchromium@gmail.com"
__status__ = "Development"

import unittest
from sparser import sparser

class TestSlurmParser(unittest.TestCase):
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_scontrol_splitting(self):
        sc = sparser()

        checks = {
            'JobId': 1337,
            'JobName': '_interactive',
            'UserId': 'hexparrot',
            'Uid': 4286,
            'GroupId': 'wheel',
            'Gid': 99,
            'MCS_label': None,
            'Priority': 999,
            'Nice': 0,
            'Account': 'wheel',
            'QOS': 'primary',
            'JobState': 'RUNNING',
            'Reason': None,
            'Dependency': None,
            'Requeue': 1,
            'Restarts': 0,
            'BatchFlag': 1,
            'Reboot': 0,
            'ExitCode': "0:0",
            'RunTime': "00:06:10",
            'RunTime': '00:06:10',
            'TimeLimit': '04:00:00',
            'TimeMin': None,
            'SubmitTime': '2022-09-24T10:48:20',
            'EligibleTime': '2022-09-24T10:48:20',
            'AccrueTime': '2022-09-24T10:48:20',
            'StartTime': '2022-09-24T10:48:20',
            'EndTime': '2022-09-24T14:48:20',
            'Deadline': None,
            'PreemptEligibleTime': '2022-09-24T11:03:20',
            'PreemptTime': None,
            'SuspendTime': None,
            'SecsPreSuspend': 0,
            'LastSchedEval': '2022-09-24T10:48:20',
            'Scheduler': 'Main',
            'Partition': 'general',
            'AllocNode:Sid': 'slurm01:2554234',
            'ReqNodeList': None,
            'ExcNodeList': None,
            'NodeList': 'c025',
            'BatchHost': 'c025',
            'NumNodes': 1,
            'NumCPUs': 1,
            'NumTasks': 1,
            'CPUs/Task': 1,
            'ReqB:S:C:T': '0:0:*:*',
            'TRES': 'cpu=1,mem=2G,node=1,billing=1',
            'Socks/Node': '*',
            'NtasksPerN:B:S:C': '0:0:*:*',
            'CoreSpec': '*',
            'MinCPUsNode': 1,
            'MinMemoryCPU': '2G',
            'MinTmpDiskNode': 0,
            'Features': 'public',
            'DelayBoot': '00:00:00',
            'OverSubscribe': 'OK',
            'Contiguous': 0,
            'Licenses': None,
            'Network': None,
            'Command': '/usr/local/bin/_interactive',
            'WorkDir': '/home/wdizon',
            'StdErr': '/dev/null',
            'StdIn': '/dev/null',
            'StdOut': '/dev/null',
            'Power': None,
        }

        for k in checks:
            self.assertEqual(sc.attr[k], checks[k])

    def test_squeue_parsing(self):
        sc = sparser()
        sc.parse_sq()

        checks = {
            'ACCOUNT': 'grp_rcadmins',
            'TRES_PER_NODE': None,
            'MIN_CPUS': 1,
            'MIN_TMP_DISK': 0,
            'END_TIME': '2022-09-26T11:11:01',
            'FEATURES': 'public',
            'GROUP': 99,
            'OVER_SUBSCRIBE': 'OK',
            'JOBID': 1401154,
            'NAME': '_interactive',
            'COMMENT': None,
            'TIME_LIMIT': '4:00:00',
            'MIN_MEMORY': '2G',
            'REQ_NODES': None,
            'COMMAND': '/usr/local/bin/_interactive',
            'PRIORITY': 99941,
            'QOS': 'public',
            'REASON': None,
            'ST': 'R',
            'USER': 'wdizon',
            'RESERVATION': None,
            'WCKEY': None,
            'EXC_NODES': None,
            'NICE': 0,
            'S:C:T': '*:*:*',
            'EXEC_HOST': 'c066',
            'CPUS': 1,
            'NODES': 1,
            'DEPENDENCY': None,
            'ARRAY_JOB_ID': 1401154,
            'SOCKETS_PER_NODE': '*',
            'CORES_PER_SOCKET': '*',
            'THREADS_PER_CORE': '*',
            'ARRAY_TASK_ID': None,
            'TIME_LEFT': '3:49:19',
            'TIME': '10:41',
            'NODELIST': 'c066',
            'CONTIGUOUS': 0,
            'PARTITION': 'general',
            'NODELIST(REASON)': 'c066',
            'START_TIME': '2022-09-26T07:11:01',
            'STATE': 'RUNNING',
            'UID': 4286,
            'SUBMIT_TIME': '2022-09-26T07:11:01',
            'LICENSES': None,
            'CORE_SPEC': None,
            'SCHEDNODES': None,
            'WORK_DIR': '/home/wdizon',
        }

        for k in checks:
            print(k)
            self.assertEqual(sc.attr[k], checks[k])

if __name__ == '__main__':
    unittest.main()
