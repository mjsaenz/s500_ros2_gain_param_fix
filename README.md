
# ROS2 Driver for Cerulean Sonar S500

This package implements a ROS driver for the Cerulean Sonar S500 device. It uses the  [ping-python](https://github.com/bluerobotics/ping-python) package to interface with the device. 




## Installing

To install the package simply clone and build like any ROS2 package. [Depends on python3-serial]

```bash
cd <sonar_ws>/src
git clone https://github.com/jackarivera/s500_ros2
cd ../
rosdep install --from-paths src --ignore-src
colcon build
```
    
## Usage

Source your workspace and run the sonar node via:

Run the sonar node
```bash
ros2 run s500_sonar sonar_node
```



## Topics / Parameters
The sonar node publishes to the /s500/sonar_range topic with a range message. It contains the min and max ranges as well as the current range.

The topic can be changed via the sonar_topic parameter.

#### Topics
| Topic | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `/s500/sonar_range` | `Range` | Publishes range data in mm from the s500 device |

#### Parameters
| Parameter | Default     | Description                |
| :-------- | :------- | :------------------------- |
| `comm_type` | `serial` | `serial` or `udp` |
| `device_port` | `/dev/ttyACM0` | The serial port if connected via serial-usb |
| `baudrate` | `115200` | The baudrate of the serial-usb connection |
| `udp_address` | `0.0.0.0` | The UDP address if using an ethernet connection |
| `udp_port` | `12345` | The UDP port if using an ethernet connection |
| `device_id` | `0` | The device ID to set if a different ID is necessary |
| `ping_interval` | `100` | The interval between pings in `ms`. |
| `sonar_topic` | `/s500/sonar_range` | Topic that range data is published to |
| `frame` | `sonar_link` | Frame of the sonar messages |
| `fov` | `0.0872665` | FOV of the sonar transmission. Not used explicitly but put here for data |
| `speed_of_sound` | `1500000` | Speed of sound in medium such as water in `mm/s` |
| `auto_mode` | `true` | Whether to automatically determine gain, min, and max ranges |
| `gain_index` | `0` | Index of the gain setting of the scan when in manual mode. Valid indices are `0-13`. Index-gain correspondences are as follows: `{0: 3.98, 1: 7.96, 2: 15.92, 3: 19.90, 4: 31.84, 5: 39.80, 6: 63.68, 7: 219.2, 8: 438.4, 9: 548.0, 10: 876.8, 11: 1096, 12: unknown, 13: unknown}`|
| `min_range` | `0` | Min range of scan in mm when in manual mode |
| `max_range` | `5000` | Max range of scan in mm when in manual mode |







## License

[MIT](https://choosealicense.com/licenses/mit/)
