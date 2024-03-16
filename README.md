In this code, the calculation of pitch, roll, and yaw is happening through a sensor fusion algorithm known as the complementary filter. 

Calculation steps:
-The code initializes an instance of the Complementary filter from the AHRS library.
-Lists are initialized to store the estimated pitch, roll, and yaw angles.
-An initial quaternion (q) representing the orientation is set to an identity quaternion [1.0, 0.0, 0.0, 0.0].


The code then iterates througb each timestamp in the data (we have extracted time as the primary column from all 3 csv files provided to us)
-The sensor readings are retrieved from the data.
-The Complementary filter's update() method is called passing sensor readings along with the quaternion.
-The Complementary filter updates the quaternion based on the sensor readings and returns the updated quaternion.
-The updated quaternion is converted to Euler angles (pitch, roll, yaw) using the q2euler() function from the AHRS library.
-The estimated pitch, roll, and yaw angles are appended to their respective lists.

Instead of accessing the quaternion directly, I updated it internally and then used the q2euler() function from the AHRS toolbox to convert the quaternion to Euler angles after each update. This allowed for the computation of pitch, roll, and yaw angles correctly without encountering any attribute errors.

A quaternion is a mathematical concept used to represent rotations in three-dimensional space. It extends the idea of complex numbers, which have a real part and an imaginary part, to three dimensions
