#!/usr/bin/env python3

import socket, sys, os
import szasar

SERVER = 'localhost'
PORT = 6012

#ez aldatu
class Menua:
	Fold, Batt, Prop, Dump, Exit = range( 1, 6 )
	Options = ( "Eguzki plakak zabaldu/tolestu", "Bateriaren karga maila ikusi", "Pultsatzaile bat martxan jarri", "Sentsoreen neurketak ikusi", "Amaiatu")

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
	#errorea da
	if( message.startswith( "ER" ) ):
		code = message[2:4]
		if code=="01":
			msg="Komando ezezaguna."
		elif code=="02":
			msg="Espero ez zen parametroa. Parametro bat jaso da espero ez zen tokian."
		elif code=="03":
			msg="Hautazkoa ez den parametro bat falta da."
		elif code=="04":
			msg="Parametroak ez du formatu egokia."
		elif code=="05":
			msg="Segurtasun kode okerra."
		elif code=="11":
			msg="Eguzki-plakak zabaldu edo tolestu eragiketa egitea ezinezkoa da."
		elif code=="12":
			msg="Plakak zabaltzea eskatu da eta zabalduta daude jada."
		elif code=="21":
			msg="Ezinezkoa da karga maila eskuratzea erantzuna negatiboa delako."
		elif code=="31":
			msg="Ezin zara propultsorearekin hasi, erantzuna negatiboa ematen du."
		elif code=="32":
			msg="Propultsorearekin hasi zara eta ezin zaio eutsi adierazitako iraupenean."
		elif code=="41":
			msg="Neurketak ezin izan dira eskuratu."
		elif code:
			#ez da definitutako errore-zenbaki bat
			print("Errore ezezaguna.")
			return True
		#errore-zenbaki ezaguna da. errorea inprimatu
		print("Errorea: " + msg)
		return True
	#ez da errorea eta OK da
	elif(message.startswith("OK")):
		return False
	#ez da ez ER ez OK
	return True

if __name__ == "__main__":

	s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
	zerb_helb = (SERVER, PORT)
	s.sendto(b"", zerb_helb)
	buf, beste_helb = s.recvfrom(1024)
	s.connect(beste_helb)

	while True:
		option = Menua.menua()

		if(option == Menua.Exit):
			print("Agur!")
			s.send(b"")
			s.close()
			exit(0)
		key = input("Sartu segurtasun-kodea: ")
		saiakerak=0
		#Kodea ondo sartzeko saiakera kopurua: 3
		while(len(key)!=5 and saiakerak<3):
			print("Kodeak 5eko luzeera izan behar du. Saiatu berriro.")
			key = input("Sartu segurtasun-kodea: ")
			saiakerak+=1


		if option == Menua.Fold:
			print("Zure aukera: Eguzki plakak zabaldu/tolestu\r\n")
			param = input("Plakak zabaldu edo tolestu nahi dituzu? [0=zabaldu, 1=tolestu] ")
			while(param not in ["0","1"]):
				print("Balioa ez da zuzena. Saiatu berriro.")
				param = input("Plakak zabaldu edo tolestu nahi dituzu? [0=zabaldu, 1=tolestu] ")
			message = key + szasar.Command.Fold + param
			s.send(message.encode("ascii"))
			buf=s.recv(1024)
			if not iserror(buf.decode("ascii")):
				if(param=="0"):
					print("Eguzki-plakak zabaltzen...")
				else:
					print("Eguzki-plakak ixten...")

		elif option == Menua.Batt:
			print("Zure aukera: Bateriaren karga maila ikusi\r\n")
			message = key + szasar.Command.Batt
			s.send(message.encode("ascii"))
			buf=s.recv(2+3) # ER + kodea(2) edo OK + portzentaia (3)
			bufDecoded = buf.decode("ascii")
			if not iserror(bufDecoded):
				message = bufDecoded[2:5]
				print("Bateriaren karga honakoa da: %" + message[0:2] +"," + message[2])


		elif option == Menua.Prop:
	            saiakerak1=0
	            saiakerak=0
	            aurkituaid=False
	            aurkituadenb=False
	            print("Zure aukera: Pultsatzaile bat martxan jarri\r\n")
	            paramId = int(input("Adierazi propultsatzailearen identifikatzailea (0-tik 9-rainoko zenbakia) "))
	            while ( (paramId < 0 or paramId > 9) and saiakerak<2 ):
	                print("Balioa ez da zuzena. Saiatu berriro.")
	                paramId = int(input("Adierazi propultsatzailearen identifikatzailea (0-tik 9-rainoko zenbakia) "))
	                saiakerak+=1
	                if saiakerak==2:
	                        aurkituaid=True
	            if aurkituaid:
	                continue
	            paramIraupen= int(input("eta propultsioaren iraupena milisegundutan (3 digitu) "))
	            while ( len(str(paramIraupen)) != 3 and saiakerak1<2 ):
	                print("Balioa ez da zuzena. Saiatu berriro.")
	                paramIraupen= int(input("Orain adierazi propultsioaren iraupena milisegundutan (3 digitu) "))
	                saiakerak1+=1
	                if saiakerak1==2:
	                    aurkituadenb=True

	            if aurkituadenb:
	                continue

	            message = key + szasar.Command.Prop +str(paramId) + str(paramIraupen)
	            s.send(message.encode("ascii"))
	            buf=s.recv(2+2) # OK edo ER + kodea(2)

	            if not iserror(buf.decode("ascii")):
	                    print("Propultsorea ondo aktibatu da.")


		elif option == Menua.Dump:
			print("Zure aukera: Sentsoreen neurketak ikusi\r\n")
			message = key + szasar.Command.Dump
			s.send(message.encode("ascii"))
			# Lehen irakurketa: ER / OK + 1000 byte (edo gutxiago) = 1002 byte max
			buf = s.recv(1002+1)
			# datan neurketa-zati guztiak gorde (OK erantzuna ezik)
			data = buf.decode()[2:]
			if not iserror(buf.decode("ascii")):
				# neurketa-zatiak irakurri, (ER/OK mezurik gabe)
				# bufferraren tamaina 1000 byte baino gutxiago den arte
				# edo 1000 byte eta hurrengoa hutsa
				if(len(buf.decode("ascii")) == 1002+1): #mezua osorik beteta zegoen, 1 gehitu RETURN-agarik
					buf = s.recv(1000+1)
					while(len(buf.decode("ascii")) == 1000+1):
						data += buf.decode("ascii")
						buf = s.recv(1000+1)

					# azken neurketa-zatia gehitu.
					if buf != b"":
						data += buf.decode("ascii")
				print("Eskuratutako neurketak: \r\n" + data)

		# marra bereizlea inprimatu
		print("\r\n" + "="*40 + "\r\n")

	s.send(b"")
	s.close()
