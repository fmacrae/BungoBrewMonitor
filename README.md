# BungoBrewMonitor
Monitoring for Bungo Brew Co FVs and CO2 emissions


Set up AWS as per:
https://realpython.com/python-boto3-aws-s3/

Create a user with sufficient S3 rights in AWS IAM and take note of private and public keys
Install boto3 and set up your credentials and default region.

Wire your DSB18B20 Temp sensor as per https://medium.com/initial-state/how-to-build-a-raspberry-pi-temperature-monitor-8c2f70acaea9
under the DSB18B20 Solution section

```
sudo nano /boot/config.txt
```
If the following line is not already in this file (if it is, it is likely at the bottom of the file), add it and save the file.
```
dtoverlay=w1-gpio,gpiopin=4
```
Restart your Pi for the changes to take effect.
```
sudo reboot
```



Wire your 811 sensor (VOC and Co2)
as per https://www.makerblog.info/cjmcu-811-with-raspberry-pi.html
I'm using a CJMCU-811

Grabbed this guy's great code to make it work:
https://gist.github.com/xxlukas42/60ae08f75e68a0cfcdb7c9dd60145d34



Added BMP280 following these instructions (temp and barometric pressure): 
https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/circuitpython-test



CORS setup if needing to host html file outside bucket:
```
[
    {
        "AllowedHeaders": [],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```

