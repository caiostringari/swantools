import datetime
from matplotlib.dates import num2date,date2num

def swantime2datetime(time,inverse=False):
	"""
		Translating Swans's time strings to datetimes and vice-versa.
		See datetime and num2date documentation for more information.
	"""

	fmt = "%Y%m%d.%H%M%S"

	dtime = []
	stime = []

	if inverse:
		for date in time:
			stime.append(datetime.datetime.strftime(num2date(date),fmt))
		return stime
	else:
		for date in time:
			dtime.append(date2num(datetime.datetime.strptime(date,fmt)))
		return dtime


def dir2cat(theta):
	""" Given a array of directions, will return the respective
	    categoreis (N,S,E,W, ect..). Credits to Eric Nardi.
	"""
	categories = ['N', 'NNE', 'NE', 'ENE',
	              'E', 'ESE', 'SE', 'SSE',
	              'S', 'SSW', 'SW', 'WSW',
	              'W', 'WNW', 'NW', 'NNW']
	# print theta
	interval = 360.0/len(categories)
	idx      = np.floor((theta+interval/2)%360/interval)
	cat      = []
	for i in idx: cat.append(categories[int(i)])
	return cat


def deg2uv(direction,intensity=False):
	"""
	Givean an array of directions will return the U and V
	components. intensity is optional.
	"""
	rad = -4.0*np.arctan(1.0)/180.
	if intensity:
		u   = intensity*np.sin(direction*rad)
		v   = intensity*np.cos(direction*rad)
	else:
		u   = np.sin(direction*rad)
		v   = np.cos(direction*rad)
	return u,v
