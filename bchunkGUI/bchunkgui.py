import os
import subprocess
import dearpygui.dearpygui as dpg
import tkinter as tk
from tkinter import filedialog

bin_path = ''
cue_path = ''

'''
filetypes:
0: bin
1: cue
'''
def tkinter_file_dialog(filetype):
    path = '[Not Selected]'

    root = tk.Tk()
    root.withdraw()

    selected = False
    if filetype == 0:
        selected = filedialog.askopenfilename(
            title='Select ".bin" file',
            filetypes = [('".bin" file', '*.bin')]
        )
    else:
        selected = filedialog.askopenfilename(
        title='Select ".cue" file',
        filetypes = [('".cue" file', '*.cue')]
        )
    root.destroy()

    if selected:
        path = selected

    return path


def run_bchunk(sender, app_data):
    pass


dpg.create_context()


def bin_dialog():
    global bin_path
    bin_path = tkinter_file_dialog(filetype=0)
    dpg.set_value('bin_label', f'bin: {os.path.basename(bin_path)}')


def cue_dialog():
    global cue_path
    cue_path = tkinter_file_dialog(filetype=1)
    dpg.set_value('cue_label', f'cue: {os.path.basename(cue_path)}')


with dpg.window(tag='primary'):
    dpg.add_button(label='Open ".bin" file', callback=bin_dialog)
    dpg.add_text('bin: [Not Selected]', tag='bin_label')

    dpg.add_button(label='Open ".cue" file', callback=cue_dialog)
    dpg.add_text('cue: [Not Selected]', tag='cue_label')

    dpg.add_button(label='Convert to ".iso" file', callback=run_bchunk)
    dpg.add_text('', tag='progress_lable')


dpg.create_viewport(title='bChunk GUI', width=450, height=350)
dpg.set_primary_window("primary", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
