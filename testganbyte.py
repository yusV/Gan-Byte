import serial, time
import urllib
import xml.etree.ElementTree as ET

arduino = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

arduino.open()

#ARRAY PENYIMPAN DATA
tanah = [0, 0, 0]
cahaya = [0, 0, 0]
siram = [0, 0, 0]
lampu = [0, 0, 0]
suhu = 0
lembab = 0
time = 0


def send-data(tnh, chy, suh, lbb):
	myPort = "8080"
	myParameters = { 	"tnh1" : "%s" %tnh[0], 
						"tnh2" : "%s" %tnh[1], 
						"tnh3" : "%s" %tnh[2], 
						"chy1" : "%s" %chy[0], 
						"chy2" : "%s" %chy[1],
						"chy3" : "%s" %chy[2],
						"suhu" : "%s" %suh,
						"lembab" : "%s" %lbb  
					}
	myURL = urllib.urlopen("http://localhost:%s/read?%s" % (myPort, urllib.urlencode(myParameters)))
	#hasilnya http://localhost (atau 192.168.10.1) /ganbyte/action/read?tnh1=t1&tnh2=t2&tnh3=t3&chy1=c1&chy2=c2&chy3=c3&suhu=suh&lembab=lbb


def get-value-sensor():
	for c in range(len(tanah)):
		arduino.write('2/1/%s') %(c+1)
		tanah[c] = arduino.readline()

	time.sleep(1)
	
	for d in range(len(cahaya)):
		arduino.write('2/2/%s') %(d+1)
		cahaya[d] = arduino.readline()

	time.sleep(1)
	
	arduino.write('2/3/1')
	suhu = arduino.readline()

	time.sleep(1)
	
	arduino.write('2/3/2')
	lembab = arduino.readline()

	time.sleep(1)


def get_instruction():
	xml = urllib.urlopen('192.168.1.4/ganbyte/xml')
	tree = ET.parse(xml)
	root = tree.getroot()
	sir = ['0', '0', '0']
	lam = ['0', '0', '0']

	for data in root.findall('tanaman'):
		kode = data.get('kode')
		kode = int(kode)
		sir[kode - 1] = data.find('siram').text
		lam[kode - 1] = data.find('cahaya').text

	for data in range(len(sir)):
		siram[data] = int(sir[data])

	for data in range(len(lam)):
		lampu[data] = int(lam[data])
	#semua data yang masuk dalam bentuk waktu

def do_instruction():
	for x in range(len(siram)):
		if siram[x] != 0:
			arduino.write('1/1/%s/%s')%((x+1), siram[x])

	for x in range(len(lampu)):
		if lampu[x] != 0:
			arduino.write('1/1/%s/%s')%((x+1), lampu[x])

	time.sleep(1)



try:
    while True:
    	if time == 3600:
    		get-value-sensor()
    		send-data(tanah, cahaya, suhu, lembab)
    		time = 0
    	if time % 300 == 0:
    		get_instruction()
    		do_instruction()
    	time.sleep(1)
    	time += 1
    	

except KeyboardInterrupt:
    arduino.close()


