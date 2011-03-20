from Registry import Register
import Yahoo2
from utilities import iterModule
		
#simple heuristic for now, could do it manually later.
for m_name,m_obj in [(name.lstrip("get"),obj) for (name,obj) in iterModule(Yahoo2) if callable(obj) and 'get' in name]:
	Register("".join(["Daily",m_name]),m_obj)
	
Register("DailyPricesDates",Yahoo2.getDates)
#Register("DailyFundamentalsDates",Yahoo2.getDates)