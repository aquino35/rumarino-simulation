#!/usr/bin/env python

import rospy # ros client library
from sensor_msgs.msg import Imu # for imu data
from uuv_sensor_ros_plugins_msgs.msg import DVL # for dvl data
from sensor_msgs.msg import FluidPressure # for pressure sensor data
from hydrus.msg import ControlsMsg as UUV_Message # custom messsage with filtered data


class ControlSystemNode():
    """## Help on the Control System Node module:
    --------------------------------
    ### Name
        ControlSystemNode 

    ---------------------
    ### Description 
    
        This rospy object was developed with the intention of creating a modular ros node inside of a r
        unning roscore. In this case, the node will subscribe to the incoming data from uuv's imu, dvl and 
        pressure sensor, then it will filter and publish the subscribed data to a new ros topic using a 
        custom message with the incoming subscriptions. Finally, a ros subscriber is created to log the 
        new filtered data. Launch can be created with this node to provide modularity with the ros remapping 
        mechanism. View rexrov2_controls_system_node.launch for a clear example.

        @library: rospy -> Ros client library

        @library: ros std sensor_msgs -> Imu and FluidPressure

        @library: uuv_sensor_ros_plugins_msgs -> DVL

        @node controls_system_node:  Reference for roscore.
        
        @topic imu: Placeholder imu topic publishing the imu message structure.
        
        @topic dvl: Placeholder DVL topic publishing the DVL message structure.
        
        @topic pressure: Placeholder pressure sensor topic publishing the fluid pressure message structure.

        @topic controls_system_data: New topic created by node publishing the controls system message structure.

        @subscriber imu_sub: Subscriber created by node. Goal: subscribe to the linear acceleration of the imu on any UUV.
        
        @subscriber dvl_sub: Subscriber created by node. Goal: subscribe to the velocity of the DVL on any UUV.

        @subscriber pressure_sub: Subscriber created by node. Goal: subscribe to the fluid pressure of the pressure sensor on any UUV.
        
        @example: roslaunch hydrus rexrov2_controls_system_node.launch  

        @example: rosrun hydrus controls_systems_node.py imu:=/rexrov2/imu dvl:=/rexrov2/dvl pressure:=/rexrov2/pressure

        @example: python controls_systems_node.py imu:=/rexrov2/imu dvl:=/rexrov2/dvl pressure:=/rexrov2/pressure

    ---------------------
    ### Package Contents
    
        - _imu_sub
        - _dvl_sub
        - _pressure_sub
        - _controls_pub
        - _controls_msg
        - _controls_sub
        - _linear_acceleraton_cb()
        - _velocity_cb()
        - _pressure_cb()

    ---------------------
    @author: Osvaldo Aquino
    """


    def __init__(self):
        """ Constructor of the UUV node."""

        # Initialize ROS node
        rospy.init_node('controls_system_node') 

        # Construct three subscribers that will extract relevant data for the division. 
        self._imu_sub = rospy.Subscriber("imu", Imu, self._linear_acceleration_cb)
        self._dvl_sub = rospy.Subscriber("dvl", DVL, self._velocity_cb)
        self._pressure_sub = rospy.Subscriber("pressure", FluidPressure, self._pressure_cb)

        # Create a new ROS topic called 
        self._controls_pub = rospy.Publisher('/controls_system_data', UUV_Message, queue_size=1)

        # Create custom message with relevant data for controls system
        self._controls_msg = UUV_Message() 

        # Creates a subscriber to our filtered ROS Topic
        self._controls_sub = rospy.Subscriber("/controls_system_data", UUV_Message, self.uuv_subscriber_cb) # construct filtered subscriber 


    def _linear_acceleration_cb(self, incoming_msg : Imu):
        """Callback intended to subscribe and publish the incoming imu's angular acceleration data."""


        self._controls_msg.imu_linear_acceleration = incoming_msg.linear_acceleration
        self._controls_pub.publish(self._controls_msg)


    def _velocity_cb(self, incoming_msg : DVL):
        """Callback intended to subscribe and publish the incoming dvl's velocity data."""
    
           
        self._controls_msg.dvl_velocity = incoming_msg.velocity
        self._controls_pub.publish(self._controls_msg)


    def _pressure_cb(self, incoming_msg : FluidPressure):
        """Callback intended to subscribe and publish the incoming pressure sensor's fluid pressure data."""
        
        self._controls_msg.fluid_pressure = incoming_msg.fluid_pressure
        self._controls_pub.publish(self._controls_msg)


    def uuv_subscriber_cb(self, incoming_msg : UUV_Message):
        """ Callback intended to subscribe to the uvv message published by the node."""

        imu_msg = incoming_msg.imu_linear_acceleration
        dvl_msg = incoming_msg.dvl_velocity
        pressure_sensor_msg = incoming_msg.fluid_pressure
        rospy.loginfo(" UUV filtered data (IMU, DVL, Pressure Sensor): %s %s %s \n", imu_msg, dvl_msg, pressure_sensor_msg )
        
        
    def loop(self):
        """ Loops the ros node object."""

        rospy.spin()


if __name__ == '__main__':

    controls_system_node = ControlSystemNode() # Create the node obj
    controls_system_node.loop() # loop