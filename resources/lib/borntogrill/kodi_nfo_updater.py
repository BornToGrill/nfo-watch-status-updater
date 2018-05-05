# -*- coding: utf-8 -*-

from datetime import datetime
from xml.dom import minidom
from xml.dom.minidom import Node
from xml.etree import ElementTree
from contextlib import closing
import re

import xbmcvfs # pylint: disable=import-error

ENCODING = 'UTF-8'
PLAYCOUNT_TAG = 'playcount'
LAST_PLAYED_TAG = 'lastplayed'

IO_ERROR_ENOENT = (2, 'No such file or directory')

def _format_datetime(date):
	return date.strftime('%Y-%m-%d %H:%M:%S')

def _remove_blanks(node):
    for x in node.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            if x.nodeValue:
                x.nodeValue = x.nodeValue.strip()
        elif x.nodeType == Node.ELEMENT_NODE:
            _remove_blanks(x)

def _to_pretty_xml(node, indent='\t', newl='\n', encoding=None):
	node_string = ElementTree.tostring(node, encoding=encoding)
	reparsed = minidom.parseString(node_string)
	_remove_blanks(reparsed)
	pretty_bytes = reparsed.toprettyxml(indent=indent, newl=newl, encoding=encoding)
	pretty_string = pretty_bytes.decode(encoding)

	excessive_newline_fix = re.compile(r'((?<=>)(\n[\t]*)(?=[^<\t]))|(?<=[^>\t])(\n[\t]*)(?=<)')
	fixed_pretty_string = re.sub(excessive_newline_fix, '', pretty_string)
	return fixed_pretty_string

def update_nfo(path, playcount, last_played=None):
	if last_played is None:
		last_played = datetime.now()

	if not xbmcvfs.exists(path):
		(error_code, error_message) = IO_ERROR_ENOENT
		raise IOError('File does not exist', path, error_code, error_message)

	file = xbmcvfs.File(path)
	with closing(file):
		nfo_content = file.read()

	parser = ElementTree.XMLParser(encoding=ENCODING)
	tree_element = ElementTree.fromstring(nfo_content, parser=parser)
	tree = ElementTree.ElementTree(tree_element)

	root = tree.getroot()
	playcount_element = tree.find(PLAYCOUNT_TAG)
	last_played_element = tree.find(LAST_PLAYED_TAG)

	if playcount > 0:
		if playcount_element is None:
			playcount_element = ElementTree.SubElement(root, PLAYCOUNT_TAG)
		if last_played_element is None:
			last_played_element = ElementTree.SubElement(root, LAST_PLAYED_TAG)
		playcount_element.text = str(playcount)
		last_played_element.text = _format_datetime(last_played)
	else:
		root.remove(playcount_element)
		root.remove(last_played_element)

	# TODO: Config. if 'pretty xml' setting is enabled. Use to_pretty_xml. Otherwise use simple ElementTree.tostring() for peformance
	pretty_xml_string = _to_pretty_xml(root, encoding=ENCODING)
	
	file = xbmcvfs.File(path, 'w')
	with closing(file):
		encoded = pretty_xml_string.encode(ENCODING)
		file.write(encoded)
