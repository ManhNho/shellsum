#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import hashlib
from prettytable import PrettyTable

def get_banner():
	'''
	This function be used to print "Shellsum" banner
	'''
	print '''                                                                                
         _      _ _                     
 ___  __| |___ | | |___ _   _  ___ __ _ 
|__ \/ _` / _ \| | |__ | | | |/ _ ' _` |
/ __| | | \__  | | / __| |_| | | | | | |
\___|_| |_|___/|_|_\___|_.__/|_| |_| |_|
                                          
    Shellsum.py - Author: ManhNho
    A defense tool - detect web shells in local system via md5sum
    Usage:
    	python shellsum.py
    	Input website directory > /var/www/html/
	'''

def check_dir(target):
	'''
	Use check_dir function to check input directories >> os.path.isdir() return True or False
	'''
	if os.path.isdir(target):
		pass
	else:
		print "Please recheck input directory!"
		sys.exit(0)

def generate_md5sum(filename):
    '''This function generates an md5 hash for a given file.'''
    return hashlib.md5(open(filename, "rb").read()).hexdigest()

def get_origin_hashes(target):
	'''Listing all files in directory with os.walk() and then calc md5sum of each file'''
	origin_hashes = {}
	for cwd, lod, lof in os.walk(target):
		for file in lof:
			file_path = os.path.join(cwd, file)
			file_hash = generate_md5sum(file_path)
			origin_hashes[file_hash] = file_path
	return origin_hashes

def compare_hashes(origin_hashes, shell_hashes):
	'''Compare generated values with shell hashes'''
	result = set(origin_hashes.keys()) & set(shell_hashes.keys())
	if result == set([]):
		print "="*63
		print "[+] Congratulation, not detect any web shells in 'sauces' code."
		print "="*63
	else:
		print "="*15
		print "[+] Found shell!"
		print "="*15
		table = PrettyTable(['ID', 'Original file', 'Shell reference file', 'md5sum'])
		for i in range(0, len(result)):
			detected_hash = result.pop()
			table.add_row([i+1, origin_hashes[detected_hash], shell_hashes[detected_hash], detected_hash])
		print table

def main():
	get_banner()
	target = raw_input("Input website directory > ")
	check_dir(target) 
	origin_hashes = get_origin_hashes(target)
	try:
		shell_hashes = eval(open("database.data").read())
	except Exception as e:
		raise e
	compare_hashes(origin_hashes, shell_hashes)

if __name__ == '__main__':
	main()