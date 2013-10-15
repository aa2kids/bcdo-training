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

  '''   Something wrong here with handling of None
  def test_parse_argsNone(self):
    argv = [ self, None ]
    myobj = ec2run.Main(argv)
    self.assertDictEqual(myobj.parse_args(), self.mydict)
  '''
  
  def test_parse_argsEmpty(self):
    argv = [ self ]
    myobj = ec2run.Main(argv)
    self.assertDictEqual(myobj.parse_args(), self.mydict)

  
  def test_parse_argsOptions(self):
    argv = [ self, '-n', '3', '-v', '-r', 'west' ]
    myobj = ec2run.Main(argv)
    self.mydict['verbose']= True
    self.mydict['region'] = 'west'
    self.mydict['instance_count'] = int(3)
    self.assertDictEqual(myobj.parse_args(), self.mydict)
  

if __name__ == '__main__':
  unittest.main()
    
