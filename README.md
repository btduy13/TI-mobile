# Tape Inventory Management Mobile App

A mobile application for managing tape inventory, orders, and tracking.

## Building the APK

To build the APK for Android, follow these steps:

1. **Prepare the build package**:
   - Run the `prepare_for_build.py` script to create a zip file containing all necessary files:
     ```
     python prepare_for_build.py
     ```
   - This will create a file named `TapeInventoryMobile_build_TIMESTAMP.zip`

2. **Build using Google Colab**:
   - Open the `build_apk_colab.ipynb` notebook in Google Colab:
     - Go to [Google Colab](https://colab.research.google.com/)
     - Click on "File" > "Upload notebook"
     - Upload the `build_apk_colab.ipynb` file
   - Follow the instructions in the notebook:
     - Run the first cell to install dependencies
     - Upload the zip file created in step 1
     - Run the remaining cells to build the APK
     - Download the APK file when the build is complete

3. **Install on your Android device**:
   - Transfer the APK to your Android device
   - Enable "Install from unknown sources" in your device settings
   - Open the APK file to install the application

## Development

### Project Structure
- `main.py`: Application entry point
- `src/`: Source code directory
  - `database/`: Database models and configuration
  - `screens/`: UI screens and components
  - `utils/`: Utility functions
- `assets/`: Images and other static assets
- `requirements.txt`: Python dependencies

### Requirements
- Python 3.10+
- Kivy 2.2.1
- KivyMD 1.1.1
- SQLAlchemy
- Pillow

### Running Locally
```
python main.py
```
