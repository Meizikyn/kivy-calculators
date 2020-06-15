#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout

class EventHandler(object):
  def __init__(self, dgt=lambda x: None, op=lambda x: None, eq=lambda: None, clear=lambda: None):
    self.call = {'dgt': dgt, 'op': op, 'eq': eq, 'clear': clear}

class Calculator(BoxLayout):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.orientation='vertical'


    self.display = Label(size_hint=(1,0.2), font_size='16', halign='right')
    self.l       = Label()
    self.r       = Label()
    self.op      = ''
    self.buffer  = self.l
    self.state   = 'clear'

    parse = self.parse
    clear = self.clear
    advance = self.advance
    replace_op = self.replace_op
    insert_dgt = self.insert_dgt
    replace_dgt = self.replace_dgt
    set_buffer_left = self.set_buffer_left
    set_buffer_right = self.set_buffer_right

    self.fsm = {
      'clear': EventHandler(
        eq    = lambda x: [parse(), advance('post')],
        clear = lambda x: [clear(), advance('clear'), set_buffer_left()],
        dgt   = lambda x: [replace_dgt(x), advance('left')]
      ),
      'left': EventHandler(
        eq    = lambda x: [parse(), advance('post')],
        clear = lambda x: [clear(), advance('clear'), set_buffer_left()],
        dgt   = lambda x: insert_dgt(x),
        op    = lambda x: [replace_op(x), advance('hold'), set_buffer_right()]
      ),
      'hold': EventHandler(
        eq    = lambda x: [parse(), advance('post')],
        clear = lambda x: [clear(), advance('clear'), set_buffer_left()],
        dgt   = lambda x: [replace_dgt(x), advance('right')],
        op    = lambda x: replace_op(x)
      ),
      'right': EventHandler(
        eq    = lambda x: [parse(), advance('post')],
        clear = lambda x: [clear(), advance('clear'), set_buffer_left()],
        dgt   = lambda x: insert_dgt(x),
        op    = lambda x: [parse(), replace_op(x), advance('hold')]
      ),
      'post': EventHandler(
        eq    = lambda x: parse(),
        clear = lambda x: [clear(), advance('clear'), set_buffer_left()],
        dgt   = lambda x: [replace_dgt(x), advance('left'), set_buffer_left()],
        op    = lambda x: [replace_op(x), advance('hold')]
      )
    }

    self.display.text = '0'

    inputs = [
      ['7',   'dgt'],
      ['8',   'dgt'],
      ['9',   'dgt'],
      ['/',    'op'],
      ['4',   'dgt'],
      ['5',   'dgt'],
      ['6',   'dgt'],
      ['*',    'op'],
      ['1',   'dgt'],
      ['2',   'dgt'],
      ['3',   'dgt'],
      ['-',    'op'],
      ['C', 'clear'],
      ['0',   'dgt'],
      ['=',    'eq'],
      ['+',    'op'],
    ]
    pad = GridLayout()
    pad.cols = 4
    for input in inputs:
      button = Button(text=input[0])
      button.event = input[1]
      button.bind(on_press=self.hook)
      pad.add_widget(button)

    self.add_widget(self.display)
    self.add_widget(pad)

  def hook(self, btn):
    self.fsm[self.state].call[btn.event](btn.text)

  def set_buffer_left(self):
    self.buffer = self.l

  def set_buffer_right(self):
    self.buffer = self.r

  def replace_dgt(self, val):
    self.buffer.text = val
    self.display.text = self.buffer.text

  def insert_dgt(self, val):
    self.buffer.text += val
    self.display.text = self.buffer.text

  def replace_op(self, op):
    self.op = op

  def parse(self):
    expression = '{}{}{}'.format(self.l.text,self.op,self.r.text)
    value = eval(expression)
    self.l.text = str(value)
    self.display.text = str(value)

  def update(self):
    self.display.text = self.buffer.text

  def clear(self):
    self.display.text = '0'

  def advance(self, state):
    self.state = state


class CalculatorApp(App):
  def build(self):
    return Calculator()

if __name__ == '__main__':
  CalculatorApp().run()
