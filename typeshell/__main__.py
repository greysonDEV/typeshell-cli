import sys
from os import system
import argparse
from typeshell.testmanager.TestManager import TestManager
from typeshell.ValidateSession import ValidateSession
import pytyper

def main():
	parser = argparse.ArgumentParser(description='Practice your typing speed.')
	parser.add_argument('-c', '--create', help='create a typing session', action=ValidateSession, metavar=('COUNT', 'TYPE'), nargs=2)
	parser.add_argument('-V', '--version', help="show program version", action='version', version='%(prog)s 0.1.0')
	parser.add_argument('-v', '--verbose', help='increase ouput verbosity', action='store_true')

	args = parser.parse_args()
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(0)

	if args.create:
		print("creation")
		prepare_session(args.create[0], args.create[1])
		proceed = input()
		system('clear')
		begin_session(args.create[0], args.create[1], args.verbose)

def prepare_session(prompt_count, prompt_type):
	system('clear')
	print('*-------[Generating session]-------*')
	lines = ['Prompts:', str(prompt_count), 'Type:', prompt_type]
	for line in lines:
		print(line.center(36))
	print('*------[Press enter to begin]------*\n')
   
def begin_session(prompt_count, prompt_type, is_verbose):
	tmgr = TestManager()
	tmgr.begin_test(prompt_count, prompt_type)
	output(tmgr.averages, tmgr.stats, is_verbose)

def output(average_stats, stats, is_verbose):
	system('clear')
	print('*-------[Finished session]-------*')
	print('Average statistics:\n')
	keys = {'Gross-WPM':'gross_wpm', 'Net-WPM':'net_wpm','Accuracy':'accuracy','Errors':'errors', 'Time':'seconds'}
	longest_key = max(list(keys.keys()), key=len)
	"""
	Using match_length (pytyper) to eliminate possible output offset due to character differences in the keys
	"""
	for key in keys:
		print(f'{pytyper.match_length(key, longest_key)[0]}: {average_stats[keys[key]]}')
	print('*----------------------------------*\n')
	if is_verbose:
		for stat in stats:
			prompt = stat[0]
			user_input = stat[1]
			print(f'> {prompt}')
			print(f'$ {user_input}')
			"""
			Using conflict_str (pytyper) to point to characters that were typed incorrectly
			"""
			conflict_str = pytyper.conflict_str(prompt, user_input)
			if conflict_str != '':
				print(f'  {conflict_str}')