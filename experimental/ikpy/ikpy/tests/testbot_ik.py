#"../resources/poppy_ergo.URDF")

import numpy as np
import matplotlib.pyplot as plt
import math

# IKpy imports
from ikpy import chain
from ikpy import plot_utils


def test_ergo(resources_path, interactive):
    a = chain.Chain.from_urdf_file(resources_path + "/testbot.urdf", base_elements=["base"])
    print(a)
    target = [0.15, 0.15, 0.1]
    #target = [0.07, 0.0, 0.0]
    frame_target = np.eye(4)
    frame_target[:3, 3] = target
    joints = [0] * len(a.links)
    print(joints)
    ik = a.inverse_kinematics(frame_target, initial_position=joints)

    print("The angles of each joints are : ", a.inverse_kinematics(frame_target))
    arr =  a.inverse_kinematics(frame_target)
    print("Angle 0: ",math.degrees(arr[0]))
    print("Angle 1: ",math.degrees(arr[1]))
    print("Angle 2: ",math.degrees(arr[2]))
    print("Angle 3: ",math.degrees(arr[3]))
    print("Angle 4: ",math.degrees(arr[4]))
    
    brr = a.forward_kinematics(arr)
    print("Computed position vector: ", brr[:3,3])

    ax = plot_utils.init_3d_figure()
    a.plot(ik, ax, target=target)
    plt.savefig("out/ergo.png")

    if interactive:
        plot_utils.show_figure()

test_ergo("../resources", True)