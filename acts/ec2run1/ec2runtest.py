#!/usr/bin/env python

import unittest
import ec2run

class E2crunTestCase(unittest.TestCase):
  def setUp(self):
    self.mydict = { "ami":None, "group":None, "verbose":False, "availability_zone":None,
               "region":None, "user_data":None, "instance_count":None,
               "instance_type":"t1.micro", "key":None, "user_data_file":None }
               

  def tearDown(self):
    self.mydict = None
    pass

  
  def test_parse_argsNone(self):
    argv = None
    myobj = ec2run.Main(argv)
    self.assertDictEqual(myobj.parse_args(), self.mydict)

  
  def test_parse_argsEmpty(self):
    argv = [ self ]
    myobj = ec2run.Main(argv)
    self.assertDictEqual(myobj.parse_args(), self.mydict)

  
  def test_parse_argsOptions(self):       # positive test all settable options
    argv = [ self, '-n', '3', '-v', '--region', 'west', '-z', 'any-available',
             '--user-data', 'some user data', '-t', 'instance type', '--ami',
             'image', '-g', 'group1', 'group2', '--key', 'some key' ]
    myobj = ec2run.Main(argv)
    self.mydict['verbose']= True
    self.mydict['region'] = 'west'
    self.mydict['instance_count'] = int(3)
    self.mydict['user_data'] = 'some user data'
    self.mydict['instance_type'] = 'instance type'
    self.mydict['key'] = 'some key'
    self.mydict['group'] = [ 'group1', 'group2' ]
    self.mydict['ami'] = 'image'
    self.mydict['availability_zone'] = 'any-available'
    self.assertDictEqual(myobj.parse_args(), self.mydict)
    
# error case -> non-number for -n option
# but argparse does an exit on error instead of raising Exception
# so, I ?????
  '''
  def test_parse_argsNoNumberInstanceCont(self):
    argv = [ self, '-n', 'not a number' ]
    myobj = ec2run.Main(argv)
    self.assertDictEqual(myobj.parse_args(), self.mydict)
  '''

# error case -> assign both -d and -f exclusive options

# error case -> when -f option check for file, give it something not a file

# error case -> call an option but don't give it anything
  

if __name__ == '__main__':
  unittest.main()
    
