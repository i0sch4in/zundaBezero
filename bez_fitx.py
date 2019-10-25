#!/usr/bin/env python3

import socket, sys, os
import szasar

#SERVER = 'localhost'
#PORT = 6012

#ez aldatu
class Menua:
	Fold, Batt, Prop, Dump, Exit = range( 1, 6 )
	Options = ( "Eguzki plakak zabaldu/tolestu", "Bateriaren karga maila", "Pultsatzaile bat martxan jarri", "Sentsoreen neurketak", "Amaiatu")

	def menua():
		print( "+{}+".format( '-' * 38 ) )
		for i,option in enumerate( Menua.Options, 1 ):
			print( "| {}.- {:<33}|".format( i, option ) )
		print( "+{}+".format( '-' * 38 ) )

		while True:
			try:
				selected = int( input( "Egin zure aukera: " ) )
			except:
				print( "Aukera okerra, saiatu berriro." )
				continue
			if 0 < selected <= len( Menua.Options ):
				return selected
			else:
				print( "Aukera okerra, saiatu berriro." )

#aldatu (ibon)
def iserror(message):
	if( message.startswith( "ER" ) ):
		code = message[2:]
		if(code=="01"):
			msg="Komando ezezaguna."
		elif(code=="02"):
			msg="Espero ez zen parametroa. Parametro bat jaso da espero ez zen tokian."
		elif(code=="03"):
			msg="Hautazkoa ez den parametro bat falta da."
		elif(code=="04"):
			msg="Parametroak ez du formatu egokia."
		elif(code=="05"):
			msg="Segurtasun kode okerra."
		elif(code=="11"):
			msg="Eguzki-plakak zabaldu edo tolestu eragiketa egitea ezinezkoa da."
		elif(code=="12"):
			msg="Plakak zabaltzea eskatu da eta zabalduta daude jada"
		elif(code=="21"):
			msg="Ezinezkoa da karga maila eskuratzea erantzuna negatiboa delako"
		elif(code=="31"):
			msg="Ezin zara propultsorearekin hasi, erantzuna negatiboa ematen du"
		elif(code=="41"):
			msg="Propultsorearekin hasi zara eta ezin zaio eutsi adierazitako iraupenean."
	else:
		print("Errore ezezaguna.")
		return False
	print("Errorea: " + msg)
	return True


if __name__ == "__main__":
	if len( sys.argv ) != 3:
		print( "Erabilera: {} [<zerbitzaria> <portua>]".format( sys.argv[0] ) )
		exit( 2 )

	if len( sys.argv ) >= 2:
		SERVER = sys.argv[1]
	if len( sys.argv ) == 3:
		PORT = int( sys.argv[2])

	print(" Zerbitzaria: {}, Portua: {} ".format(SERVER, PORT))
	s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
	zerb_helb = (SERVER, PORT)
	"""NO FUNCSIONA"""
	# mezua="konexioa hasi"
	# s.sendto(mezua.encode(), zerb_helb )
	# saiakerak = 0
	# """ Zerbitzariak ez badu bidalitako mezuarekin erantzuten (5 saiakeretan),
	# 	komunikazioa etengo da.
	# """
	# buf, beste_helb = s.recvfrom(1024)
	# while(buf.decode() != mezua and saiakerak<5):
	# 	s.sendto(mezua.encode(), zerb_helb )
	# 	buf, beste_helb = s.recvfrom(1024)
	# 	saiakerak+=1
	# if(saiakerak>=5):
	# 	print("Ez da zerbitzaria lokalizatu")
	# 	s.close()
	# 	exit(1)
	# s.connect(beste_helb)

	s.sendto(b"", zerb_helb)
	buf, beste_helb = s.recvfrom(1024)
	s.connect(beste_helb)

	while True:
		option = Menua.menua()
		key = input("Sartu segurtasun-kodea:")
		if option == Menua.Fold:
			param = input("Plakak zabaldu edo tolestu nahi dituzu? [0=zabaldu, 1=tolestu]")
			while(param not in ["0","1"]):
				print("Balioa ez da zuzena. Saiatu berriro.")
				param = input("Plakak zabaldu edo tolestu nahi dituzu? [0=zabaldu, 1=tolestu]")
			message = key + szasar.Command.Fold + param
			s.send(message.encode("ascii"))
		# elif option == Menua.Batt:
		#
		#
		# elif option == Menua.Prop:
		#
		#
		# elif option == Menua.Dump:
		#
		#
		# elif option == Menua.Exit:
		# 	s.close()
		# 	exit(0)
	s.close()
