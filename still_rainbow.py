# coding=utf-8
# Copyright (C) 2009-2010 Serhiy Zagoriya (Сергій Загорія) (int_ua)
# Licence: GPLv3 http://www.gnu.org/licences/gpl-3.0.html
# project is too small to attach full licence text at the moment
__name__='Still Rainbow S60 ' # :)
__version__='0.95'
__author__='Serhiy Zagoriya (int_ua)'
__copyright__ = "Copyright 2009-2010, Serhiy Zagoriya"
__license__ = "GPLv3"
__email__ = "xintx.ua@gmail.com"
__status__ = "experimental"
# future release: i18n, scenario linking to other scenario
# img.open(file) instructions on start?
# appuifw.app.full_name()

import appuifw,e32,sysinfo,os
from graphics import Image
img=Image.new(sysinfo.display_pixels(),'RGB')
appuifw.app.screen='full'
appuifw.app.orientation='portrait'

color=[0,255,0]
velocity=10
custom_accuracy=24
showing_info=1
running=0
paused=0
color_channel=0
to_white=0
font_height=9
info_width=font_height+1

map={
'down': 'channel_plus',
'up': 'channel_minus',
'right': 'channel_right',
'left': 'channel_left',
'ok': 'direct_input',
'1': 'draw',
'4': 'draw2',
'7': 'draw3',
'2': 'draw_scenario',
'5': 'write_scenario',
'8': 'toggle_info',
'3': 'set_accuracy',
'6': 'velocity_inc',
'9': 'velocity_dec',
'0': 'pause',
'*': 'white',
'#': 'black',
'pen': 'draw3_white',
'green': 'do_nothing',
'menu': 'do_nothing',
'camera': 'do_nothing',
'c': 'exit'}

hotkeys=dict()
for key,func in map.items():
 hotkeys[func]=key

codes={48: '0', 49: '1', 1: 'c', 42: '*', 167: 'ok', 14: 'left', 15: 'right', 16: 'up', 17: 'down', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 127: '#', 18: 'pen', 196: 'green',180:'menu',226:'camera'}

def keypress_handler(pressed):
 if not(img): return 0
 if pressed['type']==1:
  eval(map[codes[pressed['scancode']]])()

def do_nothing():
 pass

def white():
 global color
 color=[255,255,255]
 rect(color)

def black():
 global color
 color=[0,0,0]
 rect(color)

def velocity_inc():
 global velocity
 velocity+=(velocity/abs(velocity))
 rect(color)

def velocity_dec():
 global velocity
 if abs(velocity)>1: velocity-=(velocity/abs(velocity))
 rect(color)

def velocity_input():
 global velocity
 velocity=limit(appuifw.query(u'velocity','number',abs(velocity)),(1,255))
 rect(color)

def toggle_info():
 global showing_info
 showing_info=not(showing_info)
 rect(color)

def channel_minus():
 global color
 color[color_channel]=limit(color[color_channel]-custom_accuracy)
 rect(color)

def channel_plus():
 global color
 color[color_channel]=limit(color[color_channel]+custom_accuracy)
 rect(color)

def channel_right():
 global color_channel
 color_channel+=(1,-2)[color_channel>1]
 rect(color)

def channel_left():
 global color_channel
 color_channel+=(-1,2)[color_channel<1]
 rect(color)

def direct_input():
 input_int()
 input_hex()

def input_int():
 global color
 for i in range(3):
  color[i]=limit(appuifw.query(u'color direct input: '+str(('Rgb','rGb','rgB')[i]),'number',color[i]))

def input_hex():
 global color
 col_hex=''
 for i in range(3):
  col_hex+=t(str(('',0)[color[i]<16])+str(hex(color[i]).split('x')[1]))
 col_hex=appuifw.query(u'color direct input: new hex value','text',col_hex)
 if col_hex!=None:
  col_hex+='0'*(6-len(list(col_hex)))
  for i in range(3):
   color[i]=limit(int(str(list(col_hex)[i*2])+str(list(col_hex)[i*2+1]),16))
 rect(color)

def set_accuracy():
 global custom_accuracy
 custom_accuracy=limit(appuifw.query(u'custom accuracy','number',custom_accuracy),(1,255))
 rect(color)

def info_width_input():
 global info_width
 info_width=limit(appuifw.query(u'info width','number',info_width),(1,80))
 rect(color)

def screen_resize():
 global screen_height,color_height,screen_height_coef
# screen_width=sysinfo.display_pixels()[0]
 screen_height=sysinfo.display_pixels()[1]
# screen_height=128+font_height*6 # compact info mode
 left=screen_height-font_height*6
 screen_height_coef=(left/256.0,divmod(left,256)[0])[left>256]
 color_height=int(256*screen_height_coef)
screen_resize()

def font_input():
 global font_height,info_width
 font_height=limit(appuifw.query(u'font height','number',font_height),(1,64))
 info_width=font_height+1
 screen_resize()
 rect(color)

def draw3_white():
 global to_white
 to_white=1

def rect(col=color):
# output color and info
 img.clear(tuple(col))
 if showing_info:
# black info panel background
  img.rectangle((0,0,info_width*3,screen_height),fill=(0,0,0))
  for i in range(3):
   col_hex=hex(col[i]).split('x')[1]
   col_hex='0'*(2-len(col_hex))+col_hex
   fill_untupled=[0,0,0]
   fill_untupled[i]=255
   fill=tuple(fill_untupled)
# graphic channels
   img.rectangle((info_width*i,screen_height-color_height+1,(i+1)*info_width,1+screen_height-color_height+int(col[i]*screen_height_coef)),fill=fill)
# int rgb
   img.text((0,(i+1)*font_height),t(str(col[i])),fill,(None,font_height))
# hex rgb
   img.text((i*(font_height+1),4*font_height),t(col_hex),fill,(None,font_height))
# custom accuracy
  img.text((0,5*font_height),t(str(custom_accuracy)),0xffffff,(None,font_height))
# velocity (+pause,wait)
  img.text((0,6*font_height),t(str(abs(velocity))+str((u'',u'p')[paused])+str((u'',u'w'+str(wait))[wait>0])),0xface0D,(None,font_height))
# white color channel marker
  img.rectangle((color_channel*info_width,screen_height-color_height,color_channel*info_width+info_width,screen_height-color_height+1),fill=0xffffff)
 canvas.blit(img)

def limit(col,gap=(0,255)):
 return (gap[0],(col,gap[1])[col>gap[1]])[col>gap[0]]

def draw():
# initial idea, cycles all bright colors smoothly
 global velocity,running;
 running=not(running)
 while running: #
  for i in range(3): #
   while color[i] != ( 255*(1+(velocity/abs(velocity)))/2 ): #
    e32.ao_yield()
    if running==0: return
    color[i]=limit(color[i]+velocity) #
    rect(color) #
    while paused:
     e32.ao_sleep(0.1)
     e32.ao_yield()
     if running==0: return
   velocity=-velocity #

def pause():
 global paused
 paused=not(paused)
 rect(color)

def draw2():
# bright colors + white
 global velocity,running
 running=not(running)
 while running:
  for o in range(4):
   for i in range(3):
    while color[i] != (255*(1+(velocity/abs(velocity)))/2):
     color[i]=limit(color[i]+velocity)
     e32.ao_yield()
     if running==0: return
     rect(color)
     while paused:
      e32.ao_sleep(0.1)
      e32.ao_yield()
      if running==0: return
    velocity=-velocity
    if o==2:
     velocity=abs(velocity)

def draw3():
# bright colors with white on manual signal
 global velocity,running,to_white
 running=not(running)
 while running:
  for i in range(3):
   while color[i] != (255*(1+(velocity/abs(velocity)))/2):
    color[i]=limit(color[i]+velocity)
    e32.ao_yield()
    if running==0: return
    rect(color)
    while paused:
     e32.ao_sleep(0.1)
     e32.ao_yield()
     if running==0: return
   if color==[255,255,255]: to_white=0
   velocity=-velocity
   if to_white==1:
    velocity=abs(velocity)

# 2.0 begin

def input_scenario(default):
 return str(appuifw.query(u'file with scenario:','text',default))

def check(filepath,mode='r'):
 if not(filepath) or filepath=='None': return -1 #cancel
 try:
  file=open(filepath,mode)
  file.close()
  return 1
 except:
  appuifw.note(u'error opening file:'+str(filepath)+u' in '+{'r':'read','a':'append','w':'write'}[mode]+u' mode')
  return 0

wait=0

def draw_scenario():
 global running,color,wait
 target=[0,0,0]
 v=[0,0,0] #velocities
#input
 scenario_path=input_scenario(u'e:\\Python\\scenario_read.csv')
 if check(scenario_path)<1: return
#read
 file=open(scenario_path,'r')
 line_counter=0
 running=1
 while running:
  line="None"
  if line == "": running=0
  while line != "":
   line=file.readline()
   line_counter+=1
   if line=="":
    file.close()
    appuifw.note(u'scenario '+str(scenario_path)+u' finished')
    return
   if line[0]=="#" or len(line)<13: break
   try:
    line=str(line).split(',')
    for i in range(3):
     target[i]=limit(int(line[i+3]))
     v[i]=abs((velocity,int(line[i]))[int(line[i])!=0])*cmp(target[i],color[i])
    wait=abs(float(line[6]))
   except:
    break
#draw
   while color != target:
    for i in range(3):
     gap=((color[i],target[i]),(target[i],color[i]))[color[i]>target[i]]
     color[i]=limit(color[i]+v[i],gap)
     e32.ao_yield()
     if running==0: file.close(); return
    rect(color)
#pause
    while paused:
     e32.ao_sleep(0.1)
     e32.ao_yield()
     if running==0: file.close(); return
#wait
   while wait>0:
    e32.ao_sleep(0.1)
    wait=round(wait-0.1,1)
    if wait<=0: wait=0
    rect(color)
    e32.ao_yield()
    if running==0: return

scenario_to_write=None

def new_scenario():
 global scenario_to_write
 scenario_to_write=input_scenario(u'e:\\Python\\scenario_write.csv')

def write_scenario():
 if not(scenario_to_write):
  new_scenario()
 else:
  (do_nothing,new_scenario)[appuifw.selection_list([str(scenario_to_write)+u'',u'other scenario'])]()
 if check(scenario_to_write,'a')<1: return 0
 file=open(scenario_to_write,'a')
 line=u'\r\n'
 for i in range(3):
  line+=str(limit(appuifw.query(u'velocity #'+str(i),'number',velocity)))+u','
 for i in range(3):
  line+=str(color[i])+u','
 line+=str(round(float(appuifw.query(u'wait (seconds):','float')),1))
 file.write(line)
 file.close()

# 2.0 end

def t(s): return s.decode('utf-8')

def help():
 text=appuifw.Text()
 text.font=(None,font_height)
 appuifw.app.body=text
 stop()
 text.set(t(instruction))
 text.set_pos(0)
 appuifw.app.menu=[(u'<',unhelp)]

def unhelp():
 appuifw.app.body=canvas
 appuifw.app.menu=menu

def help_u():
 global instruction
 instruction=__name__+__version__+'\n\nПрограма для кольорового \"малювання світлом\" (вночі за допомогою фотоапарата з контролем витримки)\nале може також стати у нагоді для відображення чи вибору будь-якого кольору як у шістнадцяткових (hex), так і в десяткових значеннях RGB\nАбо для гіпнотизування друзів ;)\n\nЛiцензiя: GPLv3\nhttp://www.gnu.org/licences/gpl-3.0.html\n\n(c) Сергiй Загорiя (int_ua) 2009-2010\n( xintx.ua@gmail.com )\n\n\nЯкщо Ви оцiнили мої старання, Ви можете пiдтримати мене повiдомленням або (хоча б) грошима:\nPayPal(^) або Webmoney:\nU215842819919\nZ327603499116\nE243558295191\n:)'
 help()

def help_r():
 global instruction
 instruction=__name__+__version__+'\n\nПрограмма для цветного \"рисования светом\" (ночью при помощи фотоаппарата с контролем выдержки)\nно может также пригодиться для отображения или выбора любого цвета как в шестнадцатеричных (hex), так и в десятичных значениях RGB\nИли для гипнотизирования друзей ;)\n\nЛицензия: GPLv3\nhttp://www.gnu.org/licences/gpl-3.0.html\n\n(c) Сергей Загория (int_ua) 2009-2010\n( xintx.ua@gmail.com )\n\n\nЕсли Вы оценили мои старания, Вы можете поддержать меня сообщением или (хотя бы) деньгами:\nPayPal(^) или Webmoney:\nR309038080035\nZ327603499116\nE243558295191\n:)'
 help()

def help_e():
 global instruction
 instruction=__name__+__version__+'\n\nProgram is designed for making colorful \"light painting\" with your smartphone and some camera.\nBut it can be used also for easy viewing and selecting colors with their hex or integer values.\nOr for hypnotizing your friends ;)\n\nLicence: GPLv3\nhttp://www.gnu.org/licences/gpl-3.0.html\n\n(c) Serhiy Zagoriya aka int_ua 2009-2010\n( xintx.ua@gmail.com )\n\n\nIf you appreciate my efforts, you can support me by emailing or (at least) donating:\nPayPal(^) or Webmoney:\nZ327603499116\nE243558295191\n:)'
 help()

def raw_hotkeys():
 global instruction
 instruction=''
 for key,func in map.items():
  instruction+=str(key)+str(u' ')*(15-len(key))+str(func)+'\n'
 help()

def redraw(*args):
 if img:
  canvas.blit(img)

def stop():
 global running
 running=0
 e32.ao_sleep(0.001)

lock=e32.Ao_lock()
def exit():
 stop()
 lock.signal()
 appuifw.app.set_exit()

menu=[
 (u'draw',(
  (u'bright'+' ('+hotkeys['draw']+')',draw),
  (u'  (un)pause'+' ('+hotkeys['pause']+')',pause),
  (u'bright+white'+' ('+hotkeys['draw2']+')',draw2),
  (u'bright+white on click'+' ('+hotkeys['draw3']+')',draw3),
  (u'white click'+' ('+hotkeys['draw3_white']+')',draw3_white),
  (u'black'+' ('+hotkeys['black']+')',black),
  (u'white'+' ('+hotkeys['white']+')',white))),
 (u'scenario',(
  (u'draw scenario'+' ('+hotkeys['draw_scenario']+')',draw_scenario),
  (u'write current color',write_scenario))),
 (u'set',(
  (u'color'+' ('+hotkeys['direct_input']+')',direct_input),
  (u'   in hex',input_hex),
  (u'   in int',input_int),
  (u'velocity',velocity_input),
  (u'joystick accuracy'+' ('+hotkeys['set_accuracy']+')',set_accuracy),
  (u'info visibitity'+' ('+hotkeys['toggle_info']+')',toggle_info),
  (u'font height',font_input),
  (u'info width',info_width_input),
  (u'increase velocity'+' ('+hotkeys['velocity_inc']+')',velocity_inc),
  (u'decrease velocity'+' ('+hotkeys['velocity_dec']+')',velocity_dec))),
 (u'?',(
  (t('Довiдка'),help_u),
  (t('Справка'),help_r),
  (u'Help',help_e),
  (u'raw_hotkeys()',raw_hotkeys))),
 (u'X',exit)]

canvas=appuifw.Canvas(event_callback=keypress_handler,redraw_callback=redraw)
appuifw.app.body=canvas
appuifw.app.menu=menu
appuifw.app.exit_key_handler=exit
rect()
lock.wait()
