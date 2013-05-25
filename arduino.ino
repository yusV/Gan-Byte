int waktu;
int katub;
int lampu;
int sensorVal;

void setup(){
	Serial.begin(9600);
}

void loop(){
	getSerial();
	switch(serialdata){
		case 1: //output
		{
			getSerial();
			switch(serialdata){
				case 1: //sirem
				{
					getSerial();
					katub = serialdata;
					getSerial();
					waktu = serialdata;
					pinMode(pinNo, OUTPUT);
					switch(katub){
						case 1:
						{
							nyala(2 ,waktu);//pin katub1 = 2
							break;
						}
						case 2:
						{
							nyala(3 ,waktu);//pin katub2 = 3
							break;
						}
						case 3:
						{
							nyala(4 ,waktu);//pin katub3 = 4
							break;
						}
					}
					break;
				}
				case 2: //lampu
				{
					getSerial();
					lampu = serialdata;
					getSerial();
					waktu = serialdata;
					pinMode(pinNo, OUTPUT);
					switch(lampu){
						case 1:
						{
							nyala(5 ,waktu);//pin lampu 1 = 5
							break;
						}
						case 2:
						{
							nyala(6 ,waktu);//pin lampu 2 = 6
							break;
						}
						case 3:
						{
							nyala(7 ,waktu);////pin lampu 3 = 7
							break;
						}
					}
					break;
				}
			}
		}
		////////////////INPUT//////////////////
		case 2://input
		{
			getSerial();
			switch(serialdata){
				case 1://sensor tanah
				{
					bacaSensor();
					break;
				}
				case 2://sensor cahaya
				{
					bacaSensor();
					break;
				}
				case 3:// sensor humidity & temperatur
				{
					int t = 0;
					while(t == 0){
						int chk = DHT11.read(DHT11PIN);
						if(chk == DHTLIB_OK){
							getSerial();
							if (serialdata == 1){ //humidity
								Serial.println((float)DHT11.humidity, 2);
							}
							else if (serialdata == 2){ // temperatur
								Serial.println((float)DHT11.temperature, 2);
							}
							t = 1;
						}
						delay(2000);
					}
					break;
				}
			}
		}
	}
}

void bacaSensor(){
	getSerial();
	pinNo = serialdata;
	pinMode(pinNo, INPUT);
	sensorVal = analogRead(pinNo);
	Serial.println(sensorVal);
	sensorVal = 0;
	pinNo = 0;
}

void nyala(int pinNo, int waktu){
	digitalWrite(pinNo, HIGH);
	delay(waktu*60);
	digitalWrite(pinNo, LOW);
}

long getSerial()
{
  serialdata = 0;
  while (inbyte != '/')
  {
    inbyte = Serial.read(); 
    if (inbyte > 0 && inbyte != '/')
    {
     
      serialdata = serialdata * 10 + inbyte - '0';
    }
  }
  inbyte = 0;
  return serialdata;
}
