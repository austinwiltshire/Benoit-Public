from Registry import Register
from utilities import iterModule
import Google
		
#simple heuristic for now, could do it manually later.
for m_name,m_obj in [(name.lstrip("get"),obj) for (name,obj) in iterModule(Google) if callable(obj) and 'get' in name]:
	Register(m_name,m_obj)
#	if 'Annual' not in m_name and 'Quarterly' not in m_name:
#		print m_name
#	print m_name

