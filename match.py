import cv2
import argparse

parser = argparse.ArgumentParser(description='Fingerprint Matching')
parser.add_argument('first_img', help='Path to first image')
parser.add_argument('second_img', help='Path to second image')
# parser.add_argument('--thresh', help='Matching threshold')

args = parser.parse_args()
# IMAGES_PATH = os.path.join('data')
FIRST_IMAGE_PATH = args.first_img
SECOND_IMAGE_PATH = args.second_img
# THRESHOLD = float(args.thresh)

test_original = cv2.imread(FIRST_IMAGE_PATH)
test_original = cv2.cvtColor(test_original, cv2.COLOR_RGB2GRAY)
cv2.imshow(f"Original - {FIRST_IMAGE_PATH}", cv2.resize(test_original, None, fx=1, fy=1))
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print(f'Current Image: {file}')
fingerprint_database_image = cv2.imread(SECOND_IMAGE_PATH)
fingerprint_database_image = cv2.cvtColor(fingerprint_database_image, cv2.COLOR_RGB2GRAY)
cv2.imshow(f"Current - {SECOND_IMAGE_PATH}", cv2.resize(fingerprint_database_image, None, fx=1, fy=1))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
sift = cv2.xfeatures2d.SIFT_create()

keypoints_1, descriptors_1 = sift.detectAndCompute(test_original, None)
keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image, None)

matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), 
    dict()).knnMatch(descriptors_1, descriptors_2, k=2)

match_points = []

for p, q in matches:
    if p.distance < 0.1*q.distance:
        match_points.append(p)

keypoints = 0
if len(keypoints_1) <= len(keypoints_2):
    keypoints = len(keypoints_1)            
else:
    keypoints = len(keypoints_2)

# print("Figerprint ID: " + str(file), end=' ')
print(f'{(len(match_points) / keypoints) * 100}% match')
result = cv2.drawMatches(test_original, keypoints_1, fingerprint_database_image, 
                        keypoints_2, match_points, None) 
result = cv2.resize(result, None, fx=1, fy=1)
cv2.imshow(f"Features", result)
cv2.waitKey(0)
cv2.destroyAllWindows()