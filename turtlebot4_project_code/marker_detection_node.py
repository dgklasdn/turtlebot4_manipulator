import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from cv2 import aruco
import geometry_msgs.msg
import math
from std_msgs.msg import String
import time

marker = 0

class MarkerDetectionNode(Node):
    def __init__(self):
        super().__init__('marker_detection_node')
        self.subscription = self.create_subscription(Image, '/color/preview/image', self.image_callback, 10)
        self.subscription  # prevent unused variable warning

        self.bridge = CvBridge()
        self.aruco = aruco

        self.marker_pose = self.create_publisher(geometry_msgs.msg.Twist, 'cmd_vel', 10)
        self.move_cmd = geometry_msgs.msg.Twist()

        self.marker_arrive = self.create_publisher(String, 'marker_arrive', 10)
        self.tb_marker = String()

        self.tb4_arrive = self.create_subscription(String,'/position_location',self.callback,10)
        self.tb4_pose = String()

    def callback(self, msg):
        global marker
        self.tb4_pose = msg.data

        if self.tb4_pose == 'arrive':
            print("aiive at location")
            marker = 10
            
    def image_callback(self, msg):
        global marker

        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        aruco_dict = self.aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        parameters = cv2.aruco.DetectorParameters()

        corners, ids, rejectedImgPoints = aruco.detectMarkers(cv_image, aruco_dict, parameters=parameters)

        if ids is not None:
            for i in range(len(ids)):
                corner = corners[i][0]

                cx = int((corner[0][0] + corner[2][0]) / 2)
                cy = int((corner[0][1] + corner[2][1]) / 2)

                marker_size = abs(corner[0][0] - corner[2][0])

                cv2.putText(cv_image, f"Center: ({cx}, {cy})", (10, 20 + i * 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(cv_image, f"Size: {marker_size}", (10, 40 + i * 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

                if marker == 10: 
                    #print("0")
                    if  25 < marker_size <= 70:
                        if cx <= 104:
                            self.move_cmd.linear.x = 0.03
                            self.move_cmd.linear.y = 0.0
                            self.move_cmd.linear.z = 0.0
                            self.move_cmd.angular.z = 0.04

                        elif 136 <= cx:
                            self.move_cmd.linear.x = 0.03
                            self.move_cmd.linear.y = 0.0
                            self.move_cmd.linear.z = 0.0
                            self.move_cmd.angular.z = -0.04

                        elif 105 <= cx <=135:
                            self.move_cmd.linear.x = 0.05
                            self.move_cmd.linear.y = 0.0
                            self.move_cmd.linear.z = 0.0
                            self.move_cmd.angular.z = 0.0

                    elif marker_size >= 61:
                        self.move_cmd.linear.x = 0.0
                        self.move_cmd.linear.y = 0.0
                        self.move_cmd.linear.z = 0.0
                        self.move_cmd.angular.z = 0.0 
                        print("arrive at marker")
                        print("carring item")

                        time.sleep(5)

                        self.tb_marker.data = ('marker_arrive')
                        self.marker_arrive.publish(self.tb_marker)

                        maker = 0
                        break                          

                    self.marker_pose.publish(self.move_cmd)
            aruco.drawDetectedMarkers(cv_image, corners, ids)
            
        cv2.imshow("ArUco Marker Detection", cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    marker_detection_node = MarkerDetectionNode()

    rclpy.spin(marker_detection_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
