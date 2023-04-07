# Driver Restlessness detection 
### Aim: to detect driver restlessness using Emotion detection ML model and Heart Rate Sensor. 

***Inspired by the need to add to driver safety systems to a vehicle, this is a project to detect and create an Alert when a distressed driver is detected at the wheel.***

#### Decision to create an alert is based on 2 main systems that interact with the driver
-  Detecting and identifying facial expression of driver using OpenCV and Emotional Detection ML Model.
-  Monitor Drivers Heart Rate.

### Emotion detection 
- Making use of pretrained or selftrained model to idetntify the drivers emotion at that instant. Sliding window algorithm running in the background to measure frequency of every window range and finally the program checks whether the frequency pattern is goung above the set threshold to conclude a restless emotion

## Heartrate Sensor 
- Using the PULSE SENSOR, heart rate of driver is contantly measured. Data is recieved as Serial input through Ardunio UNO which is used to run the Sensor.
- Time period unsual HeartRate (that is above a threshold) is monitored its time period then is reported.

## Final Decision (in progress)
- Based on the noted time periods of a Restless Expression and Unusual Heartrates , by comparing the time Ranges during which these traits were noted , we can bring out an Alert to conclude that the Driver is a "RESTLESS STATE" and my not be fit to drive with necessary safety measures being activated accordingly.
