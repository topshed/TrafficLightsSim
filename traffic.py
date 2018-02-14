# Full crossing simulator
#  Two Pi-Top trafic lights
#  Two RGB LEDs - The Green (or red) Man or Walk/Don't Walk
#  Two push buttons
#  A buzzer
#
# This code simulates the operation of taffic light controlled crossing
# Normal traffic light sequence: 
# 1) red
# 2) red + amber
# 3) green
#
# Traffic will pass with walk/don't walk light red until button is pressed.  Then
# stopping sequence will activate:
#
# 1) green
# 2) amber
# 3) red
#
# Walk/don't walk will turn green (green man) and buzzer will beep. When buzzer stops,  green
# man will blink until traffic light sequence (red -> green) restarts, when walk/don't walk turns
# back to red.
# If button is pressed againwithin 10 seconds, crossing will not activate imediately, but wait
# until 10 seconds since last crossing has elapsed 

from gpiozero import Button, Buzzer, LED, RGBLED
from time import sleep

# Pi-Stop Traffic lights
l1_red = LED(21)
l1_amber = LED(20)
l1_green = LED(16)
l2_red = LED(26)
l2_amber = LED(19)
l2_green = LED(13)
# Buttons
b1 = Button(14)
b2 = Button(15)
# Walk/don't walk indicator
m1 = RGBLED(11,9,10)
m2 = RGBLED(7,8,25)
# buzzer
bz = Buzzer(17)

time_since_last_red = 0

def stop_go_seq(): # Traffic lights change from red to green 
   print("Going sequence")
   global time_since_last_red
   l1_amber.off()
   l1_green.off()
   l1_red.on()
   l2_amber.off()
   l2_green.off()
   l2_red.on()
   sleep(1)
   l1_amber.on()
   l1_green.off()
   l1_red.on()
   l2_amber.on()
   l2_green.off()
   l2_red.on()
   sleep(2)
   l1_amber.off()
   l1_green.on()
   l1_red.off()
   l2_amber.off()
   l2_green.on()
   l2_red.off()
   time_since_last_red = 0 # reset time since last crossing 
   
def go_stop_seq(): # Traffic lights change from green to red 
   print("Stoppng sequence")
   l1_amber.off()
   l1_green.on()
   l1_red.off()
   l2_amber.off()
   l2_green.on()
   l2_red.off()
   sleep(1)
   l1_amber.on()
   l1_green.off()
   l1_red.off()
   l2_amber.on()
   l2_green.off()
   l2_red.off()
   sleep(2)
   l1_amber.off()
   l1_green.off()
   l1_red.on()
   l2_amber.off()
   l2_green.off()
   l2_red.on()



def button_pressed():
   print("Button Pressed")
   global time_since_last_red
   if time_since_last_red < 10: # check how long since the button was last pressed
       hold = 10 - time_since_last_red
       print("waiting " + str(hold) + " seconds")
       sleep(10 - time_since_last_red)
   go_stop_seq() # stop traffic - turn lights to red
   sleep(1)
   m1.color = (0,1,0) # walk/don't walk to green
   m2.color = (0,1,0)
   bz.beep(0.2,0.2, n = 13 ) # crossing beep
   sleep(5)
   # green man flashes
   m1.blink(off_time = 0.8, on_time = 0.8, on_color = (0,1,0), off_color = (0,0,0), n=5, background = True)
   m2.blink(off_time = 0.8, on_time = 0.8, on_color = (0,1,0), off_color = (0,0,0), n=5, background = False)
   m1.color = (1,0,0) # the turns back to red
   m2.color = (1,0,0)
   stop_go_seq()
   
# set function to be run when either button is pressed
b1.when_pressed = button_pressed
b2.when_pressed = button_pressed

m1.color = (1,0,0) # walk/don't walk to red
m2.color = (1,0,0) # walk/don't walk to red
stop_go_seq()
while True:
    if l1_green.value == True: # Are the traffic lights green?
        time_since_last_red+=1 # Count how long since they were last red
        print(time_since_last_red)
        sleep(1)

        
