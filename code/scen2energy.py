
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

ind = np.arange(2)
width=0.35
ax = plt.subplot(111)
vat = [71.43,78.737]
bio = [151.14,179.99]
fos = [201.64,122.35]
vind = [4.18,4.6122]
kaern = [174.4988,192.336]

p1 = plt.bar(ind, vat, width, color='#ff0000')
p2 = plt.bar(ind, bio, width, color='#33ff33', bottom=vat)
p3 = plt.bar(ind, fos, width, color='#3333ff', bottom=[vat[j] + bio[j] for j in range(len(vat))])
p4 = plt.bar(ind, vind, width, color='#aad8e6', bottom=[vat[j] + bio[j] + fos[j] for j in range(len(vat))])
p5 = plt.bar(ind, kaern, width, color='#FF6600', bottom=[vat[j] + bio[j] + fos[j] + vind[j] for j in range(len(vat))])

ax.set_xlim(-0.3, 3)
ax.set_ylabel('TWh')
ax.set_title(u'Primärenergiernas förbrukning')
ax.set_xticks(ind+width/2.)
ax.set_yticks(np.arange(0,620,50))
ax.set_xticklabels(['Nutid', '2030'])
ax.legend( (p5[0], p4[0], p3[0], p2[0], p1[0]), (u'Kärnkraft', 'Vindkraft', u'Fossila bränslen', u'Biobränsle', 'Vattenkraft'), bbox_to_anchor=(0.632,0.65), loc=2, borderaxespad=0.)
plt.show()
