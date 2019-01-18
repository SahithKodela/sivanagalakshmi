import pandas as pd
from matplotlib import pyplot as plt

names=['radhika','sai','ram','sahith']
age=[21,22,23,24]

lis=list(zip(names,age))
li=pd.DataFrame(data=lis,columns=['names','age'])
print(li)

x=li['names']
y=li['age']
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y, color='lightblue', linewidth=3)
plt.show()
