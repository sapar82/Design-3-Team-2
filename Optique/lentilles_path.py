#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from raytracing import*

systems = ['Na Ji', 'design_3_telescope', 'design_3_divergent']
system = systems[1]


if system == 'design_3_telescope':
    wavelength = 976e-6  # Value from article, in mm
    w = 0.8  # Value from article, in mm
    theta = 0 
    #theta = 0.0990  # In rad, obtained from Code V for w = 0.8 mm (value from article)
    a0 = 2.5  # Value from article, in mm

    """ Focal lengths, in [mm] """
    fLa = -50
    fLb = 100

    fLa = -30
    fLb = 60

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



if system == 'design_3_divergent':
    wavelength = 976e-6  # Value from article, in mm
    w = 0.8  # Value from article, in mm
    theta = 0 
    #theta = 0.0990  # In rad, obtained from Code V for w = 0.8 mm (value from article)
    a0 = 2.5  # Value from article, in mm

    """ Focal lengths, in [mm] """
    fLa = -30
    filtre = 1

    """ Spacings, in [mm] """
    dBefore = 10
    da = 40

    #inputRays = UniformRays(yMin=-a0, yMax=a0, thetaMin=-theta, thetaMax=theta, N=10, M=5)
    #inputRays = UniformRays(yMin=0, yMax=2*a0, thetaMin=-theta, thetaMax=theta, N=10, M=5)
    inputRays = UniformRays(yMin=2*a0, yMax=4*a0, thetaMin=-theta, thetaMax=theta, N=10, M=5)

    path = ImagingPath(label='design 3 system')
    path.append(Space(d=dBefore))
    path.append(Lens(f=fLa, diameter=25.4, label='L1'))
    path.append(Space(d=da))
    path.append(Lens(f=filtre, diameter=50.8, label='Filtre'))
    path.display(raysList=[inputRays])
