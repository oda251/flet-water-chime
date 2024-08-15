import os
import time
import datetime
from enum import Enum
import flet as ft
import random
import threading
from playsound import playsound

os.chdir(os.path.dirname(__file__))

alarm_minites = [0, 57, 40]
image_sea = ['sea_1.jpg', 'sea_2.jpg', 'sea_3.jpg']

class ChimeSound(Enum):
  # https://soundeffect-lab.info/sound/environment/
  KAMOME = 'https://soundeffect-lab.info/sound/environment/mp3/beach-seagull1.mp3'
  # https://otologic.jp/free/se/school_bell01.html
  SCHOOL_CHIME = 'https://otologic.jp/sounds/se/pre/Japanese_School_Bell02-02(Slow-Mid).mp3'
  # https://soundeffect-lab.info/sound/button/
  CLICK = 'https://soundeffect-lab.info/sound/button/mp3/cursor1.mp3'
  def __str__(self):
    return self.value

class IconButtonWithSound(ft.Column):
  def __init__(self, icon, selected_icon, on_click=None, sound=None):
    super().__init__()
    def handle_click(_):
      self.button.selected = not self.button.selected
      if on_click:
        on_click()
      if self.button.selected:
        threading.Thread(target=playsound, args=(sound,)).start()
    self.button = ft.IconButton(
      icon=icon,
      selected_icon=selected_icon,
      selected=True,
      on_click=handle_click,
    )
    self.audio = ft.Audio(
      src=sound,
      autoplay=False,
      volume=1,
      balance=0,
    )
    self.controls = [
      self.button,
      self.audio,
    ]
  
class Clock(ft.Text):
  def __init__(self, on_alarm):
    super().__init__()
    self.value = datetime.datetime.now().time().replace(microsecond=0)
    self.color = "lightgray"
    self.weight = "bold"
    self.size = 40
    self.alarm_is_on = True
    self.on_alarm = on_alarm
  def update_time(self):
    while True:
      time.sleep(1)
      self.value = datetime.datetime.now().time().replace(microsecond=0)
      # if self.alarm_is_on and self.value.minute in alarm_minites and self.value.second == 0:
      if self.value.second == 0:
        self.on_alarm()
      self.update()
  def start_clock(self):
    self.update_time()

class AlarmClock(ft.Column):
  def __init__(self, on_alarm):
    super().__init__()
    def handle_alarm():
      on_alarm()
      threading.Thread(target=playsound, args=(ChimeSound.SCHOOL_CHIME,)).start()
    self.clock = Clock(handle_alarm)
    self.alarm_switch_btn = IconButtonWithSound(
      icon=ft.icons.NOTIFICATIONS_PAUSED_OUTLINED,
      selected_icon=ft.icons.NOTIFICATIONS_ON,
      sound=ChimeSound.CLICK,
      on_click=self.toggle_alarm,
    )
    self.controls = [
        self.clock,
        self.alarm_switch_btn,
      ]
    self.alignment = ft.MainAxisAlignment.CENTER
    self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    self.bgcolor = ft.colors.BLACK
    self.height = 500
    self.width = 700
  def did_mount(self):
    self.clock.start_clock()
  def toggle_alarm(self):
    self.clock.alarm_is_on = self.alarm_switch_btn.button.selected
    self.update()

class Notifier(ft.Stack):
  def __init__(self, message):
    super().__init__()
    self.image = ft.Image(
      src=random.choice(image_sea),
      fit=ft.ImageFit.FILL,
      expand=True,
    )
    self.message = ft.Text(
      value=message,
      color=ft.colors.WHITE,
      size=20,
      weight="bold",
    )
    self.button = ft.FilledButton(
      text="OK",
      on_click=lambda e: self.close(e),
    )
    self.notification = ft.Column(
      controls=[
        self.message,
        self.button,
      ],
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    self.controls = [
        self.image,
        self.notification,
      ]
    self.bgcolor = ft.colors.BLACK
    self.expand = True
    self.alignment = ft.alignment.center
    self.isolated = True
    # 初回起動時は非表示
    self.visible = False
  def close(self, _):
    self.visible = False
    self.update()

class AlarmApp(ft.Stack):
  def __init__(self):
    super().__init__()
    self.clock = AlarmClock(self.on_alarm)
    self.expand = True
    self.notifier = Notifier("Time to drink water!")
    self.controls = [
        self.clock,
        self.notifier,
      ]
  def on_alarm(self):
    self.notifier.visible = True
    self.page.window.to_front()
    self.page.window.center()
    self.notifier.update()
    self.update()

def main(page: ft.Page):
  page.padding=0
  page.window.height=500
  page.window.width=700
  page.add(AlarmApp())

ft.app(target=main)