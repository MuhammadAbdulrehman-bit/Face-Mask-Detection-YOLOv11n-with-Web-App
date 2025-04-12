# Face Mask Detection System

A real-time face mask detection system using **YOLOv8** to identify whether a person is wearing a mask. Violations (no mask) trigger alerts, image captures, and logging.

---

## Features
- Real-time detection via webcam using **YOLOv8**.
- Audible alert (`winsound.Beep`) for violations.
- Automatic logging of violations to `violations_log.csv`.
- Saves violation snapshots in `violations/` folder.
- **Streamlit dashboard** to review logs and images.

---

## Project Structure
```bash
Face_Mask_Detection/
├── Mask_Wearing.v1i.yolov8/  # Dataset (YOLOv8 format)
├── violations/               # Saves images in Violations folder
├── Detect_capture_store.py   # Main detection script
├── App.py                    # Streamlit dashboard
├── violations_log.csv        # Logs timestamps & confidence
└── yolov8n.pt               # Custom-trained YOLOv8 model
```

## Prerequisites

To get started, you will need to install the following libaries:
```bash
pip install ultralytics opencv-python winsound streamlit pandas pillow
```

## How to Run

- First run the Detect_capture_store.py file. It will open a webcam and will start detecting.
- If you wear a mask, it will detects it as such and will not take any pictures.
- But if you are not wearing any mask, then it will start taking pictures of yours and saves it in the violations folder with timestamp saved in the violation_log.csv file.
- Then when your done with detecting, press Q to exit.
- After that, run the followin command in terminal ***streamlit run App.py***
- This will open the web application, and from there you can load any images by copying the timestamp from the file into the search bar at the bottom.


## Additional Information

- Mask Wearing.v1i.yolov8 folder contains the dataset for training the model, in case if you wanted to train the model by yourself.

- Inside the Mask Wearing.v1i.yolov8 folder, it will contain data.yaml file. When you open it, it will look like this:

```bash
train: E:\New folder\Face Mask Detection\Mask Wearing.v1i.yolov8/train/images #change the file path accordingly
val: E:\New folder\Face Mask Detection\Mask Wearing.v1i.yolov8/valid/images #change the file path accordingly
test: E:\New folder\Face Mask Detection\Mask Wearing.v1i.yolov8/test/images #change the file path accordingly
#Ignore the rest of this
nc: 2
names: ['mask', 'no-mask']

roboflow:
  workspace: muhammad-abdul-rehman-buhdh
  project: mask-wearing-uqr7d
  version: 1
  license: CC BY 4.0
  url: https://universe.roboflow.com/muhammad-abdul-rehman-buhdh/mask-wearing-uqr7d/dataset/1
```

- Once you set the file path according to the file path where the folder is stored, you need to run the following command in terminal:
  ``` bash
  yolo detect train data=data.yaml model=yolov8n.pt epochs=50 imgsz=640 #set epochs to whatever you want and imgsz should not be changed no matter what
  ```
  
- Upon completing the above step, the model will begin to train. After it has been trained, a run folder will be generated containing the best weights.

- Runs folder contains the best weights and bias for the model. If you train your model, then after training it, go to this folder and search for those ***"train"*** folders, which have ***"best.pt"***. Then in the detect file, change this code:
 
 ```bash
  model = YOLO("runs\\detect\\train2\\weights\\best.pt")
  ```
   To
  ```bash
  model = YOLO("runs\\detect\\(The train folder that contains the best weight)\\weights\\best.pt")
  ```

- Then follow the instructions above heading **How to Run** to do the rest.

## Cameara Not Working?

``` bash
cap = cv2.VideoCapture(0)  # Change `0` to `1` if using secondary camera
```

