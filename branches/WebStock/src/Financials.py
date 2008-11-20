import Annual
import Quarter
from utilities import Lazy

class FinancialPeriod(object):
	def __init__(self, policy, *args, **kwargs):
		self.policy = policy
		self.args = args
		self.kwargs = kwargs
	
	@Lazy
	def Quarter(self):
		return self.FinancialsForPeriod(Quarter)

	@Lazy
	def Annual(self):
		return self.FinancialsForPeriod(Annual)
	
	def FinancialsForPeriod(self, period):
		return Financials(period, self.policy, *self.args, **self.kwargs)

	@classmethod
	def Meta(cls, *args, **kwargs):
		class policy(object):
				@staticmethod
				def resolveClass(cls):
					return cls.Meta
	
				@staticmethod
				def construct(cls, *args, **kwargs):
					return cls(*args, **kwargs)
			
		
		return cls(policy, *args, **kwargs)
	
	@classmethod
	def Normal(cls, *args, **kwargs):	
		class policy(object):
			@staticmethod
			def resolveClass(cls):
				return cls
	
			@staticmethod
			def construct(cls, *args, **kwargs):
				return cls.fetch(*args, **kwargs)
		
		return cls(policy, *args, **kwargs)
	
class Financials(object):
	def __init__(self, module, policy, *args, **kwargs):
		self.policy = policy
		self.args = args
		self.kwargs = kwargs
		self.module = module
	
	@Lazy
	def BalanceSheet(self):
		return self.SECDocument("BalanceSheet")
	
	@Lazy
	def IncomeStatement(self):
		return self.SECDocument("IncomeStatement")
	
	@Lazy
	def CashFlowStatement(self):
		return self.SECDocument("CashFlowStatement")
	
	def SECDocument(self, document):
		resolvedClass = self.policy.resolveClass(self.module)
		innerClass = getattr(resolvedClass, document)
		return self.policy.construct(innerClass, *self.args, **self.kwargs)