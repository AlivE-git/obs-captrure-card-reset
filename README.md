# obs-captrure-card-reset
This script automatically resets the capture card when the resolution is changed.
[Video demonstration.](https://www.youtube.com/watch?v=VgwOHDZtF7Y)
## Installation
1. Download and install [python](https://www.python.org/downloads/);
2. Install package "pygrabber":
```
pip install pygrabber
```
3. Run OBS, Tools - Scripst - Python Settings. Specify the installation path. Example:
```
C:/Users/user/AppData/Local/Programs/Python/Python310
```
4. Add and configure the script. You can add and configure GDI+ text source to display the resolution on the screen. The script interacts only with the source text.