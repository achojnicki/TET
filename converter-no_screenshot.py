#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sys import argv
from tqdm import tqdm
from random import randint

FONT_SIZE=50
FONT_NAME='comic_sans_bold_ms.ttf'

LETTER_WIDTH=45
LETTER_HEIGHT=70

CACHE={}

class converter:
	_data="""\
<html>
<body>
<style>
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
<div>
"""

	def __init__(self):
		with open(argv[1],'r') as file:
			self._input_data=file.read()

		self._font=ImageFont.truetype(FONT_NAME, FONT_SIZE)


		self._output_file='data.html'
		self._convert()
		self._save()



	def cod(self, cls):
		return f"""<td class="{cls}"></td>"""

	def col(self,r,g,b):
		return '#%02x%02x%02x' % (r, g, b)

	def cod_bgc(self, col):
		return f"""<td style="background-color: {col}"></td>"""

	def _letter_to_bitmap(self, letter):
		if letter in CACHE:
			return CACHE[letter]
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
			CACHE[letter]=bitmap
			return bitmap

	def _convert(self):
		for letter in self._input_data:
			if letter.isprintable():
				bitmap=self._letter_to_bitmap(letter)
				self._convert_character(bitmap)
			elif letter=="\n":
				self._data+="<br>"
		self._data+="</div>"

	def _convert_character(self, bitmap):
		self._data+="""<table background="https://s3.gifyu.com/images/bSsZ9.gif">"""
		for x in tqdm(range(0,LETTER_HEIGHT, 1)):
			self._data+="<tr>"
			for y in range(0,LETTER_WIDTH, 1):
				if bitmap[x][y][0]<20 and bitmap[x][y][1]<20 and bitmap[x][y][2]<20:	
					self._data+=self.cod("")
				else:
					r=randint(0,255)
					self._data+=self.cod_bgc(self.col(r,r,r))
			self._data+="</tr>"
		self._data+="</table>"

	def _save(self):
		with open(self._output_file,'w') as f:
			f.write(self._data)
			f.close()



if __name__=="__main__":
		c=converter()

