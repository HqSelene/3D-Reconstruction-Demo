# Use Ubuntu 22.04 (will be supported until April 2027)
# Use Ubuntu 22.04
FROM ubuntu:jammy

# 全局设置
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/openMVG_Build/install/bin:/opt/openMVS_Build/bin:/usr/local/bin:$PATH"

# 一次性安装所有依赖（合并 OpenMVG 和 OpenMVS 的依赖）
RUN apt-get update && \
    apt-get install -y \
    # 基础工具
    wget curl unzip tar pkg-config \
    cmake build-essential graphviz git python3 python3-pip \
    # OpenMVG 依赖
    coinor-libclp-dev libceres-dev liblemon-dev \
    # OpenMVS 依赖
    libboost-iostreams-dev libboost-program-options-dev \
    libboost-system-dev libboost-serialization-dev \
    libopencv-dev libcgal-qt5-dev libglfw3-dev libglew-dev \
    libglu1-mesa-dev libxmu-dev libxi-dev zlib1g-dev \
    libpng-dev libjpeg-dev libtiff-dev libatlas-base-dev \
    libsuitesparse-dev \
    libcgal-dev \
    && apt-get autoclean && apt-get clean

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

RUN cd /opt && wget https://github.com/CGAL/cgal/releases/download/v6.0.1/CGAL-6.0.1.tar.xz && \
    tar -xvf CGAL-6.0.1.tar.xz && \
    cd CGAL-6.0.1 && \
    mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local .. && \
    make -j4 && make install
    
# 安装 VCGLib（OpenMVS 依赖）
RUN git clone https://github.com/cdcseacave/VCG.git /opt/vcglib

# 安装 Eigen (OpenMVS 需要)
#RUN git clone https://gitlab.com/libeigen/eigen.git /opt/eigen && \
#  cd /opt/eigen && \
#  git checkout 3.4.0 && \
#  mkdir build && cd build && \
#  cmake .. && make install

#RUN git clone https://gitlab.com/libeigen/eigen --branch 3.4; \
#  mkdir eigen_build && cd eigen_build; \
#  cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX="/usr/local/include/eigen34" . ../eigen; \
#  make -j$(nproc) && make install; \
#  cd .. && rm -rf eigen_build


# 安装 OpenMVS
RUN git clone --recurse-submodules https://github.com/cdcseacave/openMVS.git /opt/openMVS; \
    #sed -i 's|<CGAL/AABB_traits_3.h>|<CGAL/AABB_tree.h>|g' /opt/openMVS/libs/MVS/SceneReconstruct.cpp && \
    #sed -i 's|<CGAL/AABB_triangle_primitive_3.h>|<CGAL/AABB_triangle_primitive.h>|g' /opt/openMVS/libs/MVS/SceneReconstruct.cpp && \
    mkdir /opt/openMVS_Build && cd /opt/openMVS_Build && \
    cmake -DCMAKE_BUILD_TYPE=Release \
      -DVCG_ROOT=/opt/vcglib \
      #-DEIGEN3_INCLUDE_DIR=/usr/local/include/eigen34/include/eigen3 \
      #-DPython3_ROOT_DIR=$(which python3) \
      -DCMAKE_INSTALL_PREFIX="/opt" \
      ../openMVS && \
    make -j4 && make install
  #cp ../openMVS/scripts/python/MvgMvsPipeline.py /opt/bin/ && \

# 安装 OpenMVG
RUN git clone --recursive https://github.com/openMVG/openMVG.git /opt/openMVG && \
    mkdir /opt/openMVG_Build && cd /opt/openMVG_Build && \
    cmake -DCMAKE_BUILD_TYPE=RELEASE \
      -DCMAKE_INSTALL_PREFIX="/opt/openMVG_Build/install" \
      -DOpenMVG_BUILD_TESTS=ON \
      -DOpenMVG_BUILD_EXAMPLES=OFF \
      -DCOINUTILS_INCLUDE_DIR_HINTS=/usr/include \
      -DLEMON_INCLUDE_DIR_HINTS=/usr/include/lemon \
      -DCLP_INCLUDE_DIR_HINTS=/usr/include \
      -DOSI_INCLUDE_DIR_HINTS=/usr/include \
      ../openMVG/src && \
    make -j4 && make test && make install

WORKDIR /app
ENV PATH="/usr/local/bin:$PATH"
EXPOSE 5000
CMD ["python3", "app/main.py"]