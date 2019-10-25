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
	s.connect( (SERVER, PORT) )

	while True:
		option = Menua.menua()

		if option == Menua.Fold:
			message = "{}\r\n".format( szasar.Command.Fold )
			s.sendall( message.encode( "ascii" ) )
			message = szasar.recvline( s ).decode( "ascii" )
			if iserror( message ):
				continue
			filecount = 0
			print( "Zerbitzaritik jasotako fitxategi zerrenda" )
			print( "-----------------------------------------" )
			while True:
				line = szasar.recvline( s ).decode("ascii")
				if line:
					filecount += 1
					fileinfo = line.split( '?' )
					print( "{:<20} {:>8}".format( fileinfo[0], int2bytes( int(fileinfo[1]) ) ) )
				else:
					break
			print( "-------------------------------" )
			if filecount == 0:
				print( "Ez dago fitxategirik eskuragarri." )
			else:
				plurala = "{} fitxategi".format( filecount ) if filecount > 1 else "fitxategi bat"
				print( "Guztira {} eskuragarri.".format( plurala ) )

		elif option == Menua.Batt:
			filename = input( "Idatzi jaitsi nahi duzun fitxategiaren izena: " )
			message = "{}{}\r\n".format( szasar.Command. Batt, filename )
			s.sendall( message.encode( "ascii" ) )
			message = szasar.recvline( s ).decode ("ascii" )
			if iserror( message ):
				continue
			filesize = int( message[2:] )
			message = "{}\r\n".format( szasar.Command.Download2 )
			s.sendall( message.encode( "ascii" ) )
			message = szasar.recvline( s ).decode( "ascii" )
			if iserror( message ):
				continue
			filedata = szasar.recvall( s, filesize )
			try:
				with open( filename, "wb" ) as f:
					f.write( filedata )
			except:
				print( "Ezin da fitxategia disko lokalean gorde." )
			else:
				print( "'{}' fitxategia jaso da zuzenki.".format( filename ) )

		elif option == Menua.Prop:
			filename = input( "Idatzi igo nahi duzun fitxategiaren izena: " )
			try:
				filesize = os.path.getsize( filename )
				with open( filename, "rb" ) as f:
					filedata = f.read()
			except:
				print( "'{}' fitxategia ezin izan da atzitu.".format( filename ) )
				continue

			message = "{}{}?{}\r\n".format( szasar.Command.Prop, filename, filesize )
			s.sendall( message.encode( "ascii" ) )
			message = szasar.recvline( s ).decode( "ascii" )
			if iserror( message ):
				continue

			message = "{}\r\n".format( szasar.Command.Upload2 )
			s.sendall( message.encode( "ascii" ) )
			s.sendall( filedata )
			message = szasar.recvline( s ).decode( "ascii" )
			if not iserror( message ):
				print( "'{}' fitxategia bidali da zuzenki.".format( filename ) )

		elif option == Menua.Dump:
			filename = input( "Idatzi ezabatu nahi duzun fitxategiaren izena: " )
			message = "{}{}\r\n".format( szasar.Command.Dump, filename )
			s.sendall( message.encode( "ascii" ) )
			message = szasar.recvline( s ).decode( "ascii" )
			if not iserror( message ):
				print( "'{}' fitxategia ezabatu da.".format( filename ) )

		elif option == Menua.Exit:
			s.close()
			exit(0)
	s.close()
