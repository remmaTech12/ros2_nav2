#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseWithCovarianceStamped
from lifecycle_msgs.srv import GetState

import time

class InitialposePublisher(Node):
    def __init__(self):
        super().__init__('initialpose_publisher')
        self.amcl_service_name = '/amcl/get_state'
        self.pose_pub = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)

        self.cli = self.create_client(GetState, self.amcl_service_name)

        self.timer = self.create_timer(1.0, self.check_amcl_state)

    def check_amcl_state(self):
        if not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /amcl/get_state service...')
            return
    
        self.get_logger().info('Requesting AMCL state...')
        request = GetState.Request()
        future = self.cli.call_async(request)
        future.add_done_callback(self.handle_amcl_state_response)
    
    def handle_amcl_state_response(self, future):
        try:
            response = future.result()
            state = response.current_state.label
            self.get_logger().info(f'AMCL current state: {state}')
            if state == 'active':
                self.publish_initial_pose()
                self.destroy_timer(self.timer)
                rclpy.shutdown()
        except Exception as e:
            self.get_logger().error(f'Failed to get AMCL state: {e}')

    def publish_initial_pose(self):
        msg = PoseWithCovarianceStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'

        msg.pose.pose.position.x = 0.0
        msg.pose.pose.position.y = 0.0
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.w = 1.0
        msg.pose.covariance = [0.0] * 36

        self.pose_pub.publish(msg)
        self.get_logger().info('Initial pose published')

def main(args=None):
    rclpy.init(args=args)
    node = InitialposePublisher()
    rclpy.spin(node)

if __name__ == '__main__':
    main()