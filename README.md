# Droidsaber - Turn your linux into a lightsaber!

## Main Idea

Droidsaber uses the IIO system to read out a accelerometer and make
appropriately giggle-worthy Star Wars-like lightsaber sound effect.

## Howto

1. Find the right IIO sensor, on droid4 maemo leste beowulf, its /dev/iio:device2
2. goto /sys/bus/iio/devices/iio:device2/scan_elements and echo 1 > in_accel_x_en , do the same to y_en, z_en and timestamp_en
3. goto /sys/bus/iio/devices/iio:device2/buffer and echo 1 > enable
4. start the program

Step 2, 3 and 4 might require root access.

## Acknowledgements

(the original) Thinksaber is obviously inspired by the program MacSaber, and I'm
grateful to the MacSaber people for assembling the Star Wars sound
effects collection needed to make it so successful.

Thinksaber uses a motion-detection algorithm derived from the one
written by Tatsuhiko Miyagawa (miyagawa at gmail.com) for his own
thinkpad-saber program, which ran only under Perl for Windows.

Droidsaber adapts thinksaber to use something else.

## Requirements

Droidsaber runs under PyGame, a python-based gaming library, and
should run on any device with IIO sensors and PyGame installed.

## NO WARRANTY GRANTED OR IMPLIED
