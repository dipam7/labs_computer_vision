In this lab we implement corner detection using Harris detector. The intermediate results are as shown below

### 1. input image 

We take an input image and convert it to greyscale

![test](https://github.com/dipam7/labs_computer_vision/blob/master/lab_3/trial_2.png)

### 2. derivative in x direction - Ix

We calculate the derivatives in the x and y direction

![test](https://github.com/dipam7/labs_computer_vision/blob/master/lab_3/Ix.png)

### 3. derivative in y direction - Iy

![test](https://github.com/dipam7/labs_computer_vision/blob/master/lab_3/Iy.png)

### 4. Ix^2

We calculate Ix square, Iy square and Ixy

![test](https://github.com/dipam7/labs_computer_vision/blob/master/lab_3/Ix2.png)

### 5. Iy^2

![test](https://github.com/dipam7/labs_computer_vision/blob/master/lab_3/Iy2.png)

### 6. Ixy

![test](https://github.com/dipam7/labs_computer_vision/blob/master/lab_3/Ixy.png)

### 6. Output

We calculate eigenvalues from those, use some threshold and find the output

![test](https://github.com/dipam7/labs_computer_vision/blob/master/lab_3/output.png)
