import numpy as np

def my_imfilter(image, imfilter):
    """function which imitates the default behavior of the build in scipy.misc.imfilter function.

    Input:
        image: A 3d array represent the input image.
        imfilter: The gaussian filter.
    Output:
        output: The filtered image.
    """
    ###################################################################################
    # TODO:                                                                           #
    # This function is intended to behave like the scipy.ndimage.filters.correlate    #
    # (2-D correlation is related to 2-D convolution by a 180 degree rotation         #
    # of the filter matrix.)                                                          #
    # Your function should work for color images. Simply filter each color            #
    # channel independently.                                                          #
    # Your function should work for filters of any width and height                   #
    # combination, as long as the width and height are odd (e.g. 1, 7, 9). This       #
    # restriction makes it unambigious which pixel in the filter is the center        #
    # pixel.                                                                          #
    # Boundary handling can be tricky. The filter can't be centered on pixels         #
    # at the image boundary without parts of the filter being out of bounds. You      #
    # should simply recreate the default behavior of scipy.signal.convolve2d --       #
    # pad the input image with zeros, and return a filtered image which matches the   #
    # input resolution. A better approach is to mirror the image content over the     #
    # boundaries for padding.                                                         #
    # Uncomment if you want to simply call scipy.ndimage.filters.correlate so you can #
    # see the desired behavior.                                                       #
    # When you write your actual solution, you can't use the convolution functions    #
    # from numpy scipy ... etc. (e.g. numpy.convolve, scipy.signal)                   #
    # Simply loop over all the pixels and do the actual computation.                  #
    # It might be slow.                                                               #
    ###################################################################################
    ###################################################################################
    # NOTE:                                                                           #
    # Some useful functions                                                           #
    #     numpy.pad or numpy.lib.pad                                                  #
    # #################################################################################

    # Uncomment if you want to simply call scipy.ndimage.filters.correlate so you can
    # see the desired behavior.

    output = np.zeros_like(image, dtype=np.float32)
    f_h, f_w = imfilter.shape
    if len(image.shape) == 3:
        # color image
        img_h, img_w, img_c = image.shape
        image = np.pad(image, ((f_h//2,f_h//2), (f_w//2,f_w//2), (0,0)), 'constant', constant_values=0)
        for ch in range(img_c):
            for i in range(img_h):
                for j in range(img_w):
                    output[i][j][ch] = np.sum(imfilter * image[i:i+f_h, j:j+f_w, ch])

    elif len(image.shape) == 2:
        # gray scale image
        img_h, img_w = image.shape
        image = np.pad(image, ((f_h//2,f_h//2), (f_w//2,f_w//2)), 'constant', constant_values=0)
        for ch in range(img_c):
            for i in range(img_h):
                output[i][j] = np.sum(imfilter * image[i:i+f_h, j:j+f_w])
        

    # import scipy.ndimage as ndimage
    # output = np.zeros_like(image)
    # for ch in range(image.shape[2]):
    #    output[:,:,ch] = ndimage.filters.correlate(image[:,:,ch], imfilter, mode='constant')
    
    ###################################################################################
    #                                 END OF YOUR CODE                                #
    ###################################################################################
    return output

if __name__ == '__main__':
    pass