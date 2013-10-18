#!/usr/bin/env python
"""script ec2run.py
   Written as a class
   uses argparse.ArgumentParser to create options list
   and usage messages then parse argv and
   return object as dictionary
"""

import sys
import argparse
import os
import re

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


class Main(object):

  def __init__(self, argv=None):
    ''' Initializer
    '''
    
    self._argv = argv
    
    self.AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', None)
    self.AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY', None)
    assert self.AWS_ACCESS_KEY is not None, "Env Var AWS_ACCESS_KEY not set"
    assert self.AWS_SECRET_KEY is not None, "Env Var AWS_SECRET_KEY not set"

    
  def parse_args(self):
    """Return object from argparse.ArgumentParser.parse_args()
       Returning Dictionary
    """
    if self._argv == None:
      fargv = [ ]
    else:
      fargv = self._argv[1:]   #have to strip out argv0, the name of program
    
    parser = argparse.ArgumentParser(description='Python wrapper for ec2run')
  
    group = parser.add_mutually_exclusive_group()

    parser.add_argument("-r", "--region", help="ec2 region", choices=[ 'us-east-1',
      'eu-west-1', 'us-west-2', 'us-west-1' ], default='us-east-1')

    parser.add_argument("-z", "--availability-zone",
      help="ec2 availability zone", required=True)

    parser.add_argument("-a", "--ami", help="AMI name", required=True)

    group.add_argument("-d", "--user-data", help="User data string")
    
    group.add_argument("-f", "--user-data-file",
      help="Read user data from file", type=file)
    
    parser.add_argument("-g", "--group", help="Ec2 Security group name/id",
      nargs='+', default='default')

    parser.add_argument("-k", "--key", help="Ec2 Keypair name", required=True)

    parser.add_argument("-t", "--instance-type", help="Ec2 Instance Type",
      default="t1.micro")

    parser.add_argument("-n", "--instance-count",
      help="Maximum instances to launch", type=int)

    parser.add_argument("-v", "--verbose", help="Verbose output",
      action="store_true")


    return parser.parse_args(fargv).__dict__
#    return vars(parser.parse_args(self._argv[1:]))

  def myConn(self, region):
    Driver = None
    if region == 'us-west-1':
      Driver = get_driver(Provider.EC2_US_WEST)
    elif region == 'us-west-2':
      Driver = get_driver(Provider.EC2_US_WEST_OREGON)
    elif region == 'eu-west-1':
      Driver = get_driver(Provider.EC2_EU_WEST)
    else:
      Driver = get_driver(Provider.EC2_US_EAST)
    
    return Driver(self.AWS_ACCESS_KEY, self.AWS_SECRET_KEY)
    

  def isValid_avail(self, conn, avail):
    
    if avail != None or '':
      azones = conn.ex_list_availability_zones()
      p = re.compile(avail)

      for zone in azones:
        if p.search(str(zone)) != None:
          return True

    return False
    
    
  def isValid_keypair(self, conn, key):
  
    if key != None or '':
      kps = conn.ex_describe_all_keypairs()
      p = re.compile(key)

      for keyp in kps:
        if p.search(str(keyp)) != None:
          return True

    return False
    
    
  def isValid_group(self, conn, group):
    
    if group != None or '':
      groups = conn.ex_list_security_groups()
    
      for pp in group:
        p = re.compile(str(pp))

        for grp in groups:
          if p.search(str(grp)) != None:
            return True

    return False
    
    
  def isValid_ami(self, conn, ami):
  # Need to change this code to a try except where we pass the ami list
  # to the list_images fn,
  #  amis = conn.list_images(None, ami)
    if ami != None or []:
      amis = conn.list_images()
      str_ami = 'id=' + ami + ','
      p = re.compile(str_ami)
    
      for image in amis:
        if p.search(str(image)) != None:
          return True

    return False      
    

def main(argv=None):
  """Main function
  """

  myMain = Main(argv)
  
  myargs = myMain.parse_args()
  
  myconn = myMain.myConn(myargs['region'])
  
  
  
  if myMain.isValid_avail(myconn, myargs['availability_zone']):
    print mything + " is available in " + myargs['region']
  else:
    if myargs['availability_zone'] != None:
      print mything + " is not available in " + myargs['region']
    else:
      print "--availability_zone value was None"
  
  '''
  if myargs['availability_zone'] != None:
    if myMain.isValid_avail(myconn, myargs['availability_zone']):
      print myargs['availability_zone'] + " is available in " + myargs['region']
    else:
      print myargs['availability_zone'] + " is not available in " + myargs['region']
  '''
    
  if myargs['key'] != None:
    if myMain.isValid_keypair(myconn, myargs['key']):
      print myargs['key'] + " is available in " + myargs['region']
    else:
      print myargs['key'] + " is not available in " + myargs['region']
  
  if myargs['group'] != None:
    print "One of these Security groups:"
    print myargs['group']
    if myMain.isValid_group(myconn, myargs['group']):
      print "available in " + myargs['region']
    else:
      print "not available in " + myargs['region']    

  if myargs['ami'] != None:
    if myMain.isValid_ami(myconn, myargs['ami']):
      print myargs['ami'] + " is available in " + myargs['region']
    else:
      print myargs['ami'] + " is not available in " + myargs['region']
  
  
#  print type(myargs)
'''  
  for key in myargs.keys():
    print key + ": "  + str(myargs[key])
'''

if __name__  == '__main__':
  main(sys.argv)
