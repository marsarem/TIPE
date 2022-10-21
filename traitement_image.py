from PIL import Image
import cv2
import numpy as np
import math
import sys
import random

from classes import *
from vizier import *


def detection_centre_etoiles(chemin_img):
	"""
	Détecte le centre des points sur l'image
	"""
	centres_etoiles = []
	image = cv2.imread(chemin_img)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	edged = cv2.Canny(gray, 30, 200) # Canny edges
	# Contours : https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html
	contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	aires, perimetres = [], []
	for contour in contours:
		aire = cv2.contourArea(contour)
		aires.append(aire)

		peri = cv2.arcLength(contour,True)
		perimetres.append(peri)

		if aire > 20 and peri < 100:
			M = cv2.moments(contour)
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])

			centres_etoiles.append(Point(cx, cy))
			# cv2.circle(image, (cx, cy), 20, (174, 97, 255), 2) # Trace le centre
			# cv2.circle(image, (cx, cy), 1, (0, 0, 255), 5)

	# cv2.imshow('Contours', image)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()


	return centres_etoiles


def enregistre_paires_bases(paires_bases, chemin_img_aste, chemin_img_ref):
	couleurs = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(len(paires_bases*2))]

	for i in range(len(paires_bases)):
		image_aste = cv2.imread(chemin_img_aste)
		image_ref = cv2.imread(chemin_img_ref)
		l = [image_aste, image_ref]
		for j in range(2):
			vecteur1 = paires_bases[i][j].vect1
			vecteur2 = paires_bases[i][j].vect2

			cv2.line(l[j], vecteur1.point_appli.couple(), vecteur1.point_arrivee.couple(), couleurs[i], 5)

			cv2.line(l[j], vecteur2.point_appli.couple(), vecteur2.point_arrivee.couple(), couleurs[2*i+1], 5)

			print("test/" + str(i) + "_" + str(j) +".png")
			cv2.imwrite("test/" + str(i) + "_" + str(j) +".png", l[j])

	# print(emplacement + "test/bases/" + str(k) +".png")

def creer_bases(centres_etoiles):
	"""Créé toutes les bases possibles en choisissant 3 points à partir de la liste des centres des étoiles"""
	bases = []

	for i in range(len(centres_etoiles)):
		for j in range(i+1, len(centres_etoiles)):
			for k in range(j+1, len(centres_etoiles)):
				point1 = centres_etoiles[i]
				point2 = centres_etoiles[j]
				point3 = centres_etoiles[k]

				x = point2.x - point1.x
				y = point2.y - point1.y
				vect1 = Vecteur(x, y, point_application=point1)

				x = point3.x - point1.x
				y = point3.y - point1.y
				vect2 = Vecteur(x, y, point_application=point1)

				bases.append(Base(vect1, vect2))

	return bases



def bases_qui_matchent(bases_img_aste, bases_img_ref):
	paires_de_bases = []  # Liste de bases qui fonctionnent : [[Base1, Base2], [...] ...]


	# Arrêt lorsque nb_max paires de bases qui fonctionnent ont été trouvées. 
	# Mettre len(bases_img_aste)*len(bases_img_ref) pour qu'il y ait de limite
	nb_max = len(bases_img_aste)*len(bases_img_ref)
	nb_max = 2000

	i = 0
	while i < len(bases_img_aste) and len(paires_de_bases) < nb_max:
		base_img_aste = bases_img_aste[i]

		vect1_img_aste = base_img_aste.vect1 
		vect2_img_aste = base_img_aste.vect2
		prod_scal_img_aste = calcul_produit_scalaire(vect1_img_aste, vect2_img_aste)
		angle_img_aste = calcul_angle(vect1_img_aste, vect2_img_aste)

		j = 0
		while j < len(bases_img_ref) and len(paires_de_bases) < nb_max:
			base_img_ref = bases_img_ref[j]

			vect1_img_ref = base_img_ref.vect1
			vect2_img_ref = base_img_ref.vect2
			prod_scal_img_ref = calcul_produit_scalaire(vect1_img_ref, vect2_img_ref)
			angle_img_ref = calcul_angle(vect1_img_ref, vect2_img_ref)

			coeff_vect_1 = vect1_img_aste.calcul_norme() / vect1_img_ref.calcul_norme() 
			coeff_vect_2 = vect2_img_aste.calcul_norme() / vect2_img_ref.calcul_norme() 

			if abs(angle_img_aste - angle_img_ref) < 0.01 and abs(coeff_vect_2 - coeff_vect_1) < 0.01:
				paires_de_bases.append([base_img_aste, base_img_ref])
			j += 1
		i += 1

	return paires_de_bases



def lie_position_etoile(centre_etoiles_img_ref, position_etoiles, img_reference):
	# centre_etoiles_img_ref : px des étoiles de l'image ref
	# position_etoiles : recup_coo_etoiles_vizier()

	coo_centre_image_ref = img_reference.string
	taille_image_ref = img_reference.taille

	etoiles = []
	centre_img = coord.SkyCoord(coo_centre_image_ref, unit=(u.hourangle, u.deg))

	centre_ra = float(centre_img.ra.to_string(decimal=True))
	centre_dec = float(centre_img.dec.to_string(decimal=True))


	img_ref = Image.open(img_reference.chemin_image)

	taille_x, taille_y = img_ref.size

	centre_x, centre_y = taille_x / 2, taille_y / 2

	# Calcul taille 1 pixel
	pixel_x = (taille_image_ref/60) / taille_x # 1 pixel = X ra
	pixel_y = (taille_image_ref/60) / taille_y


	
	etoiles_trouvees = []
	ecarts = []
	for centre_etoile in centre_etoiles_img_ref:
		x, y = centre_etoile.x, centre_etoile.y
		distance_au_centre_x = centre_x - x 
		distance_au_centre_y = centre_y - y

		position_etoile_calculee_ra = (distance_au_centre_x * pixel_x) + centre_ra
		position_etoile_calculee_dec = (distance_au_centre_y * pixel_y) + centre_dec

		mini = position_etoiles[0]
		for position_reelle in position_etoiles:
			ra, dec = position_reelle.ra, position_reelle.dec
			ecart_mini = abs(position_etoile_calculee_ra - mini.ra) + abs(position_etoile_calculee_dec - mini.dec)
			ecart = abs(position_etoile_calculee_ra - ra) + abs(position_etoile_calculee_dec - dec)
			if ecart < ecart_mini:
			# if  abs(position_etoile_calculee_ra - ra) < abs(position_etoile_calculee_ra - mini.ra) and\
			#     abs(position_etoile_calculee_dec - dec) < abs(position_etoile_calculee_dec - mini.dec):
				mini = position_reelle

		ecart_mini = abs(position_etoile_calculee_ra - mini.ra) + abs(position_etoile_calculee_dec - mini.dec)

		ecarts.append([abs(position_etoile_calculee_ra - mini.ra), abs(position_etoile_calculee_dec - mini.dec)])
		etoiles_trouvees.append(Etoile(coo_img=centre_etoile, coo_reelles=mini, ecart=ecart_mini))
		position_etoiles.remove(mini)

	
	etoiles_trouvees.sort(key=lambda etoile: etoile.ecart)
	return etoiles_trouvees


def identifie_asteroide(centres_etoiles_img_aste, px_asteroide_img_aste):
	# L'astéroide est le point le plus proche des pixels approximatifs (obtenus sur gimp) 
	px_x, px_y = px_asteroide_img_aste.x, px_asteroide_img_aste.y
	mini = centres_etoiles_img_aste[0]
	mini_ecart = abs(centres_etoiles_img_aste[0].x - px_x) + abs(centres_etoiles_img_aste[0].y - px_y)
	for centre_etoile in centres_etoiles_img_aste:
		x, y = centre_etoile.x, centre_etoile.y
		ecart = abs(px_x - x) + abs(px_y - y)
		if ecart < mini_ecart:
			mini = centre_etoile
			mini_ecart = ecart

	return mini



if __name__ == '__main__':
	liste = [Point(1, 2), Point(2, 4), Point(3, 7), Point(4, 9), Point(7,18)]
	print(len(creer_bases(liste)))
