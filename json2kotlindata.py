#!/usr/bin/python3
import requests, sys
if len(sys.argv) is not 4:
	print("usage: json2kotlindata.py <path to json file> <class name> <package>")
	print("to save result to file, add ` >> filename.kt ` after command")
	exit()

with open(sys.argv[1], 'r') as content:
	jsonBody = content.read()
payload = {
	'schema'                 : jsonBody,
	'targetpackage'          : sys.argv[3],
	'classname'              : sys.argv[2], 
	'sourcetype'             : 'json',
	'annotationstyle'        : 'gson',
	'propertyworddelimiters' : '- _'
}

r = requests.post("http://www.jsonschema2pojo.org/generator/preview", data = payload)
responseText = r.text
parsedText = []
for line in responseText.splitlines():
	if "class" in line:
		line = line.replace("public", "data")
		line = line.replace("{", "(")
	if line == '}':
		parsedText[len(parsedText) - 2] = parsedText[len(parsedText) - 2].replace(',', '')
		line = ')'
	if ';' in line and not "import" in line and not "package" in line:
		elements = line.split(" ")
		varName = elements[len(elements) - 1].replace(';', '')
		varType = elements[len(elements) - 2]
		line = "    var " + varName + " : " + varType + ','
	parsedText.append(line)
result = ""
for line in parsedText:
	result += line + '\n'
print(result)
