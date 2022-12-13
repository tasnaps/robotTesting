# EV3 on micropython. Football player robots code functions:

### movement

The main movement function to perform turning and going forward actions. When the ball recognized between the two "hands", we move to moveToLine function
Otherwise we update our values and move and turn accordingly.

### moveToLine

This function makes the robot return to the middle line. Sometimes we use time.sleep to give some breathing room for the robot. In troubleshooting
Delay sometimes helps with getting correct angle.

This function also calls other functions such as movement in case of ball loss, checkBallControl function to check ball location, getRotation to get current angling.

### deduct

This method is called when we have extra spin on global values and deduct those.
