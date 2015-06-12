# -*- coding: utf-8 -*-
import time
import cv2
import numpy as np
from send_alert import sending_alert

###  定数  ###
IMG_HEIGHT = 240		# 処理画像の縦サイズ
IMG_WIDTH = 340			# 処理画像の横サイズ
MIN_THRESH = 500		# 閾値の最小値
MIN_VAL = 1000			# 初期値設定時の火元大きさ最小値		
FIRE_MASK = 225			# 赤外線の強さの閾値
WAIT_TIME = 10　			# 閾値を超えてから火災と判定するまでの繰り返し回数
THRESH_WEIGHT = 1.5　	# 火災と判定する閾値設定の初期値の重み(x倍)

alert_address = 'kitazonoalert@gmail.com'

###  無限ループで火災を検知する  ###
def main():
	## 初期設定 ##
		hold_time = 0
		# カメラ映像の取得
		cap = cv2.VideoCapture(0)
		# 閾値の初期化、設定
		thresh = int(threshInit(cap) * THRESH_WEIGHT)
		print 'Threshold Value is ', thresh
	## 無限ループ・火災検知 ##
		while True:
			# キャプチャの白黒画像を取得
			im_bi = cap_bin(cap)
			# 画像の白黒をT/Fで持った配列maskの作成
			mask = im_bi > FIRE_MASK
			# 白部分の画素数をwhitenumに格納
			whitenum = 0
			for line in mask:
				for boolean in line:
					if boolean:
						whitenum += 1
			# whitenumを表示(デバッグ用)
			print whitenum
			# 閾値より大きい場合は警告
			if whitenum > thresh:
				print "Warning!"
				hold_time += 1
				if hold_time > WAIT_TIME:
					sending_alert(alert_address)
					print "A fire occured!!\n Sent alert to ", alert_address
					break
			else:
				hold_time = 0
			# 画面に処理画像イメージを表示
			cv2.imshow("Binary",im_bi)
			# キーが押されたループから抜ける
			if cv2.waitKey(10) > 0:
				break
	## 終了処理 ##
		# キャプチャー解放
		cap.release()
		# ウィンドウ破棄
		cv2.destroyAllWindows()


### 初期化して閾値を設定する ###
def threshInit(cap):
	whiteval = []
## 画面情報を表示(デバッグ用) ##
	print 'IMG_HEIGHT is ', IMG_HEIGHT
	print 'IMG_WIDTH is ', IMG_WIDTH
	print 'Total number of Pixel is ', IMG_HEIGHT*IMG_WIDTH
## 10回の平均から閾値を算出 ##
	for i in range(10):
		# キャプチャの白黒画像を取得
		im_bi = cap_bin(cap)
		# 画像の白黒をT/Fで持った配列maskの作成
		mask = im_bi > FIRE_MASK
		# 白部分の画素数をwhitenumに格納
		whitenum = 0
		for line in mask:
			for boolean in line:
				if boolean:
					whitenum += 1
		# 平均算出用配列whitevalにwhitenumの格納
		if whitenum > MIN_VAL:
			whiteval.append(whitenum)
	# whitevalの平均値をaverageに格納
	print whiteval
	average = np.average(whiteval)
	# 算出した平均値が最低設定値を下回ったら最低値を設定する
	if average < MIN_THRESH:
		return 	MIN_THRESH
	else:
		return average

### キャプチャ取得・白黒化 ###
def cap_bin(cap):
	# キャプチャから画像を取得	
	ret, im = cap.read()
	# 画像を半分にリサイズ
	im_half = cv2.resize(im,(IMG_WIDTH, IMG_HEIGHT))
	# 画像をグレースケールに変換
	im_gray = cv2.cvtColor(im_half, cv2.COLOR_BGR2GRAY)
	# グレースケール画像を2値画像に変換(閾値122)
	mask = im_gray > FIRE_MASK
	# 背景画像と同じサイズの配列作成
	im_bi = np.zeros((im_gray.shape[0], im_gray.shape[1]), np.uint8)
	# True部分(背景)は白塗り
	im_bi[mask] = 255
	return im_bi


if __name__ == '__main__'	:
	main()
	
