# Bill learning how to Kalman Filter

This repo is going to contain various learning projects that involve simple Kalman Filters (if there's such a thing as a simple Kalman Filter).

## Kalman Filter simulation results:
### 50 Data Points:
![50 Data Points](https://i.imgur.com/ywXoEKe.png)

### 100 Data Points:
![100 Data Points](https://i.imgur.com/L3OeHQC.png)

### 1000 Data Points:
![1000 Data Points](https://i.imgur.com/FqEcVsg.png)


## Project goals:
- Python KF simulation
  - Model a simple diff-drive with random measurement noise
  - Learning points:
    - KF implementation (theory)
    - Python (general)
    - Python modeling and simulation (Numpy, MatPlotLib, ModSimPy, etc)
- Non-ROS Arduino KF for simple remote diff-drive car from scratch
  - Learning points:
    - KF implementation (practice)
    - Arduino sensor input (IMU/GPS)
- ROS Arduino KF
  - Learning points:
    - ROS

## Python simulation:
### Progress:
- Basic graphing and data generation
- Filter 1D static model
- Filter 1D motion 3 state physical model w/o input (Assuming constant accel)

### Next:
- Add sliders
- Build python & pyplot framework for generating plots w/ sliders easily
- Model a robot drive with input, including input into physical model

## ROS:
### TODO!!


