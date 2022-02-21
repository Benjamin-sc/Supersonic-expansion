# Clusters-size introduction
Tkinter GUI to estimate the gas clusters size when expanding into the vacuum after passing through a nozzle.

A Gas cluster is a small particle that can contain 100 to 10 000 atoms bound together by Van Der Waals forces. Neutral clusters are produced in a supersonic expansion where a high pressure of gas is forced through a nozzle. The gas undergoes an adiabatic expansion and the clusters are formed upon cooling.
The interaction of laser pulses with clusters is an active area of research. Moreover cluster beams began to be extensively used for secondary-ion mass spectrometry. In each application, the cluster size is critical [1].

The gas properties, temperature, backing pressure and nozzle geometry affect the properties of the jet and thus the cluster formation. There is no quantative theory to decribe the complex cluster formation but many experimental methods have been developed to estimate the cluster size [2]. The average cluster size N can be described by the semi-empirical Hagena scaling law for axisymmetric gas expansion [2-3]. N can be writen in term of Hagena parameter and the Hagena parameter is function of the backing pressure P<sub>0</sub>, the equivalent (mbar), the equivalent critical-section diameter deq of the nozzle and the gas temperature:
  
  
![Hagena equations](https://user-images.githubusercontent.com/80101412/154300373-5791172a-a7a4-4251-8711-387bb6626da7.png)


Several experiment were performed to determine the constants a and b to match the Hagena scaling law. The table below summarizes the values of thee constants for given intervals of  Hagena parameter. These intervals are taken into account in the GUI.

![table](https://user-images.githubusercontent.com/80101412/154939617-6111059b-1b93-4803-b6a6-7a0eabf6507a.png)

# GUI download and use

The GUI is performed using tkinter package. There are three folders to download; the main script and two images. When you run the script the interface corresponding to the Figure 2 appears. The interface is separated in 4 frames:
- 1) Equivalent critical section diameter. You can decribe the nozzle geometry here. You have the choice between a sonic or a conical nozzle. Due to the effect of inner boundary layers in the conical nozzle, 
- 2) Gas properties
- 3) Hagena parameter
- 4) Result

# References

[1] Shingo Houzumi et al 2005 Jpn. J. Appl. Phys. 44 6252
[2] O. F. Hagena and W. Obert, J. Chem. Phys. 56, 1793 (1972)
[3] O. F. Hagena, Cluster ion sources. Rev. Sci. Instrum. 63(4), 2374–2379 (1992)
[4] Buck, U. & Krohne, R. Cluster size determination from diffractive He atom scattering. J. Chem. Phys. 105(13), 5408–5415 (1996).
