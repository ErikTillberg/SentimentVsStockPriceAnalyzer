import json
import csv
#
file_name = "tsla"
string_to_add = ","
#
with open(file_name+'.json', 'r') as f:
    file_lines = f.readlines()
    for x in xrange(len(file_lines)):
        if x%1000==0:
            print x
        temp = json.loads(file_lines[x])
        temp['sentiment']['result']['confidence'] = float(temp['sentiment']['result']['confidence'])
        temp['timestamp_sec'] = int(int(temp['timestamp_ms'])/1000)
        del temp['timestamp_ms']
        file_lines[x] = json.dumps(temp)
    #
    for x in xrange(len(file_lines)-1):
        # don't apply to last line
        file_lines[x] = ''.join([file_lines[x].strip(), string_to_add, '\n'])
    #
#
with open(file_name+'.fixed.json', 'w') as f:
    f.writelines(['[\n'])
    f.writelines(file_lines)
    f.writelines([']\n'])
#
