class CRC:
	
	def __init__(self):
		self.cdw = ''

	def xor(self,a,b):
		result = []
		for i in range(1,len(b)):
			if a[i] == b[i]:
				result.append('0')
			else:
				result.append('1')


		return  ''.join(result)

	def crc(self,message, key):
		pick = len(key)

		tmp = message[:pick]
		while pick < len(message):
			if tmp[0] == '1':
				tmp = self.xor(key,tmp)+message[pick]
			else:
				tmp = self.xor('0'*pick,tmp) + message[pick]

			pick+=1
   
		if tmp[0] == "1":
			tmp = self.xor(key,tmp)
		else:
			tmp = self.xor('0'*pick,tmp)

		checkword = tmp
		return checkword

	def encodedData(self,data,key):
		l_key = len(key)
		append_data = data + '0'*(l_key-1)
		remainder = self.crc(append_data,key)
		codeword = data+remainder
		self.cdw += codeword
		print("Remainder: " ,remainder)
		print("Data: " ,codeword)

	def reciverSide(self,data,key):
		r = self.crc(data,key)
		size = len(key)-1
		if r == size*'0':
			print("No Error")
		else:
			print("Error")
   
	def concat_bin(self, data):
		result = ''
		for pick in data:
			binary_p = format(pick, 'b')
			if(len(binary_p)<8):
				binary_p = '0'*(8-len(binary_p))+binary_p
			result += binary_p
		return result

data = [0x01, 0x00, 0x43, 0x46, 0x57, 0x31, 0x30, 0x30, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x76, 0x34, 0x2E, 0x32, 0x30, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x00, 0x00, 0x00]
key = '1010000000000001'
c = CRC()
data = c.concat_bin(data)
c.encodedData(data, key)
c.reciverSide(c.cdw, key)