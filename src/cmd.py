import subprocess


def execcmd(cmd):

    sub = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=True,
                           text=True,
                           executable='/bin/bash')

    return sub.communicate()
