import re

def getTitle(title, section, text):
	regex1 = r"\=\=(.*?)\=\="
	header = re.search(regex1, newText)
	title.append(header.group(1))
	return title

