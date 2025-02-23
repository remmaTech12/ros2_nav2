FROM ros:humble

ENV DEBIAN_FRONTEND=noninteractive

ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID usergroup && \
    useradd -m -u $UID -g usergroup -G sudo user && \
    echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

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
