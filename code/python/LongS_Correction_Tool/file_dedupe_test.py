import hashlib
import os

#1
cwd = os.getcwd()
output_file_path = "C:\\Users\\tuf74833\\Desktop\\new_results.txt"
input_file_path = "C:\\Users\\tuf74833\\Desktop\\test_pairs_removed_dicts_output_leading.txt"

#2
completed_lines_hash = set()

#3
output_file = open(output_file_path, "w")

#4
for line in open(input_file_path, "w"):
	#5
	hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
	#6
	if hashValue not in completed_lines_hash:
		output_file.write(line)
		completed_lines_hash.add(hashValue)
#7
output_file.close()