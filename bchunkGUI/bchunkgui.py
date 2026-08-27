import os
import subprocess
import sys
import dearpygui.dearpygui as dpg
import crossfiledialog as cfd


bin_path = ''
cue_path = ''


'''
filetypes:
0: bin
1: cue
'''
def file_dialog(filetype):
    path = '[Not Selected]'

    if filetype == 0:
        result = cfd.open_file(
            title='Select ".bin" file',
            start_dir=os.getcwd(),
            filter={'".bin" file': '*.bin'}
        )
    else:
        result = cfd.open_file(
            title='Select ".cue" file',
            start_dir=os.getcwd(),
            filter={'".cue" file': '*.cue'}
        )

    if result:
        path = result

    return path


def run_bchunk():
    if not bin_path or not cue_path:
        dpg.set_value('progress_label', 'Failure!')
        return

    dpg.set_value('progress_label', 'Converting. . .')
    out_prefix = os.path.splitext(os.path.basename(cue_path))[0]

    cmd = None
    exe = ''
    if sys.platform == 'win32':
        exe = 'bchunk.exe'
        cmd = f'{exe} "{bin_path}" "{cue_path}" "{out_prefix}"'
    else:
        exe = 'bchunk'
        cmd = [exe, bin_path, cue_path, out_prefix]

    result = None
    try:
        result = subprocess.run(cmd)
        if result.returncode == 0:
            dpg.set_value('progress_label', 'Success!')
        else:
            dpg.set_value('progress_label', f'Failure (code {result.returncode})')
    except Exception as error:
        dpg.set_value('progress_label', f'Error: {error}')


dpg.create_context()


def bin_dialog():
    global bin_path
    bin_path = file_dialog(filetype=0)
    dpg.set_value('bin_label', f'bin: {os.path.basename(bin_path)}')


def cue_dialog():
    global cue_path
    cue_path = file_dialog(filetype=1)
    dpg.set_value('cue_label', f'cue: {os.path.basename(cue_path)}')


with dpg.window(tag='primary'):
    dpg.add_button(label='Open ".bin" file', callback=bin_dialog)
    dpg.add_text('bin: [Not Selected]', tag='bin_label')

    dpg.add_button(label='Open ".cue" file', callback=cue_dialog)
    dpg.add_text('cue: [Not Selected]', tag='cue_label')

    dpg.add_button(label='Convert to ".iso" file', callback=run_bchunk)
    dpg.add_text('', tag='progress_label')


dpg.create_viewport(title='bChunk GUI', width=450, height=350)
dpg.set_primary_window("primary", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
