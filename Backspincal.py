
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import math
import pandas as pd


def Back_Spin(Velocity,x0,y0,Theta,Rpm,Res,DeltaT):  
     
    gravity = 9.82#m/s^2
    radius = (0.033)#m
    pi = (3.14)
    #User input from textboxes needed. Calculating spin(rpm/60 * 2pi = (rads))
    velocity_km= Velocity
    velocity = velocity_km/3.6 
    rpm = Rpm
    rps = rpm/60
    spin_rads = rps * (2*3.14)
    v_spin=(spin_rads * radius)
    theta_deg= Theta
    theta =theta_deg*pi/180
    deltaT = DeltaT
    #Lift Coefficient0.2150321215
    Cl = (1/(2.022 + (0.981*(velocity/v_spin))))
    # #Drag Coefficient0.5376334382
    Cd = .508+(1/(22.503+(4.196*((velocity/v_spin)**2.5))**.4))
     
    
    def func_backspin_vy(updated_velocity,new_theta,new_cd,new_cl,new_vx,new_vy):
        
        dv_dt=((0.03568659676*updated_velocity)*((-new_cd*new_vx)-(new_cl*new_vy)))- gravity
        return dv_dt
    def func_backspin_vx(updated_velocity,new_theta,new_cd,new_cl,new_vx,new_vy):
        
        dv_dt=(0.03568659676*updated_velocity)*((-new_cd*new_vx)-(new_cl*new_vy))
        return dv_dt

    def plot(userx,usery,theta,Cd,Cl,v_spin,rpm):
      
      
      x,y=userx,usery
      updated_velocity=velocity
      new_theta=theta
      new_cd=Cd
      new_cl=Cl
      t=deltaT
      vx=velocity*math.cos(theta)
      vy=velocity*math.sin(theta)
      e = Res #needs to be user input as well .75
      new_vx=vx
      new_vy=vy

      data=pd.DataFrame(columns=['x','y','t','Cd','Cl','V','Theta','vx','vy','dvx/dt','dvy/dt'])

      data=data.append({'x':x,'y':y,'t':t,'Cd':new_cd,'Cl':new_cl,'V':updated_velocity,'Theta':new_theta,'vx':new_vx,'vy':new_vy,'dvx/dt':0,'dvy/dt':0},ignore_index=True)
 
      
      
      while y >= 0.033 or (x != 11.885 and y >0.995):
          
          dvx_dt=func_backspin_vx(updated_velocity,new_theta,new_cd,new_cl,new_vx,new_vy)
          dvy_dt=func_backspin_vy(updated_velocity,new_theta,new_cd,new_cl,new_vx,new_vy)
                            
          # vx and vy values
          new_vx=new_vx+dvx_dt*deltaT
          new_vy=new_vy+dvy_dt*deltaT
          # updated theta
          new_theta=math.atan(new_vy/new_vx)
          # updated velocity
          updated_velocity= new_vx/math.cos(new_theta)
                  
          # co-ordinates
          x = x+new_vx* deltaT
          y = y+new_vy* deltaT
          # updated cd and cl
          new_cd=.508+(1/(22.503+(4.196*((updated_velocity/v_spin)**2.5))**.4))
          new_cl=(1/(2.022 + (0.981*(updated_velocity/v_spin))))
                   
          
          data=data.append({'x':x,'y':y,'t':t,'Cd':new_cd,'Cl':new_cl,'V':updated_velocity,'Theta':new_theta,'vx':new_vx,'vy':new_vy,'dvx/dt':dvx_dt,'dvy/dt':dvy_dt},ignore_index=True)
         
          
          
          if data.shape[0]==1:
            t=deltaT
          else:
            t=t+deltaT
      
      while x<= 27:
            #bounce
            rps = rpm/60
            spin_rads = rps * (2*3.14)
            vy = -e * new_vy
            vx = new_vx - ((new_vx- .33*spin_rads)/(1+1/.55)) 
            spin_rads_bounce= spin_rads + ((new_vx - .33 *spin_rads)/(.33*(1+.55)))
            v_spin=(spin_rads_bounce * radius)
            
          
            dvx_dt=func_backspin_vx(updated_velocity,new_theta,new_cd,new_cl,new_vx,new_vy)
            dvy_dt=func_backspin_vy(updated_velocity,new_theta,new_cd,new_cl,new_vx,new_vy)
                  
            
              # vx and vy values
            new_vx=new_vx+dvx_dt*deltaT
            new_vy=new_vy+dvy_dt*deltaT
            # updated theta
            new_theta=math.atan(new_vy/new_vx)
            # updated velocity
            updated_velocity= new_vx/math.cos(new_theta)
                    
            # co-ordinates
            x = x+new_vx* deltaT
            y = y+new_vy* deltaT
            # updated cd and cl
            new_cd=.508+(1/(22.503+(4.196*((updated_velocity/v_spin)**2.5))**.4))
            new_cl=(1/(2.022 + (0.981*(updated_velocity/v_spin))))
              
          
            y1=abs(y)
            if(y1>0 and y1<10):
              data=data.append({'x':x,'y':y1,'t':t,'Cd':new_cd,'Cl':new_cl,'V':updated_velocity,'Theta':new_theta,'vx':new_vx,'vy':new_vy,'dvx/dt':dvx_dt,'dvy/dt':dvy_dt},ignore_index=True)
            else:
              break
            t=t+deltaT

      return data
    
    userx = x0#26.83127295
    usery = y0#7.18941792
    df=plot(userx,usery,theta,Cd,Cl,v_spin,rpm)
    df
    df.to_csv('Backspindata.csv',encoding = 'utf-8-sig')