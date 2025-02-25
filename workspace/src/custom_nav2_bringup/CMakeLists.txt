cmake_minimum_required(VERSION 3.5)
project(custom_nav2_bringup)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch params maps urdf rviz worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
