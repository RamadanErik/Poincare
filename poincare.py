import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import time
import random


#---------------------Bemenetek----------------------

#eta = np.pi / 2  # EZT KELL VÁLTOZTATNI

hiba1 = -np.pi/2+0.7  # EZT KELL VÁLTOZTATNI  pi/2 --> lambda/4
hiba2 = 0.5  # EZT KELL VÁLTOZTATNI
hiba3 = -np.pi/2   # EZT KELL VÁLTOZTATNI

felbontas = 5000
pontossag = 3000
tureshatar = (50 / 2000.0) ** 2

# feny = np.array([[1], [0]])  # LHP
# feny = np.array([[0],[1]]) #LVP
# feny = 1/np.sqrt(2)*np.array([[1],[1]]) #+45
# feny = 1/np.sqrt(2)*np.array([[1],[-1]]) #-45
# feny = 1/np.sqrt(2)*np.array([[1],[-1j]]) #RCP
feny = 1/np.sqrt(2)*np.array([[1],[1j]]) #LCP
# feny = np.array([[np.cos(alfa)], [np.sin(alfa)]])

#alfa = np.pi / 3

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


# def forgatas(feny, fok, eta, eta2):
#     S = []
#     for i in np.linspace(0, fok, 101):
#         wpi = wp(i, eta)
#         wpi2 = wp(i, eta2)
#         out = np.matmul(wpi, feny)
#         out = np.matmul(wpi2, out)
#         S0 = np.abs(out[0]) ** 2 + np.abs(out[1]) ** 2
#         S1 = np.abs(out[0]) ** 2 - np.abs(out[1]) ** 2
#         S2 = 2 * np.real(out[0] * np.conj(out[1]))
#         S3 = 2 * np.imag(out[0] * np.conj(out[1]))
#         Si = [S0, S1, S2, S3]
#         S.append(Si)
#     return S


def kirajzolas(feny, eta1, eta2, eta3):
    S = np.zeros([felbontas,4])
    y = 0
    x = -1
    a = 180.0/180.0*np.pi
    theta_rand_all = np.random.rand(felbontas, 3)*a
    for i in range(felbontas):
        theta_rand = theta_rand_all[i,:]

    #for j in range(3):
    #     theta_rand[j] *= 2*np.pi*170/360

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



    #szorzo = 100
    #tureshatar *= szorzo
    # theta = np.random.rand(pontossag)*np.pi
    # phi = np.random.rand(pontossag)*np.pi*2
    #
    # u = np.random.rand(pontossag)
    # v = np.random.rand(pontossag)
    theta = np.arccos((2 * np.random.rand(pontossag) - 1))
    phi = 2 * np.pi * np.random.rand(pontossag)
    x[:, 0] = np.sin(theta[:]) * np.cos(phi[:])
    x[:, 1] = np.sin(theta[:]) * np.sin(phi[:])
    x[:, 2] = np.cos(theta[:])

    for i in range(pontossag):

        for p in range(felbontas):
           # if (np.abs(S[p][1] - x1) < tureshatar) and (np.abs(S[p][2] - y1) < tureshatar) and (np.abs(S[p][3] - z1) < tureshatar):
           #     count += 1
          # print(x - S[p,1:])
           if ( np.dot( x[i,:]-S[p,1:], x[i,:]-S[p,1:])<tureshatar):
               if (count[p]==0):
                   count[p]=1
                   break


    return (sum(count) / (pontossag) * 100)





def plotting():
    eta = 1
    # S = forgatas(feny, fok, eta)
    S = kirajzolas(feny, eta1, eta2, eta3)

    x = []
    y = []
    z = []

    for i in range(felbontas):
        s0, s1, s2, s3 = S[i,0], S[i,1], S[i,2], S[i,3]
        x.append((s2 / s0).item())
        y.append((s3 / s0).item())
        z.append((s1 / s0).item())

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
    # Plot the points connected with a continuous line
    ax.plot(x, y, z, color='blue', linewidth=0.1)

    a = "Eta = " + str(np.around(eta, 4)) + " \nfeny = [ " + str(np.around(feny[0], 4)) + " , " + str(
        np.around(feny[1], 4)) + " ]"
    plt.title(a)

    # Create the slider and set the update function
    axeta = fig.add_axes([0.05, 0.25, 0.0225, 0.63])
    eta_slider = Slider(
        ax=axeta,
        label="Eta",
        valmin=0,
        valmax=np.pi * 2,
        valinit=eta,
        orientation="vertical"
    )

    # Create the slider and set the update function
    axeta2 = fig.add_axes([0.15, 0.25, 0.0225, 0.63])
    eta2_slider = Slider(
        ax=axeta2,
        label="Eta2",
        valmin=0,
        valmax=np.pi * 2,
        valinit=eta2,
        orientation="vertical"
    )

    return


def update(val):
    eta = val
    # S = forgatas(feny, fok, eta, eta2)
    S = kirajzolas(feny, eta1, eta2, eta3)

    x = []
    y = []
    z = []

    for vector in S:
        s0, s1, s2, s3 = vector[0], vector[1], vector[2], vector[3]
        x.append((s2 / s0).item())
        y.append((s3 / s0).item())
        z.append((s1 / s0).item())

    # Plot the points connected with a continuous line
    ax.plot(x, y, z, color='blue', linewidth=0.1)

    return


def update2(val):
    eta2 = val
    # S = forgatas(feny, fok, eta, eta2)
    S = kirajzolas(feny, eta1, eta2, eta3)

    x = []
    y = []
    z = []

    for vector in S:
        s0, s1, s2, s3 = vector[0], vector[1], vector[2], vector[3]
        x.append((s2 / s0).item())
        y.append((s3 / s0).item())
        z.append((s1 / s0).item())

    # Plot the points connected with a continuous line
    ax.plot(x, y, z, color='blue', linewidth=0.1)

    return


#eta = np.pi
#eta2 = np.pi * 3 / 4
#fok = np.pi * 2

# S = forgatas(feny, fok, eta,eta2)
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




a = "[ " + str(np.around(feny[0], 4)) + " , " + str(
    np.around(feny[1], 4)) + " ]"
plt.title(a)

# # Create the slider and set the update function
# axeta = fig.add_axes([0.05, 0.25, 0.0225, 0.63])
# eta_slider = Slider(
#     ax=axeta,
#     label="Eta",
#     valmin=0,
#     valmax=np.pi * 2,
#     valinit=eta,
#     orientation="vertical"
#)

# Create the slider and set the update function
# axeta2 = fig.add_axes([0.15, 0.25, 0.0225, 0.63])
# eta2_slider = Slider(
#     ax=axeta2,
#     label="Eta2",
#     valmin=0,
#     valmax=np.pi * 2,
#     valinit=eta2,
#     orientation="vertical"
# )
# # MÉG NEM JÓ!

#print(S)
#kirajzolas(feny, eta, eta2, eta)

# eta_slider.on_changed(update)
# eta2_slider.on_changed(update2)

lef = lefedett_felszin(S)
print(str(round(lef, 2)) + "%-a van lefedve")

plt.show()
