import PySimpleGUI as sg
import cv2
from video_player import VideoPlayer
import time
from config import *


def check_input_format(input_str: str):
    """
    入力文字がフォルダ番号のフォーマットとして正しいか確認
    
    Parameters
    ----------
    input_str:str
        InputTextに入力された文字列
        
    Returns
    --------
    is_correct_format: bool
        true:正しい
        false:正しくない

    """
    is_correct_format = False
    #入力が3文字か
    if len(input_str) != 3:
        return is_correct_format
    
    try:
        number = int(input_str)
    except Exception as e:
        return is_correct_format
    
    is_correct_format = True         
    return is_correct_format
    

vp = VideoPlayer()
file_name: str = "None"

#レイアウト作成
layout = [[sg.Text("データセット確認ツール")], 
            [sg.Text("データ番号："),
                sg.InputText(default_text='', size=(10,1),enable_events=True , key='input'),
                sg.Button("Read"),
                sg.Text("", size=(60,1), key='check_result')
            ],
            [sg.Slider(range=(0.0, 100.0), default_value=0.0, orientation='h', enable_events=True, key='slider')],
            [sg.Button('Play/Stop'), sg.Text("Stop", key='play_stop')],
            [sg.Button('Exit')]]


#ウィンドウ作成
window = sg.Window ('operation window', layout, size=(350,230))

while True:
    event, values = window.read(timeout=0)
    # print("イベント:{}, 数値：{}".format(event, values))
    if event in (None, 'Play/Stop'):
        vp.is_play = not vp.is_play
        play_stop_str: str = 'Stop' if not vp.is_play else 'Play'
        window['play_stop'].update(play_stop_str)


    #slider再設定や動画の情報を再読み込み
    if event in (None, 'Read'):
        input_str: str = values['input']
        if check_input_format(input_str):
            cv2.destroyAllWindows()
            vp.initialize()
            file_name = input_str
            vp.read_data(input_str)
            window['slider'].Update(range=(0, vp.frame_num)) 
            window["check_result"].update("入力OK")
        else: 
            window["check_result"].update("入力NG")
            
    
    if event in (None, 'slider'):
        slider_value: int = int(values["slider"])
        vp.set_current_frame(slider_value)
        stack_img = vp.get_stack_image()
        cv2.imshow(file_name, stack_img)
        
    if event in (None, 'Exit'):
        window.close()
        cv2.destroyAllWindows()
        break

    
    if vp.is_play:
        stack_img = vp.get_stack_image()
        cv2.imshow(file_name, stack_img)
        window['slider'].Update(value=vp.current_frame)
        cv2.waitKey(1)
        time.sleep(1/FPS)
        
        
