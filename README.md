# Terraria Mining Bot (WIP)
This is an automatic mining bot for Terraria that detects ores using OpenCV, and PyAutoGUI to take care of the actions (To be imported)
The current stage of the bot supports ore classification, but as no cascade classifier files are have been trained yet, auto-movement is yet to be implemented.

## Requirements
- Python 3.8 or greater

### GPU
GPU execution requires the following NVIDIA libraries to be installed:

- [cuBLAS for CUDA 12](https://developer.nvidia.com/cublas)
- [cuDNN 8 for CUDA 12](https://developer.nvidia.com/cudnn)

## Installation
```
git clone https://github.com/akhkim/terraria-mining-bot.git
cd terraria-mining-bot
pip install -r requirements.txt
```

## To be Implemented
- Pre-trained cascades
- Optimizing Memory Usage
- Classification Accuracy
- 
