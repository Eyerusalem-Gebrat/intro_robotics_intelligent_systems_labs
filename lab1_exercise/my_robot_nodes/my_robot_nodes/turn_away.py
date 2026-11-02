
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool
from lab_interfaces.msg import ObstacleInfo
from my_robot_interfaces.msg import RobotStatus
from my_robot_interfaces.srv import SetTurnSpeed


class TurnAway(Node):

    def __init__(self):
        super().__init__('turn_away')

        self.declare_parameter('forward_speed', 0.2)
        self.declare_parameter('turn_speed', 0.5)
        self.declare_parameter('max_turn_speed', 1.5)

        self.enabled = False
        self.last_distance = float('inf')

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_publisher = self.create_publisher(
            RobotStatus, '/robot_status', 10
        )

        self.subscription = self.create_subscription(
            ObstacleInfo, '/obstacle', self.obstacle_callback, 10
        )

        self.create_service(SetBool, '/turn_away_enable', self.on_enable)
        self.create_service(
            SetTurnSpeed, '/set_turn_speed', self.on_set_turn_speed
        )

        self.get_logger().info('Turn away node started (disabled)')

    def publish_status(self, state):
        status = RobotStatus()
        status.state = state
        status.obstacle_distance = float(self.last_distance)
        self.status_publisher.publish(status)

    def stop(self):
        self.publisher.publish(Twist())
        self.publish_status('stopped')

    def on_enable(self, request, response):
        if request.data:
            self.enabled = True
            response.success = True
            response.message = 'turn away enabled'
        else:
            self.enabled = False
            self.stop()
            response.success = True
            response.message = 'turn away disabled'

        self.get_logger().info(response.message)
        return response

    def on_set_turn_speed(self, request, response):
        speed = float(request.turn_speed)
        maximum = self.get_parameter('max_turn_speed').value

        if speed <= 0.0 or speed > maximum:
            response.success = False
            response.message = f'turn speed must be above 0 and at most {maximum}'
        else:
            self.set_parameters([
                Parameter('turn_speed', value=speed)
            ])
            response.success = True
            response.message = f'turn speed set to {speed}'

        return response

    def obstacle_callback(self, msg):
        self.last_distance = msg.distance

        if not self.enabled:
            self.publish_status('stopped')
            return

        forward_speed = self.get_parameter('forward_speed').value
        turn_speed = self.get_parameter('turn_speed').value

        twist = Twist()

        if not msg.too_close:
            twist.linear.x = forward_speed
            state = 'forward'
        else:
            twist.angular.z = -turn_speed if msg.angle > 0 else turn_speed
            state = 'turning'

        self.publisher.publish(twist)
        self.publish_status(state)


def main(args=None):
    rclpy.init(args=args)
    node = TurnAway()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
