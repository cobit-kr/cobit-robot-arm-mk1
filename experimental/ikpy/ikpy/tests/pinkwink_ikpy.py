import matplotlib.pyplot

from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy import plot_utils
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

test_link = Chain(name='test_arm', links=[
    OriginLink(),
    URDFLink(
      name="first_link",
      translation_vector=[1, 1, 0],
      orientation=[0, 0, 0],
      rotation=[0, 0, 1],
    ),
    URDFLink(
      name="second_link",
      translation_vector=[1, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 0, 1],
    )
])

ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

target_vector  = [ 1, 0, 0]
target_frame = np.eye(4)
target_frame[:3, 3] = target_vector
target_frame
print("The angles of each joints are : ", test_link.inverse_kinematics(target_frame))
real_frame  = test_link.forward_kinematics(test_link.inverse_kinematics(target_frame))
print("--> Computed position vector : %s" % real_frame[:3, 3])
print("--> original position vector : %s" % target_frame[:3, 3])
ax = plot_utils.init_3d_figure()
test_link.plot(test_link.inverse_kinematics(target_frame), ax, target=target_vector)
matplotlib.pyplot.xlim(-1, 2)
matplotlib.pyplot.ylim(-1, 2)
matplotlib.pyplot.show()
