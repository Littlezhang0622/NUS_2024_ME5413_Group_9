# ME5413_Final_Project

NUS ME5413 Autonomous Mobile Robotics Final Project By Group 9 
Date:2024.4.7
> Authors: Zhang Yuanbo; Cao Ruoxi; Li Yuze; Wang Xiangyu; Yin Jiaju; Li Qi

![Ubuntu 20.04](https://img.shields.io/badge/OS-Ubuntu_20.04-informational?style=flat&logo=ubuntu&logoColor=white&color=2bbc8a)
![ROS Noetic](https://img.shields.io/badge/Tools-ROS_Noetic-informational?style=flat&logo=ROS&logoColor=white&color=2bbc8a)
![C++](https://img.shields.io/badge/Code-C++-informational?style=flat&logo=c%2B%2B&logoColor=white&color=2bbc8a)
![Python](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=Python&logoColor=white&color=2bbc8a)

Config:

Camera:Intel realsense D435 + mono

In our first experiment, we trained handwritten digits based on YOLOv3
![Yolo training ](https://github.com/MasterLaoZhang/NUS_2024_ME5413_Group_9/blob/Final/src/gif%26picture/yolo_train.gif)

Finally, we used find_object_2d (template matching) to obtain the pixel coordinates of the target object in the frame, and combined with depth information for navigation implementation
![Final Presentation ](https://github.com/MasterLaoZhang/NUS_2024_ME5413_Group_9/blob/Final/src/gif%26picture/test.gif)


## Dependencies

* System Requirements:
  * Ubuntu 20.04
  * ROS Noetic (Melodic not yet tested)
  * C++11 and above
  * CMake: 3.0.2 and above
* This repo depends on the following standard ROS pkgs:
  * `roscpp`
  * `rospy`
  * `rviz`
  * `std_msgs`
  * `nav_msgs`
  * `geometry_msgs`
  * `visualization_msgs`
  * `tf2`
  * `tf2_ros`
  * `tf2_geometry_msgs`
  * `pluginlib`
  * `map_server`
  * `gazebo_ros`
  * `jsk_rviz_plugins`
  * `jackal_gazebo`
  * `jackal_navigation`
  * `velodyne_simulator`
  * `teleop_twist_keyboard`
  * `find_object_2d`
* And this [gazebo_model](https://github.com/osrf/gazebo_models) repositiory
  Other required libraries are located in the src directory
## Installation

This repo is a ros workspace, containing three rospkgs:

* `interactive_tools` are customized tools to interact with gazebo and your robot
* `jackal_description` contains the modified jackal robot model descriptions
* `me5413_world` the main pkg containing the gazebo world, and the launch files

**Note:** If you are working on this project, it is encouraged to fork this repository and work on your own fork!

After forking this repo to your own github:

```bash
# Clone your own fork of this repo (assuming home here `~/`)
cd
git clone https://github.com/<YOUR_GITHUB_USERNAME>/ME5413_Final_Project.git
cd ME5413_Final_Project

# Install all dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build
catkin_make
# Source 
source devel/setup.bash
```

To properly load the gazebo world, you will need to have the necessary model files in the `~/.gazebo/models/` directory.

There are two sources of models needed:

* [Gazebo official models](https://github.com/osrf/gazebo_models)
  
  ```bash
  # Create the destination directory
  cd
  mkdir -p .gazebo/models

  # Clone the official gazebo models repo (assuming home here `~/`)
  git clone https://github.com/osrf/gazebo_models.git

  # Copy the models into the `~/.gazebo/models` directory
  cp -r ~/gazebo_models/* ~/.gazebo/models
  ```

* [Our customized models](https://github.com/NUS-Advanced-Robotics-Centre/ME5413_Final_Project/tree/main/src/me5413_world/models)

  ```bash
  # Copy the customized models into the `~/.gazebo/models` directory
  cp -r ~/ME5413_Final_Project/src/me5413_world/models/* ~/.gazebo/models
  ```

## Usage

### 0. Gazebo World

This command will launch the gazebo with the project world

```bash
# Launch Gazebo World together with our robot
roslaunch me5413_world world.launch
```

### 1. Mapping(hector_mapping) if you want other slam algorithms, just get the pcd map

After launching **Step 0**, in the second terminal:

```bash
# Launch GMapping
roslaunch me5413_world mapping.launch 
```

After finishing mapping, run the following command in the thrid terminal to save the map:

```bash
# Save the map as `my_map` in the `maps/` folder
roscd me5413_world/maps/
rosrun map_server map_saver -f my_map map:=/map
```


### 2. Navigation

Once completed **Step 1** mapping and saved your map, quit the mapping process.

Then, in the second terminal:

```bash
# Load a map, launch AMCL localizer and time-elastic-band navigation
roslaunch me5413_world teb_navigation.launch
```
Alternatively, you can also try elastic band planner or basic planner:
```bash
# Other navigation methods, less stable
roslaunch me5413_world eband_navigation.launch
roslaunch me5413_world navigation.launch
```

### 3. Box Recognition
#### 2D Detection
To find the desired box (number 2), run the node to do template matching.

```bash
roslaunch me5413_world find_object_2d.launch
```
Then, press the rviz botton `Vehicle-2` to navigate the robot to the entrance of the package area.

Once the robot has reached, press rviz botton `Box-2` to publish the estimated goal pose and navigate.

#### 3D Detection
With depth camera, run this node to do 3D detection.
```bash
roslaunch me5413_world find_object_3d.launch
```
Press rviz botton `Box-3` to navigate to box 2 if depth camera has detected box 2.

The goal is published by 3D frame transformation from depth information. 


## Student Tasks

### 1. Map the environment

* You may use any SLAM algorithm you like, any type:
  * 2D LiDAR
  * 3D LiDAR
  * Vision
  * Multi-sensor
* Verify your SLAM accuracy by comparing your odometry with the published `/gazebo/ground_truth/state` topic (`nav_msgs::Odometry`), which contains the gournd truth odometry of the robot.
* You may want to use tools like [EVO](https://github.com/MichaelGrupp/evo) to quantitatively evaluate the performance of your SLAM algorithm.

### 2. Using your own map, navigate your robot

* From the starting point, move to the given pose within each area in sequence
  * Assembly Line 1, 2
  * Random Box 1, 2, 3, 4
  * Delivery Vehicle 1, 2, 3
* We have provided you a GUI in RVIZ that allows you to click and publish these given goal poses to the `/move_base_simple/goal` topic:
  
  ![rviz_panel_image](src/me5413_world/media/rviz_panel.png)

* We also provides you four topics (and visualized in RVIZ) that computes the real-time pose error between your robot and the selelcted goal pose:
  * `/me5413_world/absolute/heading_error` (in degrees, wrt `world` frame, `std_msgs::Float32`)
  * `/me5413_world/absolute/position_error` (in meters, wrt `world` frame, `std_msgs::Float32`)
  * `/me5413_world/relative/heading_error` (in degrees, wrt `map` frame, `std_msgs::Float32`)
  * `/me5413_world/relative/position_error` (in meters wrt `map` frame, `std_msgs::Float32`)

## Contribution

You are welcome contributing to this repo by opening a pull-request

We are following:

* [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html),
* [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#main),
* [ROS C++ Style Guide](http://wiki.ros.org/CppStyleGuide)

## License

The [ME5413_Final_Project](https://github.com/NUS-Advanced-Robotics-Centre/ME5413_Final_Project) is released under the [MIT License](https://github.com/NUS-Advanced-Robotics-Centre/ME5413_Final_Project/blob/main/LICENSE)
