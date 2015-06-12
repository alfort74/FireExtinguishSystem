  # -*- coding: utf-8 -*-
import time
import cv2
import numpy as np
# from send_alert import sending_alert

###  定数  ###
IMG_HEIGHT = 240		# 処理画像の縦サイズ
IMG_WIDTH = 340			# 処理画像の横サイズ
MIN_THRESH = 500		# 閾値の最小値
MIN_VAL = 1000			# 初期値設定時の火元大きさ最小値	
FIRE_MASK = 160			# 赤外線の強さの閾値225
# WAIT_TIME = 10　			# 閾値を超えてから火災と判定するまでの繰り返し回数
WAIT_TIME=10 			# 閾値を超えてから火災と判定するまでの繰り返し回数
# THRESH_WEIGHT = 1.5　	# 火災と判定する閾値設定の初期値の重み(x倍)
THRESH_WEIGHT=1.5 		# 火災と判定する閾値設定の初期値の重み(x倍)
THRESH_PERCENT = 0.8
V_DIVISION = 10
H_DIVISION = 10

roi_width = IMG_WIDTH/H_DIVISION
roi_height = IMG_HEIGHT/V_DIVISION

alert_address = 'kitazonoalert@gmail.com'

###  無限ループで火災を検知する  ###
def main():
	## 初期設定 ##
		hold_time = 0
		# カメラ映像の取得
		cap = cv2.VideoCapture(0)
		# 閾値の初期化、設定
		# thresh = int(threshInit(cap) * THRESH_WEIGHT)
		# print 'Threshold Value is ', thresh
		fireList = selectScope(cap)
		timeHold = [0]*len(fireList)
	## 無限ループ・火災検知 ##
		while True:
			# キャプチャの白黒画像を取得
			im_bi = cap_bin(cap)
			roiWhite = []
			roiFire = []
#----------------- Testing : ROIを使った処理 -----------------------#
			for listnum in range(len(fireList)):			# すべての火元に対して処理を行うループ
				whiteList = [0] * len(fireList[listnum])
				roiWhite.append(whiteList)
				for i in range(len(fireList[listnum])):		# 一つの火元のすべての領域に対して処理を行うループ
					sx = roi_width*int(fireList[listnum][i]/H_DIVISION)			# ROI開始X座標
					sy = roi_height*int(fireList[listnum][i]%V_DIVISION)		# ROI開始Y座標
					ex = sx + roi_width											# ROI終了X座標
					ey = sy + roi_height										# ROI終了Y座標

					roi = im_bi[sy:ey, sx:ex]				# ROIを作成
					roiMask = roi > 110#FIRE_MASK 					# 閾値以上の部分を抽出
					
					for line in roiMask:
						for boolean in line:
							if boolean:
								roiWhite[listnum][i] += 1
					print listnum*10+i, fireList[listnum][i], roiWhite[listnum][i]
					# im_bi[sy:ey, sx:ex] = cv2.bitwise_not(roi)
					roi[roiMask] = 124									###255から124
					im_bi[sy:ey, sx:ex] = roi
				roiFire.append(sum(roiWhite[listnum]))
				print roiFire
				if roiFire[listnum] > roi_width*roi_height * THRESH_PERCENT:
					# 火災が検出されている箇所の火を白塗りする処理
					for i in range(len(fireList[listnum])):		# 一つの火元のすべての領域に対して処理を行うループ
						sx = roi_width*int(fireList[listnum][i]/H_DIVISION)
						sy = roi_height*int(fireList[listnum][i]%V_DIVISION)
						ex = sx + roi_width									
						ey = sy + roi_height								

						roi = im_bi[sy:ey, sx:ex]				# ROIを作成
						roiMask = roi > 110
						roi[roiMask] = 255									###255から124
						im_bi[sy:ey, sx:ex] = roi

					timeHold[listnum] +=1
					print "The point fire of ",listnum , "is Warning!!"
					# if timeHold[listnum] > WAIT_TIME:
						# sending_alert(alert_address)
						# print "A fire occured!! in The point",listnum,"\n Sent alert to ", alert_address
						# break
				else:
					timeHold[listnum] = 0

#------------------------------------------------------------------#

			# for address in range(H_DIVISION*V_DIVISION):
			# 	isContain = false
			# 	for x in range(len(fireList)):
			# 		if address in fireList[x]:
			# 			isContain = true
			# 	if(!isContain)
			# 	whitenum = 0
			# 	eachROI = getROI(im_bi, address)
			# 	mask = eachROI > FIRE_MASK
			# 	for line in mask:
			# 		for boolean in line:
			# 			if boolean:
			# 				whitenum +=1



#---------------- TODO : ROIを使った処理に変更 ----------------------#
			# # 画像の白黒をT/Fで持った配列maskの作成
			# mask = im_bi > FIRE_MASK
			# # 白部分の画素数をwhitenumに格納
			# whitenum = 0
			# for line in mask:
			# 	for boolean in line:
			# 		if boolean:
			# 			whitenum += 1
			# # whitenumを表示(デバッグ用)
			# print "Fire value of whole the sight is ", whitenum - sum(roiFire)
			# # 閾値より大きい場合は警告
			# if whitenum > thresh:
			# 	print "Warning!"
			# 	hold_time += 1
			# 	if hold_time > WAIT_TIME:
			# 		sending_alert(alert_address)
			# 		print "A fire occured!!\n Sent alert to ", alert_address
			# 		break
			# else:
			# 	hold_time = 0

#------------------------------------------------------------------#
		## 画像表示プロセス ##
			# 画像に部分領域を示す格子状の直線を描画
			im_bi = drawLattice(im_bi)
			# 画面に処理画像イメージを表示
			cv2.imshow("Binary",im_bi)
			# キーが押されたループから抜ける
			if cv2.waitKey(10) > 0:
				break
	## 終了処理 ##
		# キャプチャー解放
		cap.release()
		camera.release()
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
	im_bi[mask] = 120
	return im_bi

### アドレスを元にROIを返す ###
def getROI(img, address):
	sx = roi_width*int(address/H_DIVISION)
	sy = roi_height*int(address%V_DIVISION)
	ex = sx + roi_width
	ey = sy + roi_height

	roi = img[sy:ey, sx:ey]
	return roi

### 火災の検知範囲を指定 ###
def selectScope(cap):
	im_bi = drawLattice(cap_bin(cap))
	for v in range(V_DIVISION) :
		for h in range(H_DIVISION):
			text = str(V_DIVISION*v + h)
			cv2.putText(im_bi,text,(roi_width*v,roi_height*(h+1)),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255))
	cv2.imshow('Dividion',im_bi)
	print "Please Type Numeber of Fire"
	fireNum = raw_input('Number : ')
	# fireList = [12,13,14,15,16,17,18,22,23,24,25,26,27,28,32,33,34,35,36,37,38,42,43,44,45,46,47,48],[0]
	# fireList = [5,6,7,8,15,16,17,18,25,26,27,28],[0]
	fireList = []
	for i in range(int(fireNum)):
		fireList.append(map(int, raw_input('Input number of fire area : ').split()))
		# fireList = [raw_input() for _ in range(int(fireNum))]
		print fireList
	return fireList
	

### 画像に部分領域を示す格子状の直線を描画
def drawLattice(img):
	# 垂直な直線を表示
	for vertical in range(V_DIVISION):
		V_drawPoint = vertical*(IMG_WIDTH/V_DIVISION)
		cv2.line(img, (V_drawPoint,0), (V_drawPoint,IMG_HEIGHT), (255,255,255), 1)
	cv2.line(img, (IMG_WIDTH,0), (IMG_WIDTH,IMG_HEIGHT), (255,255,255), 1)
	# 水平な直線を表示
	for horizontal in range(V_DIVISION):
		H_drawPoint = horizontal*(IMG_HEIGHT/V_DIVISION)
		cv2.line(img, (0, H_drawPoint), (IMG_WIDTH,H_drawPoint), (255,255,255), 1)
	cv2.line(img, (0,IMG_HEIGHT), (IMG_WIDTH,IMG_HEIGHT), (255,255,255), 1)
	# 直線を描画した画像を返す
	return img




if __name__ == '__main__'	:
	main()
	
