
import re
import struct

pattern1 = re.compile("[0-9<>xsbB?ehHfiIlLqQd]*")
pattern2 = re.compile("[<>]{2,}")
pattern3 = re.compile("^[^<>]+|[<>][^<>]+")

class HexParser():
	STEP_INIT = 0
	STEP_HEADER = 1
	STEP_FORMAT = 2
	# FORMAT_LEN_DICT = {'<': 0, '>': 0, 'x': 1, 's': 1, 'b': 1, 'B': 1, '?': 1,'e': 2, 'h': 2,
	# 					'H': 2, 'f': 4, 'i': 4, 'I': 4, 'l': 4, 'L': 4,'q': 8, 'Q': 8, 'd': 8}

	def __init__(self):
		self.header = None
		self.header_len = 0
		self.header_idx = 0
		self.format_lst = []
		self.format_data_len = 0
		self.data_buf = []
		self.data_buf_len = 0
		self.step = self.STEP_INIT

	def setHeader(self, header):
		self.header = header
		self.header_len = len(header)
	
	# @staticmethod
	def isFormatValid(self, frmt):
		if pattern1.fullmatch(frmt) == None:
			return False
		if len(pattern2.findall(frmt)) > 0:
			return False
		return True

	def splitParseFmt(self, frmt):
		return pattern3.findall(frmt)

	def setFormat(self, frmt):
		if not self.isFormatValid(frmt):
			return False

		self.format_lst = self.splitParseFmt(frmt)
		print(self.format_lst)
		self.format_data_len = [struct.calcsize(f) for f in self.format_lst]
		print(self.format_data_len)

	def data_in(self, data):
		in_len = len(data)
		if self.step == self.STEP_INIT:
			data_idx = [i for i in range(len(data)) if data[i] == self.header[0]]
			
			for di in data_idx:
				data_part = data[di:di+self.header_len]
				match_len = self.match_header(data_part)
				if match_len == self.header_len:
					self.step = self.STEP_FORMAT
					break
				elif match_len != 0 and in_len <= di+self.header_len:
					self.step = self.STEP_HEADER
					self.header_idx = match_len
					break
		elif self.step == self.STEP_HEADER:
			data_part = data[0:self.header_len]
			match_len = self.match_header(data_part, self.header_idx)
			if match_len == self.header_len - self.header_idx:
				self.step = self.STEP_FORMAT
			elif match_len != 0 and in_len <= self.header_len - self.header_idx:
				self.header_idx = self.header_idx + match_len
		elif self.step == self.STEP_FORMAT:
			if (in_len + self.data_buf_len - self.header_len) < self.format_data_len:
				self.data_buf.append(data)
				self.data_buf_len = self.data_buf_len + in_len
			else:
				for frmt in self.format_lst:
					struct.unpack()

	def match_header(self, data, header_offset = 0):
		l = min(len(data), len(self.header_len - header_offset))
		if l == 0:
			return 0
		for i in range(l):
			fmt_byte = self.formatLst[i + header_offset]
			if fmt_byte != 'x':
				if data[i] != fmt_byte:
					return 0
		return l


