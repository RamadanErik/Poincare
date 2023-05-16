import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import time
import random


#---------------------Bemenetek----------------------

#eta = np.pi / 2  # EZT KELL VÁLTOZTATNI

hiba1 = 0.8  # EZT KELL VÁLTOZTATNI  pi/2 --> lambda/4
hiba2 = -np.pi+0.3 # EZT KELL VÁLTOZTATNI
hiba3 = -np.pi/2  # EZT KELL VÁLTOZTATNI

felbontas = 9000
pontossag = 100
tureshatar = 0.15**2
#tureshatar = (100 / 2000.0) ** 2

alfa = np.pi / 3.26

# feny = np.array([[1], [0]])  # LHP
# feny = np.array([[0],[1]]) #LVP
# feny = 1/np.sqrt(2)*np.array([[1],[1]]) #+45
# feny = 1/np.sqrt(2)*np.array([[1],[-1]]) #-45
# feny = 1/np.sqrt(2)*np.array([[1],[-1j]]) #RCP
# feny = 1/np.sqrt(2)*np.array([[1],[1j]]) #LCP
feny = np.array([[np.cos(alfa)], [np.sin(alfa)]])



#----------------------------------------------------

eta1 = np.pi/2 + hiba1
eta2 = np.pi + hiba2
eta3 = np.pi/2 + hiba3

np.random.seed(seed=int(time.time()))
count = np.zeros(felbontas)

def wp(theta, eta):
    waveplate = np.exp(-1j * eta / 2) * np.array([[np.cos(theta) ** 2 + np.exp(1j * eta) * np.sin(theta) ** 2,
                                                   (1 - np.exp(1j * eta)) * np.cos(theta) * np.sin(theta)],
                                                  [(1 - np.exp(1j * eta)) * np.cos(theta) * np.sin(theta),
                                                   np.sin(theta) ** 2 + np.exp(1j * eta) * np.cos(theta) ** 2]])
    return waveplate


def kirajzolas(feny, eta1, eta2, eta3):
    S = np.zeros([felbontas,4])
    y = 0
    x = -1
    a = 170.0/180.0*np.pi
    theta_rand_all = np.random.rand(felbontas, 3)*a
    for i in range(felbontas):
        theta_rand = theta_rand_all[i,:]


        wp1 = wp(theta_rand[0], eta1)
        wp2 = wp(theta_rand[1], eta2)
        wp3 = wp(theta_rand[2], eta3)

        out = np.matmul(wp1, feny)
        out = np.matmul(wp2, out)
        out = np.matmul(wp3, out)

        S0 = float(np.abs(out[0]) ** 2 + np.abs(out[1]) ** 2)
        S1 = float(np.abs(out[0]) ** 2 - np.abs(out[1]) ** 2)
        S2 = float(2 * np.real(out[0] * np.conj(out[1])))
        S3 = float(2 * np.imag(out[0] * np.conj(out[1])))

        S[i,:] = np.array([S0, S1, S2, S3])
    return S


def lefedett_felszin(S):   #Ezt át kell nézni!
    #
    # https://www.bogotobogo.com/Algorithms/uniform_distribution_sphere.php
    #
    # random pontok generálása egy gömbön

    x = np.random.rand(pontossag,3)


    theta = np.arccos((2 * np.random.rand(pontossag) - 1))
    phi = 2 * np.pi * np.random.rand(pontossag)
    x[:, 0] = np.sin(theta[:]) * np.cos(phi[:])
    x[:, 1] = np.sin(theta[:]) * np.sin(phi[:])
    x[:, 2] = np.cos(theta[:])

    for i in range(pontossag):

        for p in range(felbontas):
           if ( np.dot( x[i,:]-S[p,1:], x[i,:]-S[p,1:])<tureshatar):
           #if (np.dot(x[i, :] - x[p, :], x[i, :] - x[p, :]) < tureshatar):
               if (count[p]==0):
                   count[p]=1
                   break


    return (sum(count) / (pontossag) * 100)

def tesztkirajzolas():

    x = []
    y = []
    z = []
    theta = np.arccos((2 * np.random.rand(pontossag) - 1))
    phi = 2 * np.pi * np.random.rand(pontossag)
    for i in range(pontossag):
        x.append((np.sin(theta[i]) * np.cos(phi[i])).item())
        y.append((np.sin(theta[i]) * np.sin(phi[i])).item())
        z.append((np.cos(theta[i])).item())

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set the limits of the plot
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([-1, 0, 1])

    ax.set_xticklabels(['-1', '0', '1'])
    ax.set_yticklabels(['-1', '0', '1'])
    ax.set_zticklabels(['-1', '0', '1'])

    # Plot the sphere
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x_sphere = np.cos(u) * np.sin(v)
    y_sphere = np.sin(u) * np.sin(v)
    z_sphere = np.cos(v)
    ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1)

    ax.set_xlabel('S2')
    ax.set_ylabel('S3')
    ax.set_zlabel('S1')

    # Szinezes
    colors = np.linspace(0, 1, len(x))
    colormap = plt.cm.ScalarMappable(cmap='seismic')
    # colormap = plt.cm.ScalarMappable(cmap='hsv')
    # colormap = plt.cm.ScalarMappable(cmap='cool')
    ax.scatter(x, y, z, c=colormap.to_rgba(colors), s=1)
    a = f"Tesztpontok ({pontossag} db)"
    plt.title(a)



    return

x = np.random.rand(pontossag,3)
theta = np.arccos((2 * np.random.rand(pontossag) - 1))
phi = 2 * np.pi * np.random.rand(pontossag)
x[:, 0] = np.sin(theta[:]) * np.cos(phi[:])
x[:, 1] = np.sin(theta[:]) * np.sin(phi[:])
x[:, 2] = np.cos(theta[:])
tav = np.zeros(pontossag)
for i in range(pontossag):
    tav[i] = 100
    for j in range(i+1,pontossag):    #Minden ponttól a legkisebb távolságra lévő tesztpontot megkeresi
        c = np.dot(x[i, :] - x[j, :], x[i, :] - x[j, :])
        if c < tav[i]:
            tav[i] = c

counts, bins = np.histogram(np.sqrt(tav),int(pontossag/20),(0,1))
counts2 = np.zeros(len(counts))
for i in range(len(counts)):
    for j in range(i):
        counts2[i]+=counts[j]
counts2/=pontossag

plt.figure()
plt.stairs(counts2, bins)



S = kirajzolas(feny, eta1, eta2, eta3)

x = []
y = []
z = []
#print(S)
for vector in S:
    s0, s1, s2, s3 = vector[0], vector[1], vector[2], vector[3]
    x.append((s2 / s0).item())
    y.append((s3 / s0).item())
    z.append((s1 / s0).item())

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the limits of the plot
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
ax.set_xticks([-1, 0, 1])
ax.set_yticks([-1, 0, 1])
ax.set_zticks([-1, 0, 1])

ax.set_xticklabels(['-1', '0', '1'])
ax.set_yticklabels(['-1', '0', '1'])
ax.set_zticklabels(['-1', '0', '1'])

# Plot the sphere
u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
x_sphere = np.cos(u) * np.sin(v)
y_sphere = np.sin(u) * np.sin(v)
z_sphere = np.cos(v)
ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1)

ax.set_xlabel('S2')
ax.set_ylabel('S3')
ax.set_zlabel('S1')



#Szinezes
colors = np.linspace(0, 1, len(x))
#colormap = plt.cm.ScalarMappable(cmap='seismic')
#colormap = plt.cm.ScalarMappable(cmap='hsv')
colormap = plt.cm.ScalarMappable(cmap='cool')
ax.scatter(x, y, z, c=colormap.to_rgba(colors), s=1)




a = f"A bemenő fény Jones vektora: {np.array([np.around(feny[0], 4),np.around(feny[1], 4)]).T}"
plt.title(a)


#print(S)
#kirajzolas(feny, eta, eta2, eta)

lef = lefedett_felszin(S)
print(str(round(lef, 2)) + "%-a van lefedve")


plt.savefig(f'Szimulacio_{np.array([np.around(feny[0], 4),np.around(feny[1], 4)]).T}_{round(eta1+hiba1,2)}_{round(eta2+hiba2,2)}_{round(eta3+hiba3,2)}.svg', format='svg',transparent=True)
ax.view_init(azim=30)
plt.savefig(f'Szimulacio_{np.array([np.around(feny[0], 4),np.around(feny[1], 4)]).T}_{round(eta1+hiba1,2)}_{round(eta2+hiba2,2)}_{round(eta3+hiba3,2)}_2.svg', format='svg',transparent=True)
tesztkirajzolas()
plt.savefig(f"Tesztpontok_{pontossag}.svg",format='svg',transparent=True)

plt.show()
