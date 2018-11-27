observer_pattern = Observer_Pattern()
hat = Hat(0x40,50)
motion=Motion({'x':0,'y':0,'r':0,'z':0,'cam':0,'light':0})
TCP_OBJ = TCP('127.0.0.1',8082,1000000,[])

hat.add_Device('Left_Front',1,290)
hat.add_Device('Right_Front',2,290)
hat.add_Device('Right_Back',3,290)
hat.add_Device('Left_Back',4,290)
hat.add_Device('Vertical_Right',5,290)
hat.add_Device('Vertical_Left',6,290)
hat.add_Device('Main_Cam',7,450)
hat.add_Device('light',8,0)

motion.SIGNAL_Referance(observer_pattern.emit_Signal)
TCP_OBJ.SIGNAL_Referance(observer_pattern.emit_Signal)

observer_pattern.registerEventListener('PWM',hat.update)
observer_pattern.registerEventListener('TCP',motion.update)
observer_pattern.registerEventListener('TCP_ERROR',motion.update)

TCP_OBJ.main_Loop()

