from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time, sys, os, errno

def check_path(filename):
	if not os.path.exists(os.path.dirname(filename)):
		try:
			if len(filename.split("/")) >= 2:
				os.makedirs(os.path.dirname(filename))
			else:
				open(filename, 'a').close()
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

def read_file(filename):
	check_path(filename)
	with open(filename,'r+',newline='') as file_info:
		raw_text = file_info.read()
	return raw_text

def get_html_file(url, file_path=None):
	options = Options()
	options.add_argument("--headless")
	browser=webdriver.Firefox(options=options)
	browser.get(url)
	html_text = browser.page_source
	time.sleep(0.5)
	browser.close()

	html_text = html_text.splitlines()
	if file_path == None:
		pass
	else:
		check_path(file_path)
		with open(file_path,'w+',newline='') as html_file:
			for line in html_text:
				html_file.write(line)
				html_file.write("\n")
	return html_text

def find_number_elements(text, element, complement = ''):
	if complement != '':
		complement = ' '+complement
	search_term = "<"+element+complement+">"
	ocor = 0
	while(text.find(search_term) != -1):
		text = text[text.find(search_term)+len(search_term):]
		ocor += 1
	return ocor

def get_html_element(text, element, complement = '', ini = 0):
	if complement != '':
		complement = ' '+complement
	open_tag = "<"+element+complement+">"	
	open_pos = text.find(open_tag, ini)+len(open_tag)
	search_pos = open_pos
	depth = 1
	while(depth > 0):
		search_pos = text.find("<", search_pos)+1
		if text[search_pos] == "/":
			depth -=1
		elif text[search_pos:search_pos+3] == "img":
			pass
		else:
			depth +=1
	return text[open_pos:search_pos-1]

def get_all_html_elements(text, element, complement = ''):
	element_array = []
	ini = 0
	n_element = find_number_elements(text, element, complement)
	for i in range(n_element):
		element_array.append(get_html_element(text, element, complement, ini))
		ini = text.find(element_array[i])+len(element_array[i])
	return element_array

def get_element_complement(text, element, complement, ini = 0):
	search_element = "<" + element + " "
	ini_pos = ini
	while True:
		ini_element_pos = text.find(search_element, ini_pos)
		if ini_element_pos == -1:
			return "no " + element +" with " + complement + " complement found"
		end_element_pos = text.find(">", ini_element_pos)
		ini_complement_pos = text.find(complement, ini_element_pos, end_element_pos)
		if ini_complement_pos == -1:
			ini_pos = end_element_pos
		else:
			ini_return = text.find('"', ini_complement_pos)
			end_return = text.find('"', ini_return+1)
			return text[ini_return+1:end_return]
