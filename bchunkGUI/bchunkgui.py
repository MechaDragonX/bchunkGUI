import os
import subprocess
import sys
import dearpygui.dearpygui as dpg
import crossfiledialog as cfd


bin_path = ''
cue_path = ''
output_dir = ''
output_name = ''
outfile_tag  = 'outfile_input'
outfile_input_label = 'Output filename WITHOUT ".ISO"'
outfile_input_group = 'outfile_input_group'
parent_window = 'primary'


'''
filetypes:
0: bin
1: cue
2: directory
'''
def get_path_with_dialog(filetype):
    path = '[Not Selected]'

    start = ''
    if (0 and 1) or output_dir == '':
        start = os.getcwd()
    else:
        start = os.path.dirname(output_dir)

    if filetype == 0:
        result = cfd.open_file(
            title='Select ".bin" file',
            start_dir=start,
            filter={'".bin" file': '*.bin'}
        )
    elif filetype == 1:
        result = cfd.open_file(
            title='Select ".cue" file',
            start_dir=start,
            filter={'".cue" file': '*.cue'}
        )
    else:
        result = cfd.choose_folder(
            title='Select output folder',
            start_dir=start
        )

    if result:
        path = result

    if filetype != 2:
        return path
    else:
        return output_dir


def run_bchunk():
    if not bin_path or not cue_path:
        dpg.set_value('progress_label', 'Failure!')
        return

    dpg.set_value('progress_label', 'Converting. . .')
    out_prefix = f'{output_dir}{output_name}'

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


def file_dialog_handler(filetype):
    global output_dir
    global output_name

    if filetype == 0:
        global bin_path
        bin_path = get_path_with_dialog(filetype=0)
        output_dir = f'{os.path.dirname(bin_path)}/'
        dpg.set_value('bin_label', f'".bin" file: {os.path.basename(bin_path)}')
        output_name = os.path.basename(bin_path)[:-4]
    else:
        global cue_path
        cue_path = get_path_with_dialog(filetype=1)
        dpg.set_value('cue_label', f'".cue" file: {os.path.basename(cue_path)}')
        output_name = os.path.basename(cue_path)[:-4]

    dpg.delete_item(outfile_tag)
    dpg.add_input_text(tag=outfile_tag, hint=output_name, parent=outfile_input_group)
    dpg.set_value('outfile_label', f'Output filename: {output_name}')
    

def bin_dialog_handler():
    # global bin_path
    # global output_dir
    # global output_name
    # bin_path = file_dialog(filetype=0)
    # dpg.set_value('bin_label', f'".bin" file{os.path.basename(bin_path)}')
    # output_dir = f'{os.path.dirname(bin_path)}/'
    # dpg.delete_item(outfile_tag)
    # output_name = os.path.basename(bin_path)[:-4]
    # dpg.add_input_text(label=outfile_input_label, tag=outfile_tag, hint=output_name, parent=outfile_input_group)
    # dpg.set_value('outfile_label', f'Output file: {output_name}')
    file_dialog_handler(0)

def cue_dialog_handler():
    # global cue_path
    # global output_dir
    # global output_name
    # cue_path = file_dialog(filetype=1)
    # dpg.set_value('cue_label', f'".cue" file{os.path.basename(cue_path)}')
    # output_dir = f'{os.path.dirname(cue_path)}/'
    # dpg.delete_item(outfile_tag)
    # output_name = os.path.basename(cue_path)[:-4]
    # dpg.add_input_text(label=outfile_input_label, tag=outfile_tag, hint=output_name, parent=outfile_input_group)
    # dpg.set_value('outfile_label', f'Output file: {output_name}')
    file_dialog_handler(1)

def output_dialog_callback():
    # output_name = dpg.get_value('outfile_input')
    # dpg.set_value('outfile_label', output_name)
    global output_dir
    output_dir = get_path_with_dialog(filetype=2)


with dpg.window(tag='primary'):
    dpg.add_button(label='Open ".bin" file', callback=bin_dialog_handler)
    dpg.add_text('".bin" file: [Not Selected]', tag='bin_label')

    dpg.add_button(label='Open ".cue" file', callback=cue_dialog_handler)
    dpg.add_text('".cue" file: [Not Selected]', tag='cue_label')

    dpg.add_button(label='Select output folder', callback=output_dialog_callback)
    with dpg.group(tag='outfile_input_group'):
        dpg.add_text('Please type an output filename WITHOUT ".ISO"')
        dpg.add_input_text(tag='outfile_input')
    dpg.add_text('Output filename: [Not Set]', tag='outfile_label')

    dpg.add_button(label='Convert to ".iso" file', callback=run_bchunk)
    dpg.add_text('', tag='progress_label')


dpg.create_viewport(title='bChunk GUI', width=450, height=350)
dpg.set_primary_window("primary", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
