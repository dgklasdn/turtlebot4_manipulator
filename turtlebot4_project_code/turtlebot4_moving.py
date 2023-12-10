import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import time
from std_msgs.msg import String

location = []

def get_key():

    global location
    location = input("Enter location (a, b, c, or exit): ").split(',')
    return location

def tb4_driving():
    
    global location

    node = Node("my_publisher_node") 

    pose_pup = node.create_publisher(PoseStamped, "/goal_pose", 10)
    position_location = node.create_publisher(String,"position_location",10)

    msg = PoseStamped()
    tb4_ariive = String()

    point = location.pop(0)

    if point == 'a':
        #msg = PoseStamped()
        msg.header.stamp.sec = 0
        msg.header.frame_id = "map"
        msg.pose.position.x = -2.92
        msg.pose.position.y = 0.49
        msg.pose.position.z = 0.0
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 1.0
        msg.pose.orientation.w = 0.0
        print("Moving to location a...")

    elif point == 'b':
        #msg = PoseStamped()
        msg.header.stamp.sec = 0
        msg.header.frame_id = "map"
        msg.pose.position.x = -1.16
        msg.pose.position.y = 2.65
        msg.pose.position.z = 0.34
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = -0.7
        msg.pose.orientation.w = 0.7
        print("Moving to location b...")
                
    elif point == 'c':
        #msg = PoseStamped()
        msg.header.stamp.sec = 0
        msg.header.frame_id = "map"
        msg.pose.position.x = -3.0
        msg.pose.position.y = 2.7
        msg.pose.position.z = 0.0
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 1.0
        msg.pose.orientation.w = 0.0
        print("Moving to location c...")

    elif point == 'd':
        #msg = PoseStamped()
        msg.header.stamp.sec = 0
        msg.header.frame_id = "map"
        msg.pose.position.x = -3.0
        msg.pose.position.y = -1.7
        msg.pose.position.z = 0.34
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = -0.76
        msg.pose.orientation.w = 0.65
        print("Moving to location d...")

    elif point == 'exit':
        rclpy.shutdown()

    else:
        print("Invalid location.")

    pose_pup.publish(msg)
    marker = 0
    time.sleep(20)
    tb4_ariive.data = ('arrive')
    position_location.publish(tb4_ariive)


def callback(str): 

    global location

    print("carry complete")
    
    if str.data == 'marker_arrive':

        if len(location) == 0:
            location = get_key()
            
        else:
            pass
            
        tb4_driving()

def main(args=None):

    global location

    rclpy.init(args=args)
    node = Node("my_subscriptio_node")

    marker_arrive = node.create_subscription(String, '/marker_arrive', callback, 10)
    tb_marker = String() 

    location = get_key()
    tb4_driving() 

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":   
    main()