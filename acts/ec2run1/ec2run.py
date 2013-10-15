#!/usr/bin/env python
"""script ec2run.py
   Written as a class
   uses argparse.ArgumentParser to create options list
   and usage messages then parse argv and
   return object as dictionary
"""

import sys
import argparse


class Main(object):

  def __init__(self, argv=None):
    ''' Initializer
    '''
    
    self._argv = argv

  def parse_args(self):
    """Return object from argparse.ArgumentParser.parse_args()
       Returning Dictionary
    """
    
    parser = argparse.ArgumentParser(description='Python wrapper for ec2run')
  
    group = parser.add_mutually_exclusive_group()

    parser.add_argument("-r", "--region", help="ec2 region")

    parser.add_argument("-z", "--availability-zone",
      help="ec2 availability zone")

    parser.add_argument("-a", "--ami", help="AMI name")

    group.add_argument("-d", "--user-data", help="User data string")

    # Remember to remove this and use the following for type file
    group.add_argument("-f", "--user-data-file",
      help="Read user data from file")
    
    '''Following is commented out for now, to avoid checking of type file  
    group.add_argument("-f", "--user-data-file",
      help="Read user data from file", type=file)
    '''
    
    parser.add_argument("-g", "--group", help="Ec2 Security group name/id",
      nargs='+')

    parser.add_argument("-k", "--key", help="Ec2 Keypair name")

    parser.add_argument("-t", "--instance-type", help="Ec2 Instance Type",
      default="t1.micro")

    parser.add_argument("-n", "--instance-count",
      help="Maximum instances to launch", type=int)

    parser.add_argument("-v", "--verbose", help="Verbose output",
      action="store_true")


    return parser.parse_args(self._argv[1:]).__dict__ #had to strip out argv0, the name of program
#    return vars(parser.parse_args(self._argv[1:]))

def main(argv=None):
  """Main function
  """

  myargs = Main(argv).parse_args()
  
#  print type(myargs)
  
  for key in myargs.keys():
    print key + ": "  + str(myargs[key])

if __name__  == '__main__':
  main(sys.argv)
