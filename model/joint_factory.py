""" joint的Factory，用来创建各种各样的joint
"""
import threading
from model.damped_joint import DampedJoint
from model.base_joint import BaseJoint


class JointFactory:
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(JointFactory, "_instance"):
            with JointFactory._instance_lock:
                if not hasattr(JointFactory, "_instance"):
                    JointFactory._instance = object.__new__(cls)
        return JointFactory._instance

    def create_joint(self, joint_type: str, *args):
        if not JointFactory.is_illegal(joint_type):
            raise RuntimeError("ILLegal joint_type !!!")
        if joint_type == "DampedSpring":
            dp: BaseJoint = DampedJoint(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
            dp.create_joint_in_space()
            return dp
        return None

    @staticmethod
    def is_illegal(joint_type: str):
        type_list = ["DampedSpring"]
        if joint_type not in type_list:
            return False
        return True
