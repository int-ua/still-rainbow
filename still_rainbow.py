# coding=utf-8
'''
Still Rainbow - programmable tool for making colorful "light painting"
with your smartphone and photocamera.
Copyright (C) 2009-2010 Serhiy Zagoriya (Сергій Загорія) (int_ua)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

Full licence text can be found at
http://www.gnu.org/licences/gpl-3.0.html
'''
__name__='Still Rainbow S60 '
__version__='0.96'
__site__='http://code.google.com/p/still-rainbow'
__author__='Serhiy Zagoriya (int_ua)'
__copyright__ = "Copyright 2009-2010, Serhiy Zagoriya"
__license__ = "GPLv3"
__email__ = "xintx.ua@gmail.com"
# todo: i18n, scenario linking to other scenario, bookmark color

import appuifw
try:
 import e32,sysinfo,os
 from graphics import Image
except:
 appuifw.note(u'failed to\n import e32,sysinfo,os,graphics','error')

img=Image.new(sysinfo.display_pixels(),'RGB')
appuifw.app.screen='full'
appuifw.app.orientation='portrait'

#home=u'e:\\Python\\sr_files\\'
home=os.path.splitdrive(appuifw.app.full_name())[0]+u'private\\e6c858ac\\'
homecsv=home+u'csv\\'

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

keyshot={
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
codes={48: '0', 49: '1', 1: 'c', 42: '*', 167: 'ok', 14: 'left', 15: 'right', 16: 'up', 17: 'down', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 127: '#', 18: 'pen', 196: 'green',180:'menu',226:'camera'}

def keypress_handler(pressed):
 if not(img): return 0
 if pressed['type']==1:
  eval(keyshot[codes[pressed['scancode']]])() # виконати команду з масиву keyshot

def do_nothing(): # бо у масиві keyshot має бути назва функції. Див. keypress_handler()
 pass

def white():
 global color
 color=[255,255,255]
 rect(color) # тут і далі - оновити зображення. Якщо розмістити у keypress_handler(), то були проблеми з global color.

def black():
 global color
 color=[0,0,0]
 rect(color)

def velocity_inc():
 global velocity
 velocity+=(velocity/abs(velocity)) # для врахування поточного напряму руху
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

def channel_minus(): # зменшити значення каналу кольору під вказівником
 global color
 color[color_channel]=limit(color[color_channel]-custom_accuracy)
 rect(color)

def channel_plus(): # збільшити значення каналу кольору під вказівником
 global color
 color[color_channel]=limit(color[color_channel]+custom_accuracy)
 rect(color)

def channel_right(): # перемістити вказівник правіше
 global color_channel
 color_channel+=(1,-2)[color_channel>1]
 rect(color)

def channel_left(): # перемістити вказівник лівіше
 global color_channel
 color_channel+=(-1,2)[color_channel<1]
 rect(color)

def direct_input():
 input_int()
 input_hex()

def input_int(): # ввести десяткові значення
 global color
 for i in range(3):
  color[i]=limit(appuifw.query(u'color direct input: '+str(('Rgb','rGb','rgB')[i]),'number',color[i]))

def input_hex(): # ввести шістнадцяткове значення (т. зв. RGB)
 global color
 col_hex=''
 for i in range(3):
  col_hex+=t(str(('',0)[color[i]<16])+str(hex(color[i]).split('x')[1])) # конвертувати поточне значення, доповнюючи нулями де треба
 col_hex=appuifw.query(u'color direct input: new hex value','text',col_hex)
 if col_hex!=None: # якщо введення не було скасовано
  col_hex+='0'*(6-len(list(col_hex))) # Доповнити нулями до 6 символів
  for i in range(3):
   color[i]=limit(int(str(list(col_hex)[i*2])+str(list(col_hex)[i*2+1]),16)) # зчитати у десяткові значення поточного кольору
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
 screen_height=sysinfo.display_pixels()[1]
# screen_width=sysinfo.display_pixels()[0] # може колись доведеться робити і для горизонтального розташування
# screen_height=128+font_height*6 # компактне відображення інформації
 left=screen_height-font_height*6 # скільки лишилось для графічного відображення каналів кольору
 screen_height_coef=(left/256.0,divmod(left,256)[0])[left>256] # скільки разів на області для відображення поміститься 256 пікселів
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
 to_white=1 # запит до функції draw3() перейти до білого

def rect(col=color): # оновити екран включно з інформаційною панеллю
 img.clear(tuple(col))
 if showing_info:
  img.rectangle((0,0,info_width*3,screen_height),fill=(0,0,0)) # чорний фон під панель
  for i in range(3):
   col_hex=hex(col[i]).split('x')[1]
   col_hex='0'*(2-len(col_hex))+col_hex
   fill_untupled=[0,0,0]
   fill_untupled[i]=255
   fill=tuple(fill_untupled)
# графічне відображення каналів
   img.rectangle((info_width*i,screen_height-color_height+1,(i+1)*info_width,1+screen_height-color_height+int(col[i]*screen_height_coef)),fill=fill)
# десяткові значення
   img.text((0,(i+1)*font_height),t(str(col[i])),fill,(None,font_height))
# шістнадцяткові значення
   img.text((i*(font_height+1),4*font_height),t(col_hex),fill,(None,font_height))
# точність [джойстика]
  img.text((0,5*font_height),t(str(custom_accuracy)),0xffffff,(None,font_height))
# швидкість, пауза, очікування (зі сценарію)
  img.text((0,6*font_height),t(str(abs(velocity))+str((u'',u'p')[paused])+str((u'',u'w'+str(wait))[wait>0])),0xface0D,(None,font_height))
# білий вказівник активного каналу
  img.rectangle((color_channel*info_width,screen_height-color_height,color_channel*info_width+info_width,screen_height-color_height+1),fill=0xffffff)
 canvas.blit(img) # записати зміни на "полотно": вивести на екран

def limit(col,gap=(0,255)):
 return (gap[0],(col,gap[1])[col>gap[1]])[col>gap[0]] # повернути найближчу до заданої (col) точку з відрізка gap

def draw(): # виводить по черзі усі яскраві кольри
 global velocity,running;
 running=not(running)
 while running:
  for i in range(3):
   while color[i] != ( 255*(1+(velocity/abs(velocity)))/2 ): # автоматичне визначення цільового значення залежно від напряму зміни
    e32.ao_yield() # тут і далі - оновити глобальні змінні. Якось так.
    if running==0: return
    color[i]=limit(color[i]+velocity)
    rect(color)
    while paused:
     e32.ao_sleep(0.1)
     e32.ao_yield()
     if running==0: return
   velocity=-velocity # обернути напрям руху після досягнення цільового значення

def pause():
 global paused
 paused=not(paused)
 rect(color)

def draw2(): # яскраві кольори + фіксоване положення білого у циклі
 global velocity,running
 running=not(running)
 while running:
  for o in range(4): # щоб додавати перехід до білого
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
    if o==2: # перехід до білого
     velocity=abs(velocity)

def draw3(): # яскраві кольори з переходом на білий за сигналом користувача
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
   if color==[255,255,255]: to_white=0 # якщо колір вже білий, скинути позначку запиту
   velocity=-velocity
   if to_white==1: # якщо присутній запит, переходити до білого
    velocity=abs(velocity)

# 2.0 - все, що пов’язано зі сценаріями (крім виведення інформації через rect() )
wait=0

def check(filepath,mode='r'): # перевірка доступу до файлу [для зчитування]
 if not(filepath) or filepath=='None': return -1 # введення скасовано
 try:
  file=open(filepath,mode)
  file.close()
  return 1
 except:
  appuifw.note(u'error opening file:'+str(filepath)+u' in '+{'r':'read','a':'append','w':'write'}[mode]+u' mode','error')
  return 0

def new_scenario():
 return str(appuifw.query(u'new scenario name:','text',u'new.csv'))

def select_scenario(creation=0):
 try:
  scenario_list=map(unicode,os.listdir(homecsv))
 except:
  appuifw.note(u'cannot list dir '+str(homecsv),'error')
 if creation: scenario_list.append(u' + create new?')
 selected=appuifw.selection_list(scenario_list)
 if selected==None: return #cancel
 if creation and selected==len(scenario_list)-1:
  return new_scenario()
 return scenario_list[selected]

def draw_scenario():
 global running,color,wait
 target=[0,0,0]
 v=[0,0,0] #velocities

 scenario_name=select_scenario() # вибір сценарію
 if scenario_name==None: return
 scenario_path=homecsv+scenario_name
 if check(scenario_path)<1: return # якщо файл недоступний

 file=open(scenario_path,'r')
 line_counter=0
 running=1
 while running:
  line="None"
  if line == "": running=0 # пустий рядок матиме "\n", а пуста змінна означає кінець файлу
  while line != "":
   line=file.readline()
   line_counter+=1
   if line=="": # знаю, що занадто багато перевірок цього рядка. Можеш спробувати прибрати якусь, потестувати і повідомити (!) про результати ;)
    file.close()
    appuifw.note(u'scenario '+str(scenario_name)+u' finished','conf')
    return
   if line[0]=="#" or len(line)<13: break # пропустити коментарі. Мінімальна довжина рядка, що міститиме повну інформацію відвовідно до формату - 13 символів: 0,0,0,0,0,0,0
   try:
    line=str(line).split(',')
    for i in range(3):
     target[i]=limit(int(line[i+3])) # цільові значення каналів, обмежені відрізком [0,255]
     v[i]=abs((velocity,int(line[i]))[int(line[i])!=0])*cmp(target[i],color[i]) # значення швидкості і автоматичне визначення напряму руху
    wait=abs(float(line[6]))
   except:
    break

   while color != target: # потребує додаткових тестів з одночасною ручною зміною кольору (джойстиком) і ідей щодо обробки таких подій
    for i in range(3):
     gap=((color[i],target[i]),(target[i],color[i]))[color[i]>target[i]] # перетворення цільового кольору у відрізок обмеження для limit()
     color[i]=limit(color[i]+v[i],gap)
     e32.ao_yield()
     if running==0: file.close(); return
    rect(color)

    while paused:
     e32.ao_sleep(0.1)
     e32.ao_yield()
     if running==0: file.close(); return

   while wait>0:
    e32.ao_sleep(0.1)
    wait=round(wait-0.1,1) # точність - десята секунди
    if wait<=0: wait=0
    rect(color)
    e32.ao_yield()
    if running==0: return

def write_scenario():
 scenario_to_write=select_scenario(1)
 if scenario_to_write==None: return
 scenario_to_write=homecsv+scenario_to_write
 if check(scenario_to_write,'a')<1: return 0 # якщо файл недоступний для додавання даних (читати "для запису")
 file=open(scenario_to_write,'a')
 line=u'\r\n'
 for i in range(3):
  velocity_input=appuifw.query(u'velocity #'+str(i)+u' (0=adaptive)','number',velocity)
  if velocity_input==None: return # введення скасовано
  line+=str(limit(velocity_input))+u',' # введення швидкостей
 for i in range(3):
  line+=str(color[i])+u',' # колір зчитується з поточного
 wait_input=appuifw.query(u'wait (seconds):','float')
 if wait_input==None: return
 line+=str(round(float(wait_input),1))
 file.write(line)
 file.close()

def export_scenario():
 export_from=homecsv+select_scenario()
 export_to=appuifw.query(u'export to:','text',os.path.splitdrive(appuifw.app.full_name())[0]+u'export.csv')
 if check(export_to,'w')==1:
  e32.file_copy(export_to,export_from)

def import_scenario():
 import_from=appuifw.query(u'import to:','text',os.path.splitdrive(appuifw.app.full_name())[0]+u'import.csv')
 if check(import_from,'r')==1:
  e32.file_copy(homecsv+os.path.split(import_from)[1],import_from)

def remove_scenario():
 deletion=select_scenario()
 if deletion==None: return
 deletion=homecsv+deletion
 try:
  os.remove(deletion)
 except:
  appuifw.note(u'Unable to remove '+str(deletion),'error')
 remove_scenario()

# 2.0 end

def t(s): return s.decode('utf-8')

def text_message(message=''):
 stop()
 text=appuifw.Text()
 text.font=(None,font_height)
 appuifw.app.menu=[(u'<',unhelp)]
 appuifw.app.exit_key_handler=unhelp
 appuifw.app.body=text
 text.set(t(message))
 text.set_pos(0)

def unhelp():
 appuifw.app.body=canvas
 appuifw.app.menu=menu
 appuifw.app.exit_key_handler=exit

def help_u():
 text_message(__name__+__version__+'\n'+__site__+'\n\nПрограма для кольорового \"малювання світлом\" (вночі за допомогою фотоапарата з контролем витримки)\nале може також стати у нагоді для відображення чи вибору будь-якого кольору як у шістнадцяткових (hex), так і в десяткових значеннях RGB\nАбо для гіпнотизування друзів ;)\n\nЛiцензiя: GPLv3\nhttp://www.gnu.org/licences/gpl-3.0.html\n\n(c) Сергiй Загорiя (int_ua) 2009-2010\n( xintx.ua@gmail.com )\n\n\nЯкщо Ви оцiнили мої старання, Ви можете пiдтримати мене повiдомленням або (хоча б) грошима:\nPayPal(^) або Webmoney:\nU215842819919\nZ327603499116\nE243558295191\n:)\n\n\nПро проблеми можна повідомити тут:\n'+__site__+'/issues')

def help_r():
 text_message(__name__+__version__+'\n'+__site__+'\n\nПрограмма для цветного \"рисования светом\" (ночью при помощи фотоаппарата с контролем выдержки)\nно может также пригодиться для отображения или выбора любого цвета как в шестнадцатеричных (hex), так и в десятичных значениях RGB\nИли для гипнотизирования друзей ;)\n\nЛицензия: GPLv3\nhttp://www.gnu.org/licences/gpl-3.0.html\n\n(c) Сергей Загория (int_ua) 2009-2010\n( xintx.ua@gmail.com )\n\n\nЕсли Вы оценили мои старания, Вы можете поддержать меня сообщением или (хотя бы) деньгами:\nPayPal(^) или Webmoney:\nR309038080035\nZ327603499116\nE243558295191\n:)\n\n\nО проблемах можно сообщить здесь:\n'+__site__+'/issues')

def help_e():
 text_message(__name__+__version__+'\n'+__site__+'\n\nProgram is designed for making colorful \"light painting\" with your smartphone and photocamera.\nBut it can be used also for easy viewing and selecting colors with their hex or integer values.\nOr for hypnotizing your friends ;)\n\nLicence: GPLv3\nhttp://www.gnu.org/licences/gpl-3.0.html\n\n(c) Serhiy Zagoriya aka int_ua 2009-2010\n( xintx.ua@gmail.com )\n\n\nIf you appreciate my efforts, you can support me by emailing or (at least) donating:\nPayPal(^) or Webmoney:\nZ327603499116\nE243558295191\n:)\n\n\nYou can report issues here:\n'+__site__+'/issues')

def img_hotkeys():
 appuifw.Content_handler().open(home+'hotkeys.png')

def redraw(*args):
 if img:
  canvas.blit(img)

def stop():
 global running
 running=0
 e32.ao_sleep(0.001) # а ти спробуй закоментуй

lock=e32.Ao_lock()
def exit():
 stop()
 lock.signal()
 appuifw.app.set_exit()

hotkeys=dict()
for key,func in keyshot.items():
 hotkeys[func]=key

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
  (u'append current color'+' ('+hotkeys['write_scenario']+')',write_scenario),
  (u'export scenario',export_scenario),
  (u'import scenario',import_scenario),
  (u'remove scenario',remove_scenario))),
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
  (u'hotkeys.png',img_hotkeys),
  (t('Довiдка'),help_u),
  (t('Справка'),help_r),
  (u'help',help_e)))]
''' Із незрозумілих мені причин кількість пунктів меню обмежена 30-ма :( Ну це ще можна було б витерпіти. Але ж exception треба додавати! -2 години.'''

canvas=appuifw.Canvas(event_callback=keypress_handler,redraw_callback=redraw)
unhelp()
rect()
lock.wait()
