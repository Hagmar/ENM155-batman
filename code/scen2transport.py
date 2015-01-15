# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

ind = np.arange(2)
width=0.25
ax = plt.subplot(111)

fos = [94,14.7]
bio = [11,39.7]
el = [0,15.3]
vaet = [0,9.4]

p1 = plt.bar(ind, fos, width, color='#e6d822')
p2 = plt.bar(ind, bio, width, color='#33ff33', bottom=fos)
p3 = plt.bar(ind, el, width, color='#ff3333', bottom=[fos[j] +bio[j] for j in range(len(fos))])
p4 = plt.bar(ind, vaet, width, color='#3333ff', bottom=[fos[j] +bio[j] + el[j] for j in range(len(fos))])

ax.set_xlim(-0.3, 1.5)
ax.set_ylabel('TWh')
ax.set_title(u'Energiförbrukning i transportsektorn')
ax.set_xticks(ind+width/2.)
ax.set_yticks(np.arange(0,120,10))
ax.set_xticklabels(['Nutid', '2030'])
ax.legend( (p4[0], p3[0], p2[0], p1[0]), (u'Vätgas med hjälp av el', 'El', u'Biobränsle', 'Fossil energi'))
plt.savefig('../report2/scen2transport.png', bbox_inches='tight')
plt.show()
