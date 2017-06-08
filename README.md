# Engineering-Design
this repo contains a backup for the program I made for my Engineering Design course
it's called GNG1103 at the University of Ottawa

The Idea is to automate sensors and loads to a solar powered shed
The shed has 3 sensors: light, temprature, and motion (infrared) sesnors.
The Raspberry pi which I use to control the sensors and loads can only output 12V so I use a relay which acts as a swich to turn on or off
the AC loads(120V) which are connected to an AC electricity source for the ground wire and live wire, and the live wire is split and
connected to the relay, which is connected to the Pi.

the light turns on when it's dark outside and there's motion detected
the heating fan system turns on when temprature is below a certain degree
