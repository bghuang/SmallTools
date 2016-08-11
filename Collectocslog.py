#!/usr/bin/python
#-*-coding: utf-8 -*-
import re
import os
import time
import sys
import getopt
import logging
import os.path
import glob

debuglogpath = '/sn/log/'
debuglogpatten = '/sn/log/debuglog*'

today_date = time.strftime('%Y-%m-%d',time.localtime())

debugfile = '/sn/log/debuglog13'
start_date = today_date
start_time = '01:21:00'

end_date = today_date
end_time = '02:28:60'

contentList = []
print_flag = False

# This is a work one, we just try use another way to implementated it

def usage():
    print 'Usage: collectocslog [OPTION]... [START TIME] [END TIME]'
    print "Command to collect debug log from start time to end time, ouput file name is debug_output.txt in working direcotry"
    print
    print 'Mandatory arguments to long options are mandatory for short options too.'
    print '    [START TIME], [END TIME] format is Hh:Mn'
    print "Example:"
    print '    collectocslog 07:01 08:01'

'''

def compare(x,y):
    stat_x = os.stat(x)
    stat_y = os.stat(y)
    if stat_x.st_mtime < stat_y.st_mtime:
        return -1
    elif stat_x.st_mtime > stat_y.st_mtime:
        return 1
    else:
        return 0
'''
def compare(x, y):
    mtime_x = os.path.getmtime(x)
    mtime_y = os.path.getmtime(y)
    if mtime_x < mtime_y:
        return -1
    elif mtime_x > mtime_y:
        return 1
    else:
        return 0

def version():
    print "collectocslog (BG utils) 0.2"
    print "Copyright (C) 2016 Free Software Foundation, Inc."
    print "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>."
    print "This is a internal test software. There is NO RESPONSE for run this command"
    print "There is NO WARRANTY, to the extent permitted by law."
    print
    print "Written by Baogui Huang."

argv = sys.argv

try:
    opts,args = getopt.getopt(argv[1:], 'hv', ['help', 'version'])
except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)
for op,value in opts:
    if op in ('-v','--version'):
       version()
       sys.exit()


#print len(args)
if len(args) >= 2:
    if args[0] > args[1]:
        args[0],args[1] = args[1],args[0]
    start_time = args[0]
    end_time = args[1]
else:
    usage()
    sys.exit(2)


debugfilelist = glob.glob(debuglogpatten)

print "Log Duration:"
print "    Date:       ", today_date
print "    Start_time: ", start_time
print "    End_time:   ", end_time
print "Log Analyse start    at", time.asctime(time.localtime())

debugfilelist.sort(compare)

#print debugfilelist

patten = re.compile(r'^\s{3}\+{3}\s\S+\s(\S+)\s(\S+).+\s$')

for debugfile in debugfilelist:
#    print 'Open',debugfile

#Here we can use another way:
#with open(debugfile, 'r') as f:
#    for line in f:
#        ......

    with open(debugfile, 'r') as f:
        lines = f.readlines()
    for line in lines:
        m = patten.match(line)
        if m:
            m_date = m.group(1)
            m_time = m.group(2)
            if (m_time >= start_time and m_time < end_time):
                print_flag = True
            elif m_time > end_time:
                print_flag = False
#                print "Break"
                break
            else:
                print_flag = False
#        print "each line"
        if print_flag:
            contentList.append(line)
#            print "Add List"

#print contentList
with open('debug_output.txt','wb') as f:
    for i in contentList:
        f.write(i)

print "Log Analyse complete at", time.asctime(time.localtime())