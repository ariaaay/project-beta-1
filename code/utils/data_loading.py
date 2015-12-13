
from __future__ import print_function
import nibabel as nib
import numpy as np
import scipy
import scipy.ndimage
from scipy.ndimage.filters import gaussian_filter

def load_data(filename):
    """ Return fMRI data corresponding to the given filename and prints
        shape of the data array
    ----------
    filename : string 
        This string should be a path to given file. The file must be
        .nii 
    Returns
    -------
    data : numpy array
        An array consisting of the data. 
    """
    img = nib.load(filename)
    data = img.get_data()
    data = data[:,:,:,4:]
    print(data.shape)
    return data

def load_all_data(filename):
    """ Return fMRI data corresponding to the given filename and prints
        shape of the data array
    ----------
    filename : string 
        This string should be a path to given file. The file must be
        .nii 
    Returns
    -------
    data : numpy array
        An array consisting of the data. 
    """
    img = nib.load(filename)
    data = img.get_data()
    print(data.shape)
    return data

def vox_by_time(data):
    """ Returns a reshaped array w/ dimensions = #voxels x #volumes  
    Parameters
    ----------
    data : 4d array
    Returns
    -------
    reshaped : 2-D array
        Reshaped array consisting of voxels by time 
    """
    n_voxels = np.prod(data.shape[:3])
    return np.reshape(data, (n_voxels, data.shape[-1]))

def vol_std(data):
    """ Return standard deviation across voxels for 4D array `data`
    Parameters
    ----------
    data : 4D array
        4D array from FMRI run with last axis indexing volumes.  Call the shape
        of this array (M, N, P, T) where T is the number of volumes.
    Returns
    -------
    std_values : array shape (T,)
        One dimensonal array where ``std_values[i]`` gives the standard
        deviation of all voxels contained in ``data[..., i]``.
    """
    num_volumes = data.shape[-1]
    vox_by_time = data.reshape((-1, num_volumes))
    return np.std(vox_by_time, axis = 0)

def iqr_outliers(arr_1d, iqr_scale=1.5):
    """ Return indices of outliers identified by interquartile range
    Parameters
    ----------
    arr_1d : 1D array
        One-dimensional numpy array, from which we will identify outlier
        values.
    iqr_scale : float, optional
        Scaling for IQR to set low and high thresholds.  Low threshold is given
        by 25th centile value minus ``iqr_scale * IQR``, and high threshold id
        given by 75 centile value plus ``iqr_scale * IQR``.
    Returns
    -------
    outlier_indices : array
        Array containing indices in `arr_1d` that contain outlier values.
    lo_hi_thresh : tuple
        Tuple containing 2 values (low threshold, high thresold) as described
        above.
    """
    q75, q25 = np.percentile(arr_1d, [75 ,25])
    IQR = q75 - q25
    lower = q25 - iqr_scale * IQR
    upper = q75 + iqr_scale * IQR
    low_outliers = np.where(arr_1d < lower)[0]
    high_outliers = np.where(arr_1d > upper)[0]
    all_outliers = np.concatenate((low_outliers, high_outliers), axis=0)
    all_outliers = np.sort(all_outliers)
    return all_outliers, (lower, upper)

def vol_rms_diff(arr_4d):
    """ Return root mean square of differences between sequential volumes
    Parameters
    ----------
    data : 4D array
        4D array from FMRI run with last axis indexing volumes.  Call the shape
        of this array (M, N, P, T) where T is the number of volumes.
    Returns
    -------
    rms_values : array shape (T-1,)
        One dimensonal array where ``rms_values[i]`` gives the square root of
        the mean (across voxels) of the squared difference between volume i and
        volume i + 1.
    """
    num_volumes = arr_4d.shape[-1]
    vox_by_time = arr_4d.reshape((-1, num_volumes))
    differences = np.diff(vox_by_time, axis=1)
    exp_rms = np.sqrt(np.mean(differences ** 2, axis=0))
    return exp_rms

def remove_outliers_iqr(arr, axis, iqr_scale=1.5):
    """ Return data of outliers (identified by interquartile range) removed
    Parameters
    ----------
    arr : array
        Numpy array, from which we will identify outlier values.
    axis : integer
        Integer indicating the axis at which to remove the outliers
    iqr_scale : float, optional
        Scaling for IQR to set low and high thresholds.  Low threshold is given
        by 25th centile value minus ``iqr_scale * IQR``, and high threshold id
        given by 75 centile value plus ``iqr_scale * IQR``.
    Returns
    -------
    outlier_indices : 1-D array
        Array of removed outliers along the given axis.
    lo_hi_thresh : tuple
        Tuple containing 2 values (low threshold, high thresold) as described
        above.
    """
    axis_data = get_axis_data(data, axis)
    indcs, lo_hi_thresh = iqr_outliers(axis_data, iqr_scale)
    return (indcs, lo_hi_thresh) 

#project alphas's 
def smooth_gauss(data_4d, fwhm, time):

    """
    Return a 'smoothed' version of data_4d.
    Parameters
    ----------
    data_4d : numpy array of 4 dimensions 
        The image data of one subject
    fwhm : width of normal gaussian curve
    time : time slice (4th dimension)
    Returns
    -------
    smooth_results : array of the smoothed data from data_4d (same dimensions but super-voxels will be
                        indicated by the same number) in time slice indicated.
    """
    time_slice = data_4d[..., time]
    smooth_results = scipy.ndimage.filters.gaussian_filter(time_slice, fwhm)
    return smooth_results
