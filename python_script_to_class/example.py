#!/usr/bin/python

'''
This is a test script.
'''

import sys

def say_something(text):
	something(text)

def something(text):
	print text

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "[?] Usage: %s <any text>" % sys.argv[0]
		exit(0)
	say_something(sys.argv[1])
	'''
	Test for when the script is transformed to a class
	ex = Example()
	ex.say_something("LOL")
	'''