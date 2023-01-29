#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from raytracing import*

systems = ['Na Ji', 'design_3']
system = systems[1]


if system == 'design_3':
    wavelength = 976e-6  # Value from article, in mm
    w = 0.8  # Value from article, in mm
    theta = 0 
    #theta = 0.0990  # In rad, obtained from Code V for w = 0.8 mm (value from article)
    a0 = 2.5  # Value from article, in mm

    """ Focal lengths, in [mm] """
    fLa = -50
    fLb = 100

    """ Spacings, in [mm] """
    dBefore = 50
    da = fLa+fLb
    db = 50


    inputRays = UniformRays(yMin=-a0, yMax=a0, thetaMin=-theta, thetaMax=theta, N=10, M=5)
    inputRays = UniformRays(yMin=0, yMax=2*a0, thetaMin=-theta, thetaMax=theta, N=10, M=5)
    inputRays = UniformRays(yMin=2*a0, yMax=4*a0, thetaMin=-theta, thetaMax=theta, N=10, M=5)

    path = ImagingPath(label='design 3 system')
    path.append(Space(d=dBefore))
    path.append(Lens(f=fLa, diameter=25.4, label='L1'))
    path.append(Space(d=da))
    path.append((Lens(f=fLb, diameter=50.8, label='L2')))
    path.append(Space(d=db))
    path.display(raysList=[inputRays])
