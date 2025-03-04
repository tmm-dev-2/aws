import subprocess
import sys

class PackageManager:
    def __init__(self):
        self.required_packages = [
            'yfinance',
            'pandas',
            'numpy',
            'ta-lib',
            'scikit-learn',
            'tensorflow',
            'plotly',
            'matplotlib'
        ]

    def install_package(self, package):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return True
        except:
            return False

    def install_requirements(self):
        for package in self.required_packages:
            print(f"Installing {package}...")
            if self.install_package(package):
                print(f"Successfully installed {package}")
            else:
                print(f"Failed to install {package}")
