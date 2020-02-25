#!/usr/bin/env python
import sys
from os import environ as env
import os

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from pygments.lexers.shell import BashLexer
from pygments.styles import get_style_by_name


def key_bindings():
  key_binding = KeyBindings()
  key_binding.add('enter')(return_handler)
  return key_binding

def return_handler(event):
  buffer = event.current_buffer
  # document = buffer.document
  if buffer.text.endswith("\\"):
    buffer.text=buffer.text[:-1]+'\n'
  else:
    buffer.validate_and_handle()

def prompt_continuation(width, line_number, is_soft_wrap):
  return ' '*(width-2) + "… "


style = style_from_pygments_cls(get_style_by_name(env.get(
    '_debug_read_color_scheme', 'vim')))
session = PromptSession(message=env.get('_debug_prompt', '$ '),
                        lexer=PygmentsLexer(BashLexer),
                        style=style,
                        key_bindings=key_bindings(),
                        history=FileHistory(env.get('JUST_DEBUG_HISTORY',
                            os.path.expanduser('~/.debug_bash_history'))+'3'),
                        enable_history_search=True,
                        multiline=True,
                        auto_suggest=AutoSuggestFromHistory(),
                        prompt_continuation=prompt_continuation)

try:
  text = session.prompt()
  sys.stderr.write(text)
except KeyboardInterrupt:
  pass
