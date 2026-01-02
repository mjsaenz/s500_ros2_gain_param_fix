from s500_sonar.s500 import s500_sonar
import rclpy
from rclpy.node import Node

class sonar_node(Node):
    def __init__(self):
        super().__init__("sonar_node")
        self.get_logger().info("Starting Sonar Node...")
    
        # Create dictionary of node parameters to easily pass into sonar object
        parameters = {
            "device_port": self.declare_parameter('device_port', '/dev/ttyACM0').value,
            "baudrate": self.declare_parameter('baudrate', 115200).value,
            "ping_interval": self.declare_parameter('ping_interval', 100).value, # Amount of ping interval of device and publish rate
            "sonar_topic": self.declare_parameter('sonar_topic', 's500/sonar_range').value,
            "frame": self.declare_parameter('frame', 'sonar_link').value,
            "fov": self.declare_parameter('fov', 0.0872665).value, # s500 has fov of 5 degrees or 0.0872665 rad
            "speed_of_sound": self.declare_parameter('speed_of_sound', 1500000).value, # Speed of Sound [mm/s] : Water (1500000 mm/s), Air (340000 mm/s)
            "auto_mode": self.declare_parameter('auto_mode', 'true').value, # Whether s500 automatically sets gain and scan range
            "gain": self.declare_parameter('gain', -1).value, # Gain for s500 if auto_mode = false
            "min_range": self.declare_parameter('min_range', 0).value, # Min range if auto_mode = false [mm]
            "max_range": self.declare_parameter('max_range', 5000).value, # Max range if auto_mode = false [mm]
            "comm_type": self.declare_parameter('comm_type', 'serial').value, # serial or udp
            "udp_address": self.declare_parameter('udp_address', '0.0.0.0').value,
            "udp_port": self.declare_parameter('udp_port', 12345).value,
            "device_id": self.declare_parameter('device_id', 0).value
        }

        # Create device and attempt connection
        global sonar
        sonar = s500_sonar(parameters, self)
        
        if sonar.initialize() is False:
            if parameters.get("comm_type") == "serial":
                self.get_logger().info("Failed to connect to device %s over serial.\n" % parameters.get("device_port"))
            elif parameters.get("comm_type") == "udp":
                self.get_logger().info("Failed to connect to device %s:%s over udp.\n" % (parameters.get("udp_address"), parameters.get("udp_port")))
            
            self.get_logger().info("Shutting down this node...\n")
            self.destroy_node()
            rclpy.shutdown()
        else:
            self.get_logger().info("Successfully connected to device at %s" % parameters.get("device_port"))

       
def main(args=None):
    rclpy.init(args=args)
    node = sonar_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        sonar.disable_sonar()
        node.get_logger().info("Shutting down the node")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
