
import laspy
import numpy as np
import cv2
from osgeo import gdal
import matplotlib.pyplot as plt

def load_lidar_data(lidar_path):
    """Load LiDAR data from a LAS file."""
    lidar_file = laspy.file.File(lidar_path, mode='r')
    points = np.vstack((lidar_file.x, lidar_file.y, lidar_file.z)).transpose()
    intensity = lidar_file.intensity
    if hasattr(lidar_file, 'red'):
        colors = np.vstack((lidar_file.red, lidar_file.green, lidar_file.blue)).transpose()
    else:
        colors = None
    return points, intensity, colors

def load_image(image_path):
    """Load an image using OpenCV."""
    image = cv2.imread(image_path)
    return image

def get_geotransform(image_path):
    """Get geotransform from an image using GDAL."""
    dataset = gdal.Open(image_path)
    geotransform = dataset.GetGeoTransform()
    return geotransform

def pixel_to_geo(x, y, geotransform):
    """Convert pixel coordinates to geographic coordinates."""
    geo_x = geotransform[0] + x * geotransform[1] + y * geotransform[2]
    geo_y = geotransform[3] + x * geotransform[4] + y * geotransform[5]
    return geo_x, geo_y

def geo_to_pixel(geo_x, geo_y, geotransform):
    """Convert geographic coordinates to pixel coordinates."""
    inv_geotransform = gdal.InvGeoTransform(geotransform)
    pixel_x = int(inv_geotransform[0] + inv_geotransform[1] * geo_x + inv_geotransform[2] * geo_y)
    pixel_y = int(inv_geotransform[3] + inv_geotransform[4] * geo_x + inv_geotransform[5] * geo_y)
    return pixel_x, pixel_y

def overlay_lidar_on_image(lidar_points, lidar_colors, image, geotransform):
    """Overlay LiDAR points on the image."""
    lidar_points_geo = np.array([pixel_to_geo(x, y, geotransform) for x, y, z in lidar_points[:, :2]])
    lidar_points_pixel = np.array([geo_to_pixel(x, y, geotransform) for x, y in lidar_points_geo])

    # Plot the image
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), extent=[0, image.shape[1], image.shape[0], 0])

    # Overlay LiDAR points
    if lidar_colors is not None:
        plt.scatter(lidar_points_pixel[:, 0], lidar_points_pixel[:, 1], c=lidar_colors / 65535.0, s=1)
    else:
        plt.scatter(lidar_points_pixel[:, 0], lidar_points_pixel[:, 1], c=lidar_points[:, 2], cmap='viridis', s=1)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Overlay of Colorized Image on LiDAR Data')
    plt.show()

if __name__ == '__main__':
    # File paths
    lidar_path = '0000000003.las'
    image_path = '0000000003.jpg'

    # Load LiDAR data
    lidar_points, intensity, colors = load_lidar_data(lidar_path)

    # Load panoramic image
    image = load_image(image_path)

    # Get geotransform
    geotransform = get_geotransform(image_path)

    # Overlay LiDAR data on image
    overlay_lidar_on_image(lidar_points, colors, image, geotransform)
