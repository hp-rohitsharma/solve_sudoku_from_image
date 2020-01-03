import numpy as np
from sklearn.externals import joblib
from image_util import show_image, crop_digit, resize, enlarge_image_and_highlight_features, find_sudoku_rectangle
from sudoku_util import solve

try:
    import cv2
except ImportError:
    print("Please install OpenCV")

model = joblib.load(".\\model\\model.pkl")

def image_to_feature(img):
    #img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (28,28), interpolation = cv2.INTER_AREA)
    img = np.array(img) / 10
    img[img < 20] = 0
    img = img.astype("uint8")
    return img.reshape(1, -1)[0]

def image_to_array(img, size):
	#show_image(img)
	side = img.shape[:1]
	side = side[0] / 9
	result = [[0 for i in range(9)] for j in range(9)] 
	for i in range(9):
		for j in range(9):
			tl = (i * side, j * side)  # Top left corner
			br = ((i + 1) * side, (j + 1) * side)  # Bottom right corner		
			digit = crop_digit(img, (tl, br), size)
			if(digit is not None):				
				digit = resize(digit, size, 4)
				#show_image(digit)
				feature = image_to_feature(digit)
				if len(feature) != 0:								
					predicted = model.predict([feature])[0]
					#print(predicted)
					result[j][i] = int(predicted)
				else:					
					result[j][i] = int(0)
	return result

def print2DArray(result):
	for i in range(9):
		for j in range(9):	
			print(result[i][j], end =" , ")
		print()

original_image = cv2.imread('.\\image\\sudoku.png', cv2.IMREAD_GRAYSCALE)
#show_image(original_image)
sudoku_rectangle = find_sudoku_rectangle(original_image)
# re-assuring if box is indeed the sudoku
sudoku_rectangle = find_sudoku_rectangle(sudoku_rectangle)
#show_image(sudoku_rectangle)
processed_image = enlarge_image_and_highlight_features(sudoku_rectangle, 400)
#show_image(processed_image)
result = image_to_array(processed_image, 28)
print('Before')
print2DArray(result)
result = solve(result)
print('After')
print2DArray(result)