
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

ind = np.arange(2)
width=0.25
ax = plt.subplot(111)

fos = [94,22.8]
bio = [11,60.8]
el = [0,2]

p1 = plt.bar(ind, fos, width, color='#e6d822')
p2 = plt.bar(ind, bio, width, color='#33ff33', bottom=fos)
p3 = plt.bar(ind, el, width, color='#3333ff', bottom=[fos[j] +bio[j] for j in range(len(fos))])

ax.set_xlim(-0.3, 1.5)
ax.set_ylabel('TWh')
ax.set_title(u'Energiförbrukning i transportsektorn')
ax.set_xticks(ind+width/2.)
ax.set_yticks(np.arange(0,120,10))
ax.set_xticklabels(['Nutid', '2030'])
ax.legend( (p1[0], p2[0], p3[0]), ('Fossil energi', u'Biobränsle', 'El'))
plt.savefig('../report2/scen1a2transport.png', bbox_inches='tight')

plt.show()
