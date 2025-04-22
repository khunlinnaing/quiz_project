import os
import cv2
import numpy as np
from tkinter import Tk, filedialog, simpledialog
from skimage import filters, measure, morphology
from skimage.measure import regionprops
from scipy import ndimage as ndi
from tensorflow.keras.models import load_model
import pickle
import sys
import matplotlib.pyplot as plt


def check_condition_between(value, lower, upper):
    return lower <= value <= upper

def get_custom_rice_types():
    root = Tk()
    root.withdraw()
    root.update()  # Ensure the Tk window is fully initialized

    try:
        rice_type_count = int(simpledialog.askstring("Input", "Enter number of rice grain types to classify:", parent=root))
    except (TypeError, ValueError):
        print("Invalid number of rice types.")
        sys.exit()

    grain_type_conditions = {}
    grain_type_areas = {}

    for i in range(rice_type_count):
        name = simpledialog.askstring("Input", f"Enter name for rice type {i+1}:", parent=root)
        try:
            length_min = float(simpledialog.askstring("Input", f"Enter minimum length for {name} (mm):", parent=root))
            length_max = float(simpledialog.askstring("Input", f"Enter maximum length for {name} (mm):", parent=root))
            width_min = float(simpledialog.askstring("Input", f"Enter minimum width for {name} (mm):", parent=root))
            width_max = float(simpledialog.askstring("Input", f"Enter maximum width for {name} (mm):", parent=root))
            aspect_min = float(simpledialog.askstring("Input", f"Enter minimum aspect ratio for {name}:", parent=root))
            aspect_max = float(simpledialog.askstring("Input", f"Enter maximum aspect ratio for {name}:", parent=root))
        except (TypeError, ValueError):
            print("Invalid input for grain parameters.")
            sys.exit()

        grain_type_conditions[name] = {
            "length_min": length_min,
            "length_max": length_max,
            "width_min": width_min,
            "width_max": width_max,
            "aspect_min": aspect_min,
            "aspect_max": aspect_max
        }
        grain_type_areas[name] = 0

    root.destroy()
    return grain_type_conditions, grain_type_areas

def classify_grain_type(length_mm, width_mm, smooth_mask, grain_type_conditions, grain_type_areas):
    try:
        aspect_ratio = length_mm / width_mm
    except ZeroDivisionError:
        aspect_ratio = 0

    for name, cond in grain_type_conditions.items():
        if (check_condition_between(length_mm, cond['length_min'], cond['length_max']) and
            check_condition_between(width_mm, cond['width_min'], cond['width_max']) and
            check_condition_between(aspect_ratio, cond['aspect_min'], cond['aspect_max'])):
            grain_type_areas[name] += np.count_nonzero(smooth_mask)
            return name
    return "Unknown"

def print_grain_type_area_percentages(grain_type_areas):
    print("\nRice Type Area Percentages:")
    total_grain_type_area = sum(grain_type_areas.values())
    for name, area in grain_type_areas.items():
        percentage = (area / total_grain_type_area) * 100 if total_grain_type_area > 0 else 0
        print(f"{name}: {percentage:.2f}%")
