#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sys import argv
from tqdm import tqdm
from io import BytesIO

FONT_SIZE=12
FONT_NAME='comic_sans_ms.ttf'

LETTER_WIDTH=13
LETTER_HEIGHT=18

FONT_CACHE={}
TABLE_CACHE={}

class converter:
	_temp=""
	_data="""\
<html>
<body>
<style>
body {
	display: inline-block;
	}
table {
	display: inline-block;
	margin: 0px;
	padding: 0px;
	border-spacing: 0px;
}
tr {
	margin: 0px;
	padding: 0px;
}
td {
	width: 1px;
	height: 1px;
	margin: 0px;
	padding: 0px;
}

</style>
<div style="display: inline">
"""		

	def __init__(self):
		with open(argv[1],'r') as file:
			self._input_data=file.read()

		self._font=ImageFont.truetype(FONT_NAME, FONT_SIZE)

		self._output_file='data.html'
		self._convert()
		self._save()



	def cod(self,col):
		return f"""<td style="background:{col}"></td>"""


	def col(self,r,g,b):
		return '#%02x%02x%02x' % (r, g, b)

	def _letter_to_bitmap(self, letter):
		if letter in FONT_CACHE:
			return FONT_CACHE[letter]
		else:	
			img=Image.new(
				'RGB',
				(LETTER_WIDTH, LETTER_HEIGHT),
				(255,255,255)
				)

			draw=ImageDraw.Draw(img)
			draw.text(
				(0,0),
				letter,
				font=self._font,
				fill=(0,0,0)
				)
			bitmap=np.array(img)
			FONT_CACHE[letter]=bitmap
			return bitmap

	def _convert(self):
		for letter in tqdm(self._input_data):
			if letter.isprintable():
				if letter not in TABLE_CACHE:
					bitmap=self._letter_to_bitmap(letter)
					table=self._convert_character(bitmap)
					TABLE_CACHE[letter]=table
					self._data+=table
				else:
					self._data+=TABLE_CACHE[letter]
			elif letter=="\n":
				print('new line')
				self._data+="<br>"

	def _convert_character(self, bitmap):
		self._temp="""<table>"""
		for x in range(0,LETTER_HEIGHT, 1):
			self._temp+="<tr>"
			for y in range(0,LETTER_WIDTH, 1):
				self._temp+=self.cod(self.col(bitmap[x][y][0],bitmap[x][y][1],bitmap[x][y][2]))
			self._temp+="</tr>"
		self._temp+="</table>"
		return self._temp

	def _save(self):
		with open(self._output_file,'w') as f:
			f.write(self._data)
			f.close()



if __name__=="__main__":
		c=converter()

