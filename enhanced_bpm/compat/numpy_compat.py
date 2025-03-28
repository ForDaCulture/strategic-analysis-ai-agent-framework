"""
NumPy compatibility layer

This module provides a compatibility layer for NumPy that:
1. Suppresses binary incompatibility warnings
2. Provides fallback functionality when NumPy is not available
3. Handles version differences gracefully
"""

import warnings
import importlib.util
import sys
import os
import platform

# Suppress all NumPy-related warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ImportWarning)

# Check if NumPy is available
numpy_available = importlib.util.find_spec("numpy") is not None

# If NumPy is available, import it
if numpy_available:
    try:
        import numpy as np
        NUMPY_VERSION = np.__version__
        HAS_NUMPY = True
    except ImportError:
        HAS_NUMPY = False
        NUMPY_VERSION = None
else:
    HAS_NUMPY = False
    NUMPY_VERSION = None
    
    # Create a minimal NumPy-like module for basic functionality
    class MinimalNumPy:
        """A minimal NumPy-like class that provides basic functionality."""
        
        def __init__(self):
            self.nan = float('nan')
            self.inf = float('inf')
            
        def array(self, data, dtype=None):
            """Create a simple array (just returns the data)."""
            return data
            
        def mean(self, data, axis=None):
            """Calculate the mean of a list of numbers."""
            if not data:
                return 0
            if isinstance(data[0], (list, tuple)):
                # Handle 2D arrays
                if axis == 0:
                    # Mean of each column
                    result = []
                    for i in range(len(data[0])):
                        col = [row[i] for row in data]
                        result.append(sum(col) / len(col))
                    return result
                elif axis == 1:
                    # Mean of each row
                    return [sum(row) / len(row) for row in data]
                else:
                    # Overall mean
                    flat = [item for sublist in data for item in sublist]
                    return sum(flat) / len(flat)
            return sum(data) / len(data)
            
        def std(self, data, axis=None):
            """Calculate the standard deviation."""
            if not data:
                return 0
            
            if isinstance(data[0], (list, tuple)):
                # Handle 2D arrays
                if axis == 0:
                    # Std of each column
                    result = []
                    for i in range(len(data[0])):
                        col = [row[i] for row in data]
                        mean = sum(col) / len(col)
                        variance = sum((x - mean) ** 2 for x in col) / len(col)
                        result.append(variance ** 0.5)
                    return result
                elif axis == 1:
                    # Std of each row
                    result = []
                    for row in data:
                        mean = sum(row) / len(row)
                        variance = sum((x - mean) ** 2 for x in row) / len(row)
                        result.append(variance ** 0.5)
                    return result
                else:
                    # Overall std
                    flat = [item for sublist in data for item in sublist]
                    mean = sum(flat) / len(flat)
                    variance = sum((x - mean) ** 2 for x in flat) / len(flat)
                    return variance ** 0.5
            
            mean = sum(data) / len(data)
            variance = sum((x - mean) ** 2 for x in data) / len(data)
            return variance ** 0.5
        
        def zeros(self, shape, dtype=None):
            """Create an array of zeros."""
            if isinstance(shape, (list, tuple)):
                if len(shape) == 1:
                    return [0] * shape[0]
                elif len(shape) == 2:
                    return [[0 for _ in range(shape[1])] for _ in range(shape[0])]
            return [0] * shape
        
        def ones(self, shape, dtype=None):
            """Create an array of ones."""
            if isinstance(shape, (list, tuple)):
                if len(shape) == 1:
                    return [1] * shape[0]
                elif len(shape) == 2:
                    return [[1 for _ in range(shape[1])] for _ in range(shape[0])]
            return [1] * shape
        
        def arange(self, start, stop=None, step=1):
            """Create a range of numbers."""
            if stop is None:
                stop = start
                start = 0
            return list(range(start, stop, step))
        
        def reshape(self, arr, shape):
            """Reshape an array (simplified)."""
            if not arr:
                return arr
            
            # Flatten the array
            flat = []
            if isinstance(arr[0], (list, tuple)):
                for row in arr:
                    flat.extend(row)
            else:
                flat = arr
            
            # Reshape
            if len(shape) == 1:
                return flat[:shape[0]]
            elif len(shape) == 2:
                result = []
                for i in range(shape[0]):
                    row = flat[i*shape[1]:(i+1)*shape[1]]
                    result.append(row)
                return result
            return flat
    
    # Create a fake NumPy module
    np = MinimalNumPy()
    sys.modules['numpy'] = np

def get_numpy():
    """Get the NumPy module (real or minimal compatibility layer)."""
    if HAS_NUMPY:
        import numpy as np
        return np
    else:
        return np

def is_numpy_available():
    """Check if real NumPy is available."""
    return HAS_NUMPY

def get_numpy_version():
    """Get the NumPy version if available."""
    return NUMPY_VERSION

def check_numpy_compatibility():
    """Check NumPy compatibility and return a status message."""
    python_version = platform.python_version()
    
    if not HAS_NUMPY:
        return {
            "status": "not_available",
            "message": f"NumPy is not installed. Using compatibility layer with limited functionality.",
            "python_version": python_version,
            "numpy_version": None
        }
    
    # Check if we're using a compatible version
    try:
        import numpy as np
        # Try a simple operation to check compatibility
        test_array = np.array([1, 2, 3])
        test_mean = np.mean(test_array)
        
        return {
            "status": "compatible",
            "message": f"NumPy {np.__version__} is compatible with Python {python_version}.",
            "python_version": python_version,
            "numpy_version": np.__version__
        }
    except Exception as e:
        return {
            "status": "incompatible",
            "message": f"NumPy is installed but incompatible: {str(e)}",
            "python_version": python_version,
            "numpy_version": NUMPY_VERSION,
            "error": str(e)
        }