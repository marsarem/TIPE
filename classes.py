import numpy as np
import sys



class Point():
	"""Point représenté par 2 coordonnées"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.affichage = f"Point(x={self.x}, y={self.y})"

	def couple(self):
		return (self.x, self.y)

	def __str__(self):
		return self.affichage

	def __repr__(self):
		return self.affichage


class Vecteur():
	"""Vecteur représenté par ses coordonnées x, y et son point d'application"""
	def __init__(self, x, y, point_application):
		self.x = x
		self.y = y
		self.point_appli = point_application
		self.point_arrivee = self.calcul_point_arrivee()
		self.affichage = f"Vecteur(x={self.x}, y={self.y}, appli=Point(x={self.point_appli.x}, y={self.point_appli.y}))"
	
	def __str__(self):
		return self.affichage

	def __repr__(self):
		return self.affichage

	def calcul_norme(self):
		return np.sqrt(self.x**2 + self.y **2)

	def calcul_point_arrivee(self):
		arrivee_x = self.x + self.point_appli.x
		arrivee_y = self.y + self.point_appli.y
		return Point(arrivee_x, arrivee_y)


class Base():
	"""Base contenant 2 vecteurs"""
	def __init__(self, vect1, vect2):
		self.vect1 = vect1
		self.vect2 = vect2
		self.point_commun = vect1.point_appli
		self.affichage = f"Base(vect1={self.vect1}, vect2={self.vect2})"
	
	def __str__(self):
		return self.affichage

	def __repr__(self):
		return self.affichage



class Coordonnees():
	"""Coordonnées dans le ciel"""
	def __init__(self, ra, dec):
		self.ra = ra
		self.dec = dec
		self.string = f"{self.ra} {self.dec}"
		self.affichage = f"Coordonnees(ra={self.ra}, dec={self.dec})"

	def __str__(self):
		return self.affichage

	def __repr__(self):
		return self.affichage

	def convertir():
		pass


# class Pixel():
# 	def __init__(self, x, y):
# 		self.x = x
# 		self.y = y
# 		self.affichage = f"Pixel(x={self.x}, y={self.y})"

# 	def __str__(self):
# 		return self.affichage

# 	def __repr__(self):
# 		return self.affichage 
		


class Etoile():
	def __init__(self, coo_img, coo_reelles, ecart=None):
		self.coo_img = coo_img # de la classe Point
		self.coo_reelles = coo_reelles # de la classe Coordonnees
		self.ecart = ecart
		self.affichage = f"Etoile(coo_img={self.coo_img}, coo_reelles={self.coo_reelles}, ecart={self.ecart})"

	def __str__(self):
		return self.affichage

	def __repr__(self):
		return self.affichage




class ImageBase():
	"""Coordonnées dans le ciel"""
	"""{"image":"53Kalypso_843.JPG", "ra":"23:54:46.0842", "dec":"-5:43:01.180", "px_asteroide":(566, 512)}"""
	def __init__(self, chemin_image, ra, dec):
		self.chemin_image = chemin_image
		self.ra = ra
		self.dec = dec
		self.string = f"{self.ra} {self.dec}"

		self.affichage = f"ImageBase(chemin_image={self.chemin_image}, ra={self.ra}, dec={self.dec})"

	def __str__(self):
		return self.affichage

	def __repr__(self):
		return self.affichage


class ImageReference(ImageBase):
	def __init__(self, chemin_image, ra, dec, taille):
		super().__init__(chemin_image, ra, dec)
		self.taille = taille # En arcmin

		self.affichage = f"ImageReference(chemin_image={self.chemin_image}, ra={self.ra}, dec={self.dec}, \
taille={self.taille})"


class ImageAsteroide(ImageBase):
	def __init__(self, chemin_image, ra, dec, px_asteroide):
		super().__init__(chemin_image, ra, dec)
		self.px_asteroide = Point(px_asteroide[0], px_asteroide[1])

		self.affichage = f"ImageAsteroide(chemin_image={self.chemin_image}, ra={self.ra}, dec={self.dec}, \
px_asteroide={self.px_asteroide})"


def calcul_produit_scalaire(vect1, vect2):
	prod_scal = vect1.x*vect2.x + vect1.y*vect2.y
	return prod_scal


def calcul_angle(vect1, vect2):
	prod_scal = calcul_produit_scalaire(vect1, vect2)
	norme_vect1 = vect1.calcul_norme()
	norme_vect2 = vect2.calcul_norme()
	return np.arccos(prod_scal/(norme_vect1*norme_vect2))
