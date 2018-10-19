import os
import numpy as np
from scipy.signal import convolve2d
from scipy.misc import imresize
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from gauss2D import gauss2D
from my_imfilter import my_imfilter
from normalize import normalize
import scipy.ndimage as ndimage
from normalize import normalize

def ground_truth_imfilter(image, imfilter):
    output = np.zeros_like(image)
    for ch in range(image.shape[2]):
        output[:,:,ch] = ndimage.filters.correlate(
                        image[:,:,ch], imfilter, mode='constant')
        # output[:,:,ch] = ndimage.filters.convolve(
        #                 image[:,:,ch], imfilter, mode='constant')
        output[:,:,ch] = convolve2d(image[:,:,ch], imfilter, mode='same', boundary='fill', fillvalue=0)
                        
    return output

def check(img1, img2, is_show=True):
    t = img1 == img2
    img = img1 - img2
    if is_show:
        plt.imshow(np.array(normalize(img), dtype=np.float64))
        plt.show()
    return t[t==False]

def main():
    """function to helps debug your image filtering algorithm. """
    main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(main_path, 'data', 'cat.bmp')
    test_image = mpimg.imread(img_path)
    test_image = imresize(test_image, 0.7, interp='bilinear')
    test_image = test_image.astype(np.float32)/255
    plt.figure('Image')
    plt.imshow(test_image)

    identity_filter = np.array([[0, 0, 0], 
                                [0, 1, 0], 
                                [0, 0, 0]], dtype=np.float32)
    identity_image = my_imfilter(test_image, identity_filter)
    identity_image_gt = ground_truth_imfilter(test_image, identity_filter)
    print('identity test')
    check(identity_image, identity_image_gt)

    ### Small blur with a box filter ###
    # This filter should remove some high frequencies
    blur_filter = np.array([[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]], dtype=np.float64)
    blur_filter = blur_filter.astype(np.float) / np.sum(blur_filter)  # making the filter sum to 1
    blur_filter = np.ones((3, 3))/9
    blur_image = my_imfilter(test_image, blur_filter)
    blur_image_gt = ground_truth_imfilter(test_image, blur_filter)
    print('blur test')
    check(blur_image, blur_image_gt)

    ### Large blur ###
    #This blur would be slow to do directly, so we instead use the fact that
    #Gaussian blurs are separable and blur sequentially in each direction.
    large_2d_blur_filter = gauss2D(shape=(25, 25), sigma=10)
    large_blur_image = my_imfilter(test_image, large_2d_blur_filter)
    large_blur_image_gt = ground_truth_imfilter(test_image, large_2d_blur_filter)
    print('large_2d_blur test')
    check(large_blur_image, large_blur_image_gt)

    ### Oriented filter (Sobel Operator) ###
    sobel_filter = np.array([[-1, 0, 1],
                             [-2, 0, 2],
                             [-1, 0, 1]])
    s = np.array([[1, 0, -1],
                  [2, 0, -2],
                  [1, 0, -1]])
    sobel_image = my_imfilter(test_image, sobel_filter)
    sobel_image_gt = ground_truth_imfilter(test_image, s)
    #0.5 added because the output image is centered around zero otherwise and mostly black
    print('sobel test')
    check(sobel_image, sobel_image_gt)

    ### High pass filter (Discrete Laplacian) ###
    laplacian_filter = np.array([[0, 1, 0],
                                 [1, -4, 1],
                                 [0, 1, 0]])
    laplacian_image = my_imfilter(test_image, laplacian_filter)
    laplacian_image_gt = ground_truth_imfilter(test_image, laplacian_filter)
    #0.5 added because the output image is centered around zero otherwise and mostly black
    print('laplacian test')
    check(laplacian_image, laplacian_image_gt)

    ### High pass "filter" alternative ###
    high_pass_image = test_image - blur_image #simply subtract the low frequency content
    high_pass_image_gt = test_image - blur_image_gt
    print('high pass test')
    check(high_pass_image, high_pass_image_gt)

if __name__ == '__main__':
    main()