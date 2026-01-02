from brping import pinghf
from sensor_msgs.msg import Range
import rclpy

class s500_sonar:
    def __init__(self, parameters, sonar_node):
        # Handle the passed in node
        global node
        node = sonar_node

        # Configure Logger
        global logger
        logger = sonar_node.get_logger()
        logger.info("Initializing s500 sonar device...")
        
        # Initialize parameters
        global params
        params = parameters
        
        # Sonar initialization
        global sonar
        sonar = pinghf.Pinghf()
        
        if params.get("comm_type") == 'serial':
            logger.info("Attempting to connect to device at port %s over serial.\n" % params.get("device_port"))
            sonar.connect_serial(params.get("device_port"), params.get("baudrate"))
        elif params.get("comm_type") == 'udp':
            logger.info("Attempting to connect to device at %s:%s over udp.\n" % (params.get("udp_address"), params.get("udp_port")))
            sonar.connect_udp(params.get("udp_address"), params.get("udp_port"))
        else:
            logger.info("Error when attempting connection. Ensure the comm_type parameter is either serial or udp. \n")
    
    def initialize(self):
        if sonar.initialize() is False:
            return False
        else:
            # Configure Device
            if sonar.set_device_id(params.get("device_id")):
                logger.info("Device ID set to: %d " % params.get("device_id"))
            else:
                logger.warn("Unable to set the device ID")
            if str.lower(params.get("auto_mode")) != 'false':
                if sonar.set_mode_auto(1, True):
                    logger.info("S500 set to automatic mode")
                else:
                    logger.warn("Unable to set automatic mode on device")
            else:
                if sonar.set_mode_auto(0, True):
                    sonar.set_range(params.get("min_range"), params.get("max_range"), False)
                    sonar.set_gain_setting(params.get("gain_index"), False)
                    logger.info("S500 set to manual mode with range [%f:%f]mm and gain index: %f" % (params.get("min_range"), params.get("max_range"), params.get("gain_index")))
                else:
                    logger.warn("Unable to set manual mode on device")
            
            if sonar.set_ping_interval(params.get("ping_interval")):
                logger.info("Pinging at interval %d ms" % params.get("ping_interval"))
            else:
                logger.warn("Unable to set frequency on device")

            if sonar.set_speed_of_sound(params.get("speed_of_sound")):
                logger.info("Speed of sound set to %f mm/s" % params.get("speed_of_sound"))
            else:
                logger.warn("Unable to set speed of sound")
            
            sonar.set_ping_enable(1)
            
            # Create Publisher
            self.publisher_ = node.create_publisher(Range, params.get("sonar_topic"), 10)
            self.timer = node.create_timer(params.get("ping_interval") / 1000.0, self.sonar_callback)
            return True
        
    def disable_sonar(self):
        sonar.set_ping_enable(0)
        
    def sonar_callback(self):
        distance = -1.0 # Set to -1 for people to be able to handle if we aren't able to get a range distance
        global sonar_profile
        min_range = -1.0
        max_range = -1.0

        try:
            sonar_profile = sonar.get_distance() # Try and get sonar profile
            distance = sonar_profile["distance"]
            min_range = sonar_profile["scan_start"]
            max_range = sonar_profile["scan_length"]
        except:
            logger.warn("Unable to get sonar measurement! check device connection.")
            self.disable_sonar()
 
        #sos = sonar.get_distance2()
        range_msg = Range()
        range_msg.header.frame_id = params.get("frame")
        range_msg.header.stamp = node.get_clock().now().to_msg()
        range_msg.radiation_type = 1
        range_msg.field_of_view = params.get("fov")
        range_msg.min_range = min_range * 1.0
        range_msg.max_range = max_range * 1.0
        range_msg.range = distance / 1.0 # returns distance in mm
        #confidence = data["confidence"]
        self.publisher_.publish(range_msg)
        #print(distance)
        #print(sos)
        