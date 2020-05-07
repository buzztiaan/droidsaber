#!/usr/bin/env python
#
# attempt to clone thinksaber functionality for iio style accelerometers
# as used on Motorola Droid 4 in mainline kernel (as of 5.6.x)
#
# buZz / NURDspace
#

import os
import sys
import pygame
import getopt
import random
import string
import math
import re
import struct

# global constants

FREQ = 44100
BITSIZE = -16
CHANNELS = 2
BUFFER = 1024
FRAMERATE = 120


def stddev(ar):
    sumto = sum(ar)
    sumsq = sum([i*i for i in ar])
    return (math.sqrt((len(ar) * sumsq) - (sumto * sumto)) /
            (len(ar)*(len(ar) - 1)))


class Droidsaber:

    def __init__(self, opts = {}):

        self.options = {'swing': 2.0,
                        'strike': 4.5,
                        'hit': 6.0,
                        'path': '.'}

        self.options.update(opts)
        self.foundsound = [i for i in os.listdir(self.options['path'])
                           if i[-4:] in ['.wav', '.mp3']]


    def play(self):

        try:
            pygame.init()
            pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
        except pygame.error, exc:
            raise RuntimeError, "Could not initialize sound system: %s" % exc


        def gs(m):
            r = [pygame.mixer.Sound(os.path.normpath(
                                    os.path.join(self.options['path'], i)))
                 for i in self.foundsound
                 if re.match(m + r'\d+\.\w{3}$', i)]
            if len(r) < 1:
                raise RuntimeError, "Did not find files for %s sounds." % m
            return r

        sounds = dict([(i, gs(i)) for i in
                       ['start', 'on', 'off', 'idle',
                        'swing', 'strike', 'hit']])

        # get accel data (only x and y???)
        queue = {'x': [0 for i in xrange(0, 8)],
                 'y': [0 for i in xrange(0, 8)]}

        prev = 0
        up = True


        def psound(i):
            sounds[i][random.randint(0, len(sounds[i]) - 1)].play()

        try:
            clock = pygame.time.Clock()
            sounds['on'][0].play()
            while pygame.mixer.get_busy():
                clock.tick(FRAMERATE)

            idle_channel = pygame.mixer.Channel(0)
            idle_channel.set_endevent(pygame.constants.USEREVENT)
            idle_channel.play(sounds['idle'][0])

            while 1:

                with open('/dev/iio:device2', 'rb') as f:
                    b = f.read(16)

                accelx = struct.unpack('h', b[0:2])[0] >> 4
                accely = struct.unpack('h', b[2:4])[0] >> 4
                accelz = struct.unpack('h', b[4:6])[0] >> 4

                event = pygame.event.get()
                if len(event)>0:
                    if event[0].type == idle_channel.get_endevent():
                        idle_channel.play(sounds['idle'][0])
                if 1:
                    [queue[i].pop(0) for i in queue.keys()]
                    queue['x'].append(accelx * 0.048)
                    queue['y'].append(accely * 0.048)
                    val = max(stddev(queue['x']), stddev(queue['y']))
#                    print val
                    if (up):
                        if (val > prev):
                            prev = val
                            continue
                        if (val > self.options['hit']):
                            psound('hit')
                        elif (val > self.options['strike']):
                            psound('strike')
                        elif (val > self.options['swing']):
                            psound('swing')
                        up = False
                        continue
                    if (val > prev):
                        prev = val
                        up = True
                        continue
                    prev = val


        except KeyboardInterrupt:
            idle_channel.stop()
            sounds['off'][0].play()
            while pygame.mixer.get_busy():
                clock.tick(FRAMERATE)

        return 0



def usage(showall = True):
    o = ('-s, --swing=NUMBER     Threshold at which a "swing" sound occurs.',
         '-t, --strike=NUMBER    Threshold at which a "strike" sound occurs.',
         '-h, --hit=NUMBER       Threshold at which a "hit" sound occurs.',
         '-u, --usage            This help.',
         '-v, --version          Version information',
         '',
         'Thresholds are floating point numbers.  The highter the number, ',
         'the harder you have to swing the device to get a sound effect. ',
         'Meaningful values are somewhere between 1.0 and 9.0',
         '')

    print 'Droidsaber version %s' % __version__
    if showall:
        print string.join(o, '\n')


if __name__ == '__main__':
    tsopts = {}
    opts, args = getopt.getopt(sys.argv[1:], "p:s:t:h:uv",
       ["path=", "swing=", "strike=", "hit=", "usage", "version"])
    for o, a in opts:
        if o in ('-p', '--path'):
            if not os.path.isdir(a):
                raise RuntimeError, '%s is not a directory' % a
            tsopts['path'] = a
        if o in ('-s', '--swing', '-t', '--strike', '-h', '--hit'):
            tsopts[{'s': 'swing',
                    't': 'strike',
                    'h': 'hit'}.get(o.replace('-', ''),
                                    o.replace('-', ''))] = float(a)
        if o in ('-u', '--usage'):
            usage()
            sys.exit(0)

        if o in ('-u', '--usage'):
            usage(False)
            sys.exit(0)

    droidsaber = Droidsaber(tsopts)
    droidsaber.play()
