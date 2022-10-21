from PIL import Image
import cv2
import numpy as np
import math
import sys
import random

from classes import *
from vizier import *
from traitement_image import *



def main():

	img_reference = ImageReference(chemin_image="kalypso_ref.png", ra="23:54:50", dec="-05:43:00", taille=15)

	liste_images = [
	ImageAsteroide(chemin_image="Kalypso_843.JPG", ra="23:54:46.0842", dec="-5:43:01.180", px_asteroide=(566, 512)),
	ImageAsteroide(chemin_image="Kalypso_846.JPG", ra="23:54:45.8881", dec="-5:43:02.876", px_asteroide=(566, 512))
	]

	for img_asteroide in liste_images:
		print("-------")
		print(img_asteroide.chemin_image, img_asteroide.ra, img_asteroide.dec)

		centres_img_aste = detection_centre_etoiles(img_asteroide.chemin_image)
		centres_img_ref = detection_centre_etoiles(img_reference.chemin_image)

		bases_img_aste = creer_bases(centres_img_aste)
		bases_img_ref = creer_bases(centres_img_ref)

		paires_bases = bases_qui_matchent(bases_img_aste, bases_img_ref) # [[base_img_aste1, base_img_ref1],...]
		
		# enregistre_paires_bases(paires_bases, img_asteroide.chemin_image, img_reference.chemin_image)

		paire_base = paires_bases[0]


		centres_etoiles_img_ref = [paire_base[1].point_commun, paire_base[1].vect1.point_arrivee, 
			paire_base[1].vect2.point_arrivee]


		centres_etoiles_img_aste = [paire_base[0].point_commun, paire_base[0].vect1.point_arrivee, 
			paire_base[0].vect2.point_arrivee]

		position_etoile_img_ref = lie_position_etoile(centres_etoiles_img_ref,
			recup_coo_etoiles_vizier((img_reference.string))
			,img_reference)
		

		# On ne récupère que 2 étoiles
		position_etoile_img_ref = position_etoile_img_ref[:2]


		position_etoile_img_aste = []
		for i in range(len(position_etoile_img_ref)):
			coo_img = position_etoile_img_ref[i].coo_img
			coo_reelles = position_etoile_img_ref[i].coo_reelles

			index_etoile = centres_etoiles_img_ref.index(coo_img)

			position_etoile_img_aste.append(Etoile(coo_img=centres_etoiles_img_aste[index_etoile], 
				coo_reelles=coo_reelles))


		px_asteroide_img_aste = identifie_asteroide(centres_img_aste, img_asteroide.px_asteroide)


		"""
		On calcule combien fait 1 pixel en ra et en dec
		On on calcule la position de l'astéroide avec 1 des 2 étoiles
		"""
		etoile1, etoile2 = position_etoile_img_aste[:2]

		etoile1_ra, etoile1_dec = etoile1.coo_reelles.ra, etoile1.coo_reelles.dec
		etoile2_ra, etoile2_dec = etoile2.coo_reelles.ra, etoile2.coo_reelles.dec

		etoile1_x, etoile1_y = etoile1.coo_img.x, etoile1.coo_img.y
		etoile2_x, etoile2_y = etoile2.coo_img.x, etoile2.coo_img.y

		distance_etoiles_1_2 = ( ((etoile1_x - etoile2_x))**2 + ((etoile1_y - etoile2_y))**2 )**(1/2)


		# Taille 1 pixel :
		pixel_x = (etoile2_ra - etoile1_ra) / (etoile2_x - etoile1_x) # 1 pixel = X ra
		pixel_y = (etoile2_dec - etoile1_dec) / (etoile2_y - etoile1_y)

		xa, ya = px_asteroide_img_aste.x, px_asteroide_img_aste.y
		distance_x = xa - etoile1_x
		distance_y = ya - etoile1_y


		coo_reelles_asteroide = str(distance_x*pixel_x + etoile1_ra) + " " + str(distance_y*pixel_y + etoile1_dec)


		coo_reelles_asteroide = coord.SkyCoord(coo_reelles_asteroide, unit=(u.deg, u.deg))
		# print(coo_reelles_asteroide)

		ra, dec = coo_reelles_asteroide.ra.to_string(unit=u.hourangle), coo_reelles_asteroide.dec.to_string(unit=u.deg)
		print(ra, dec)



if __name__ == '__main__':
	main()