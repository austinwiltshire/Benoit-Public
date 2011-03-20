import logging
import Gmail

class EmailLogger(object):
	
	def __init__(self,subject=None):
		self.buffer = []
		self.subject = subject
	
	def write(self, str):
		self.buffer.append(str)
		
	def flush(self):
		pass
	
	def finalize(self):
		message = "".join(self.buffer)
		Gmail.sendMail(message,self.subject,_from="Project Buffet Logger")
		
#	def AddTo(self, logger):
#		logger.addHandler(logging.StreamHandler(self))

#### SCRIPT ###
