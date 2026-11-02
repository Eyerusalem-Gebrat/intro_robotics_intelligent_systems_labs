
import math
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.executors import MultiThreadedExecutor

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from my_robot_interfaces.action import Rotate


def get_yaw(quaternion):
    sin_yaw = 2.0 * (
        quaternion.w * quaternion.z +
        quaternion.x * quaternion.y
    )
    cos_yaw = 1.0 - 2.0 * (
        quaternion.y ** 2 + quaternion.z ** 2
    )
    return math.atan2(sin_yaw, cos_yaw)


def normalize_angle(angle):
    return math.atan2(math.sin(angle), math.cos(angle))


class RotateServer(Node):

    def __init__(self):
        super().__init__('rotate_server')

        self.declare_parameter('turn_speed', 0.5)

        self.publisher = self.create_publisher(
            Twist, '/cmd_vel', 10
        )

        self.odom_subscription = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10
        )

        self.current_yaw = None

        self.action_server = ActionServer(
            self,
            Rotate,
            '/rotate',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.get_logger().info('Rotate action server ready')

    def odom_callback(self, msg):
        self.current_yaw = get_yaw(
            msg.pose.pose.orientation
        )

    def stop_robot(self):
        self.publisher.publish(Twist())

    def goal_callback(self, goal_request):
        if abs(goal_request.angle) < 0.001:
            self.get_logger().warning(
                'Rejecting zero rotation goal'
            )
            return GoalResponse.REJECT

        if self.current_yaw is None:
            self.get_logger().warning(
                'No odometry received yet'
            )
            return GoalResponse.REJECT

        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info(
            'Rotation cancellation requested'
        )
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info('Starting rotation')

        result = Rotate.Result()
        total_turned = 0.0

        try:
            if self.current_yaw is None:
                goal_handle.abort()
                return result

            previous_yaw = self.current_yaw
            target_angle = float(goal_handle.request.angle)

            turn_speed = abs(
                self.get_parameter('turn_speed').value
            )

            if turn_speed <= 0.0:
                self.get_logger().error(
                    'Turn speed must be greater than zero'
                )
                goal_handle.abort()
                return result

            direction = 1.0 if target_angle > 0 else -1.0

            while abs(total_turned) < abs(target_angle):

                if goal_handle.is_cancel_requested:
                    self.stop_robot()
                    result.turned = float(total_turned)
                    goal_handle.canceled()
                    return result

                if self.current_yaw is not None:
                    delta = normalize_angle(
                        self.current_yaw - previous_yaw
                    )
                    total_turned += delta
                    previous_yaw = self.current_yaw

                feedback = Rotate.Feedback()
                feedback.turned = float(total_turned)
                goal_handle.publish_feedback(feedback)

                if abs(total_turned) >= abs(target_angle):
                    break

                twist = Twist()
                twist.angular.z = direction * turn_speed
                self.publisher.publish(twist)

                time.sleep(0.02)

            self.stop_robot()

            result.turned = float(total_turned)
            goal_handle.succeed()

            self.get_logger().info(
                f'Rotation completed: {total_turned:.3f} radians'
            )

            return result

        except Exception as error:
            self.stop_robot()
            self.get_logger().error(
                f'Rotation failed: {error}'
            )
            goal_handle.abort()
            result.turned = float(total_turned)
            return result

        finally:
            self.stop_robot()


def main(args=None):
    rclpy.init(args=args)

    node = RotateServer()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
