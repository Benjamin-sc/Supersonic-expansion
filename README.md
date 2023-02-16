# Supersonic expansion 
Tkinter GUI to characterize a supersonic expansion of a gas expanding into the vacuum after passing through a nozzle.

# Introduction
This tkinter GUI contains several tabs that allow to characterize a supersonic expansion that is use in a wide range of scientific domains. The first tab is used to estimate the average cluster size of the clusters formed during the expansion. The second tab is used to estimate the distance of the Mach disk from the nozzle in function of the conditions. These two properties are essential when designing an experiment. The third one is used to process Schlieren images. An optical system often used to visualize and quantify changes in density. 

# Average cluster size determination 
A Gas cluster is a small particle that can contain 100 to 10 000 atoms bound together by Van Der Waals forces. Neutral clusters are produced in a supersonic expansion where a high pressure of gas is forced through a nozzle. The gas undergoes an adiabatic expansion and the clusters are formed upon cooling.
The interaction of laser pulses with clusters is an active area of research. Moreover, cluster beams began to be extensively used for secondary-ion mass spectrometry. In each application, the cluster size is critical [1].

The gas properties, temperature, backing pressure and nozzle geometry affect the properties of the jet and thus the cluster formation. There is no quantitative theory to describe the complex cluster formation but many experimental methods have been developed to estimate the cluster size [2]. The average cluster size N can be described by the semi-empirical Hagena scaling law for axisymmetric gas expansion [2-3]. N can be written in term of Hagena parameter and the Hagena parameter is function of the backing pressure P<sub>0</sub>, the equivalent (mbar), the equivalent critical-section diameter d<sub>eq</sub> of the nozzle and the gas temperature:

![Hagena equations](https://user-images.githubusercontent.com/80101412/154300373-5791172a-a7a4-4251-8711-387bb6626da7.png)

*Fig. 1. Hagena parameter and average cluster size equations.*

Several experiments were performed to determine the constants a and b to match the Hagena scaling law. The table below summarizes the values of thee constants for given intervals of Hagena parameter. These intervals are considered in the GUI.

*Tab. 1. Experimentally determined a and b for a different range of Hagena parameter.*
![table](https://user-images.githubusercontent.com/80101412/154939617-6111059b-1b93-4803-b6a6-7a0eabf6507a.png)

# GUI download and use

The GUI is performed using tkinter package. There are several folders to download including illustrative images and python scripts. You have to run the main script "Createlayout.py". This will open the interface that contains two tabs. The functionalities related to these tabs are contain in the class "ClusterTab_class" and "ShockwaveTab_class".
The first tab offers 4 frames to be filled in by the user (Fig.2):

- 1) *Equivalent critical section diameter*. You can describe the nozzle geometry here. You have the choice between a sonic or a conical nozzle. Due to the effect of inner boundary layers in the conical nozzle, the orifice diameter is replaced by the equivalent diameter d<sub>eq</sub> [5]
- 2) *Gas properties*. This frame contains a selection tree to choose the gas you are working with. Indeed, the Hagena parameter is dependent of a gas specific constant K.
- 3) *Hagena parameter*. Here the temperature of the gas and its pressure are specified. A button allows to compute the Hagena parameter and another the final average cluster size.
- 4) *Result*. A plot of the result is shown. The plot will be directly updated is the parameters are changed. A curve of the average cluster size in function of the Hagena parameter is plotted. The green region shows the values of N for which the experimental power law has been satisfactorily reproduced. The red regions are the extrapolation of the law. The blue square is the final result corresponding at the parameters entered.

![GUI](https://user-images.githubusercontent.com/80101412/173371292-7be0108a-b510-412b-9c80-6f86dd967131.PNG)
*Fig. 2. clusters-size GUI.*

The second tab offers 3 frames to be filled in by the user:

- 1) *Axially symmetric supersonic jet*. Image showing the shock waves of a supersonic expansion.
- 2) *Conditions*. This frame contains three boxes that the user has to fill with the experiment conditions. The final button computes the parameter X<sub>M</sub>.
- 3) *Result*. A plot of the result is shown. The plot will be directly updated is the parameters are changed.The green region shows the values of X<sub>M</sub> for which the experimental power law has been satisfactorily reproduced. The red regions are the extrapolation of the law. The blue square is the final result corresponding at the parameters entered.

![GUI2](https://user-images.githubusercontent.com/80101412/173371820-c7ab80ea-1028-4c1c-89ba-0a6b19778557.PNG)

The third tab is used to load Schlieren images or videos:
- 1) *Schlieren imaging of a supersonic jet*. Image showing a Schlieren image system. The user can load the image and there is an interrogation box to describe the system.
- 2) *Load video and images*. The user load can play here gray or RGB video and perform a background substraction (Gaussian mixture-based Background/Foreground segmentation). The background uses two parameters that can be tuned by the user; a treshold and history value. The gray buttons can be pressed to get the information concerning these two parameters. The last button can be used to add a visual timer on the final video output. The video will be saved at the fps indicated by the user. 
- 3) *Quantification*. The goal here is to process the Schlieren image to quantify the density changes in the expansion. A calibration in Schlieren imaging can be obtained with a lens with a large focal length f [6]. This lens will provide a quantifiable relationship between the deviation angle and the pixel gray value intensity. Indeed a light ray which passes through an arbitrary location on the lens (r) will be refracted through an angle /epsilon. The user get measure the gray pixel intensity value for different location r on the lens and compute a deviation angle (r/f = tan /epsilon) and load the values from an excel. These values will be used to convert the gray image in deviation and density image. If the deflection image is obtained directly, the density is calculated according to a formula involving several simplifications and assumptions that cannot be imposed for each system studied [7].



![GUI3](https://user-images.githubusercontent.com/80101412/219381511-368865a0-c9a1-443a-91c8-76488e3d2e57.PNG)


# References

[1] Shingo Houzumi et al 2005 Jpn. J. Appl. Phys. 44 6252

[2] O. F. Hagena and W. Obert, J. Chem. Phys. 56, 1793 (1972)

[3] O. F. Hagena, Cluster ion sources. Rev. Sci. Instrum. 63(4), 2374–2379 (1992)

[4] Buck, U. & Krohne, R. Cluster size determination from diffractive He atom scattering. J. Chem. Phys. 105(13), 5408–5415 (1996).

[5] Lu, H., Ni, G., Li, R. & Xu, Z. An experimental investigation on the performance of conical nozzles for argon cluster formation in supersonic jets. J. Chem. Phys. 132(12), 124303 (2010).

[6] M.J.H. Ã, G.S. Settles, Opt. Lasers Eng. 50 (2012) 8–17.

[7] A. Scheer, H. Kruppke, R. Heib, Springer-Verlag Berlin Heidelberg GmbH, 2001.
