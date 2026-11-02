import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus

from my_robot_interfaces.action import Rotate
from lab_interfaces.action import DriveDistance


class SquareDriver(Node):

    def __init__(self):
        super().__init__('square_driver')

        self.declare_parameter('side_length', 0.5)

        self.drive_client = ActionClient(
            self, DriveDistance, '/drive_distance'
        )

        self.rotate_client = ActionClient(
            self, Rotate, '/rotate'
        )

        self.side_length = self.get_parameter(
            'side_length'
        ).value

        self.side = 0
        self.stopped = False

        self.get_logger().info('Square driver started')

    def start(self):
        self.get_logger().info('Waiting for robot to spawn...')
        self.timer = self.create_timer(5.0, self.start_square)

    def start_square(self):
        self.timer.cancel()
        self.get_logger().info('Starting square movement')
        self.drive_next_side()

    def stop_sequence(self, message):
        self.stopped = True
        self.get_logger().error(
            f'Square stopped on side {self.side + 1}/4: {message}'
        )
        rclpy.shutdown()

    def drive_next_side(self):
        if self.stopped:
            return

        if self.side >= 4:
            self.get_logger().info('Square completed!')
            rclpy.shutdown()
            return

        self.get_logger().info(
            f'Driving side {self.side + 1}/4'
        )

        goal = DriveDistance.Goal()
        goal.distance = float(self.side_length)

        if not self.drive_client.wait_for_server(timeout_sec=10.0):
            self.stop_sequence('Drive distance server not available')
            return

        future = self.drive_client.send_goal_async(goal)
        future.add_done_callback(self.drive_response)

    def drive_response(self, future):
        if self.stopped:
            return

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.stop_sequence('Drive goal rejected')
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.drive_finished)

    def drive_finished(self, future):
        if self.stopped:
            return

        wrapped_result = future.result()

        if wrapped_result.status != GoalStatus.STATUS_SUCCEEDED:
            self.stop_sequence('Drive action did not succeed')
            return

        if not wrapped_result.result.reached:
            self.stop_sequence('Drive action ended without reaching the target')
            return

        self.get_logger().info('Side completed. Rotating...')

        goal = Rotate.Goal()
        goal.angle = 1.57

        if not self.rotate_client.wait_for_server(timeout_sec=10.0):
            self.stop_sequence('Rotate server not available')
            return

        future = self.rotate_client.send_goal_async(goal)
        future.add_done_callback(self.rotate_response)

    def rotate_response(self, future):
        if self.stopped:
            return

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.stop_sequence('Rotation goal rejected')
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.rotate_finished)

    def rotate_finished(self, future):
        if self.stopped:
            return

        wrapped_result = future.result()

        if wrapped_result.status != GoalStatus.STATUS_SUCCEEDED:
            self.stop_sequence('Rotation action did not succeed')
            return

        self.side += 1
        self.drive_next_side()


def main(args=None):
    rclpy.init(args=args)

    node = SquareDriver()
    node.start()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()