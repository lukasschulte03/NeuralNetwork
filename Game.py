
Main_posX = 0.0
Main_posY = 0.0
Main_velocityX = 0.0
Main_velocityY = 0.0
Main_accelerationX = 0.0
Main_accelerationY = 0.0
L_thrust = 0.0
R_thrust = 0.0
L_angle = 0.0
R_angle = 0.0
L_angularVelocity = 0.0
R_angularVelocity = 0.0
L_angularAcceleration = 0.1
R_angularAcceleration = 0.0


while True:
    L_angularVelocity += L_angularAcceleration
    L_angle += L_angularVelocity
    R_angularVelocity += R_angularAcceleration
    R_angle += R_angularVelocity
    Main_velocityX += Main_accelerationX
    Main_posX += Main_velocityX
    Main_velocityY += Main_accelerationY
    Main_posY += Main_velocityY

    print(L_angle)
    

