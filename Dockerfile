FROM ros:humble

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    vim \
    ros-humble-rviz2 \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-turtlebot3-gazebo && \
    rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

WORKDIR /workspace

CMD ["bash"]
