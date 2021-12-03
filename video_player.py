import cv2
import os
from config import *
import numpy as np


class VideoPlayer:
        
    def __init__(self):
        self.current_frame: int = 0
        self.is_play: bool = False
        self.frame_num: int = 1
        self.left_imgs_list = []
        self.right_imgs_list = []
        self.disparity_imgs_list = []
    
    
    def scale_to_width(self, img):
        """
        幅がIMAGE_Wになるように、アスペクト比を固定して、リサイズ
        """
        h, w = img.shape[:2]
        height = round(h * (IMAGE_W / w))
        dst = cv2.resize(img, dsize=(IMAGE_W, height))

        return dst


    def vertical_stack_images(self, left_img, right_img, disparity_img):
        """
        左目、右目、視差の画像を垂直方向に重ねた画像を生成
        画像の横幅も3つの画像同一になるように変換
        
        Parameters
        ----------
        left_img: 画像
            左目画像
        right_img: 画像
            右目画像
        disparity_img: 画像
            視差画像
        
        Returns
        ---------
        stack_img: 画像
        """
        left_img = self.scale_to_width(left_img)
        right_img = self.scale_to_width(right_img)
        disparity_img = self.scale_to_width(disparity_img)
        stack_img = np.concatenate((left_img, right_img, disparity_img), axis=0)
        return stack_img
    
    
    def initialize(self):
        self.current_frame = 0
        self.is_play = False
        self.frame_num = 1
        self.left_video = None
        self.right_video = None
        self.disparity_imgs_list = []


    def read_data(self, file_idx: str):
        """
        データ番号を引数で受け取り、対象のパスを生成し左目、右目、視差のデータを読み込む
        
        Parameters
        ----------
        path: str
            データ番号
        
        Returns
        ---------
        left_video: cv2.VideoCapture
            左目動画
        right_video: cv2.VideoCapture
            右目動画
        disparity_imgs: list
            視差画像全フレームを格納したリスト
        """
        filepath = os.path.join(VIDEOS_PATH, file_idx)
        left_video = cv2.VideoCapture(os.path.join(filepath, 'Left.mp4'))
        right_video = cv2.VideoCapture(os.path.join(filepath, 'Right.mp4'))
        
        frame_num = int(left_video.get(cv2.CAP_PROP_FRAME_COUNT))
        for i in range(frame_num):
            _, cap = left_video.read()
            self.left_imgs_list.append(cap)
            _, cap = right_video.read()
            self.right_imgs_list.append(cap)
        
        #disparity_PNG内の全画像数を求めて、disparity_img_listに全画像を格納
        disparity_path: str = os.path.join(filepath, 'disparity_PNG')
        disparity_path_list: list = os.listdir(disparity_path)

        for path in disparity_path_list:
            disparity_img = cv2.imread(os.path.join(disparity_path, path))
            self.disparity_imgs_list.append(disparity_img)
        
        #その他変数の設定
        self.frame_num = len(self.disparity_imgs_list)

    
    def set_current_frame(self, frame):
        """
        スライダーによる再生位置の指定
        Parameters
        ----------
        frame: int
            スライダーで変更した再生位置
        """
        self.current_frame = frame
    
    
    def get_stack_image(self):
        """
        左目、右目、視差の画像を垂直方向に追加した画像を生成して渡す
        
        Returns
        ----------
        stack_img: 画像
            左目、右目、視差の画像を垂直方向に追加した画像
        """
        if self.current_frame >= self.frame_num:
            self.current_frame = self.frame_num -1
        
        #画像を垂直方向にstack
        stack_img = self.vertical_stack_images(self.left_imgs_list[self.current_frame], self.right_imgs_list[self.current_frame], self.disparity_imgs_list[self.current_frame])
        
        self.current_frame += 1
        
        return stack_img
    
