#!/bin/sh

# disable buffer first
echo 0 | sudo tee /sys/bus/iio/devices/iio:device2/buffer/enable >> /dev/null

# setup contents of buffer
echo 1 | sudo tee /sys/bus/iio/devices/iio:device2/scan_elements/in_accel_x_en >> /dev/null
echo 1 | sudo tee /sys/bus/iio/devices/iio:device2/scan_elements/in_accel_y_en >> /dev/null
echo 1 | sudo tee /sys/bus/iio/devices/iio:device2/scan_elements/in_accel_z_en >> /dev/null
echo 1 | sudo tee /sys/bus/iio/devices/iio:device2/scan_elements/in_timestamp_en >> /dev/null

# setup for 100hz reads
echo 100 | sudo tee /sys/bus/iio/devices/iio:device2/sampling_frequency >> /dev/null

# enable buffer
echo 1 | sudo tee /sys/bus/iio/devices/iio:device2/buffer/enable >> /dev/null

sudo python3 ./droidsaber.py
