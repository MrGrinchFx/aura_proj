#!/bin/bash
pathDatasetEuroc='/Datasets/EuRoC' #Example, it is necesary to change it by the dataset path

#------------------------------------
# Monocular Examples
echo "Launching Custom with Monocular sensor"
./Monocular/mono_euroc ../Vocabulary/ORBvoc.txt ./Monocular/Custom.yaml "$pathDatasetEuroc"/Custom "$pathDatasetEuroc"/Custom/TimeStamps/Custom.txt dataset-Custom