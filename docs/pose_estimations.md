# Pose Estimations
This document lists several implementations of pose estimation. 

## Open Pose
[Link](https://github.com/CMU-Perceptual-Computing-Lab/openpose)  
State of the art pose estimation but requiring heavy computation. It's not suitable for mobile device.  

## Mobile Pose
[Link](https://github.com/YuliangXiu/MobilePose-pytorch)  
Much lighter pose estimation implemetation. It seems working with satisfactory performance in Rasberry Pi but need verification. 
  
[Link](https://github.com/savageyusuff/MobilePose-Pi)
MobilePose-Pi, a repository implementing MobilePose for RaspberryPi. It includes installation guide of PyTorch on Raspberry Pi. But reported performance is low(~1 FPS w/ Raspberry Pi 2)


## Pose Proposal net
[Link](https://github.com/Idein/chainer-pose-proposal-net)
Chainer version. This repositroy demonstrates 10 FPS pose estimiation on Rasberry Pi 3. 
[Link](https://github.com/wangziren1/pytorch_pose_proposal_networks)
Pytorch version. I used this version for current demo.
