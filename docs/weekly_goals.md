# Weekly Goals

## 4: 09.24 - 10.01
### TO DO
- [X] Order HWs
- [X] Plan how to port pose estimation implementation to Raspberry Pi

### Reports
- Inverstigating several demonstrations of computer vision project on Rasberry Pi, I found my project to be more challenging than I thought. It seems to require heavy optimization or networking implementation.
- The problem comes from the fact that GPU embedded in Rasberry Pi(Broadcom Video Core) is not CUDA compatible. It means widely used deep learning frameworks, such as PyTorch, TensorFlow, are not able to support Rasberry Pi to make inference using GPU naturally.  Without GPU support, almost every(at least all implementations I've found so far) pose estimiation show impractical performance, less than 1 fps. 
- Some implementations demonstrated high-fps real time pose estimation using Rasberry Pi but they didn't reveal how they achived such high fps([Link](https://www.youtube.com/watch?v=L_kAUnAgkfg)). I found a comment which said that they implemented a software using Video Core instruction set to enable high performance deep learning on rasberry Pi. This team didn't also explain how exactly they made it.
- So, here I suggest two solutions for this issue. 
    - Modify existing implementations to use Video Core in Rasberry Pi. This is a kind of code optimization job, which soudns fun. But it requires studying Video Core python API and I might have to implement wrapper functions for PyTorch. That's a quite tough job.
    - Use networking. The pipeline is as follows. First, Rasberry Pi captures a video and send it to server computer which is a high performance GPU-available PC using networking. Second, server computer make inference in real time. Third, send the numerical information of 2D joint position back to Rasberry Pi using network. Fourth, Rasberry Pi draws 2D joint position on the video in real time and give an user a feedback based on 2D joint position.
- How to install PyTorch on Raspberry Pi?([Link](https://gist.github.com/fgolemo/b973a3fa1aaa67ac61c480ae8440e754)  

## 5: 10.01 - 10.08
### TO DO
- [X] Order additional HWs
- [X] Collect and classfy different push-up positions
- [X] Analyze the position of joints during different push-up position in executing pose estimation

## 6: 10.08 - 10.15
### TO DO
- [X] Run push-up demo on Jetson Nano for intermediate presentation preparation
- [X] Make a simple feedback for elbow flare
- [X] Install webcam on Jetson Nano

## 7: 10.15 - 10.22
### TO DO
We have the intermediate presentation next week!
- [X] Integrate OpenPose webcam mode with analysis program
- [X] Collect push-up data
- [X] Try clustering to distinguish elbow flare from normal push-up

## 9: 10.29 - 11.05
### TO DO
- [ ] Improve the precision of min-max feedback system 
- [X] Design and order hardware frame
- [X] Devise an algorithm for detecting elbow flare

## 10: 11.05 - 11.12
### TO DO
- [X] Improve the precision of min-max feedback system(Cont.) 
- [X] Make HW frame using 3D printer
- [X] Add more detection algorithms by resolving addressed issues

## 11: 11.12 - 11.19
### TO DO
- [ ] Integrate HW parts
- [ ] Design and Implement GUI
- [ ] Improve feedback system(Cont.) 



