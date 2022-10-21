from astroquery.vizier import Vizier # pip install --pre astroquery
import astropy.coordinates as coord
import astropy.units as u

from classes import *


def recup_coo_etoiles_vizier(coo_centre_image):
	# Renvoie : [{'ra': 358.583614, 'dec': -5.832439}, ...]
	# http://simbad.u-strasbg.fr/simbad/sim-coo?Coord=23+54+46+-05+43+00+&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&CooDefinedFrames=none&Radius=15&Radius.unit=arcmin&submit=submit+query&CoordList=
	# https://astroquery.readthedocs.io/en/latest/vizier/vizier.html
	v = Vizier(column_filters={"Rmag":"<17"})

	try:
		result = v.query_region(coord.SkyCoord(coo_centre_image, unit=(u.hourangle, u.deg)
			, frame='icrs'), 
			width="15m", catalog=["USNO-A2.0"])
	except Exception as e:
		print(e)
		sys.exit(0)

	coo_etoiles = []
	for i in result["I/252/out"]:
		coo_etoiles.append(Coordonnees(ra=i["RAJ2000"], dec=i["DEJ2000"]))

	return coo_etoiles


def convertir_coo(coo):
	ra, dec = coo.ra, coo.dec
	coo_reelles_asteroide = coord.SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))

	ra, dec = coo_reelles_asteroide.ra.to_string(), coo_reelles_asteroide.dec.to_string()
	return Coordonnees(ra=ra, dec=dec)



if __name__ == '__main__':
	coo_centre_image = "23:54:50 -05:43:00"
	print(recup_coo_etoiles_vizier(coo_centre_image))