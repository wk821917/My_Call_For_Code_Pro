# My_Call_For_Code_Pro
A project wish to explore the relationship between moisture and slope that can be helpful to Landslides disaster

## 1.About The Sensor
The sensor just like a pole insert into the soil.
The sensor use embeded controler to monitor the parameters around the slope.
It can return some information about soil and simple enviroment parameters around,for example moisture, tilt or temperature.
Following pictures introduce some information about the sensor:
![avatar](Md_pic/E_shanjing1.png)
![avatar](Md_pic/E_shanjing4.png) ![avatar](Md_pic/E_shanjing3.png)

## 2.About The Software 
#### (1)Download the whole project
   `wget https://github.com/wk821917/My_Call_For_Code_Pro/archive/master.zip`

#### (2)Unzip the zipfile
   `unzip -o -d ./ master.zip`

#### (3)Run the Create_model script
   1.You can find the scripts in the dir My_Call_For_Code_Pro-master <br>
   2.You can run the 'Create_model.ipynb' by jupyter notebook with python3.5 kernal <br>
   3.You can also run the script by watson stdio service, the service provide python3.5 kernal <br>
   4.The notebook will connect with watson machine learning service and call the script named 'lstmtest.py' <br>
   5.The script not only create model and weight file but also made a test with a picture 
     named'pred_act.png' output,the model file and weight file will save in the cloud-object-storage.
     You can find the logfile and the picture in the current dir.
     
#### (4)Run the predict script
      cd My_Call_For_Code_Pro-master/predict_script
      python3 predict_script.py`
   The script will connect with watson machine learning service and call the script named 'lstmtest.py' <br>
   The last_time.json means the Unix time when the data update,the program will update 'last_time.json'.
     
#### (5)Download the file and plot picture
      cd ./download_script
      python downloadfile.py
  Run the 'plot_pic.ipynb' by jupyter notebook
  The file will save in the dir named 'downloadfile'
  The picture will save in the dir named 'save_pic'
    
#### (6)Use scikit-learn to do cluster and classifier
   Run the script in the 'My_Call_For_Code_Pro-master' dir named IBM_ML_KMeans_Test.ipynb and classifier_test.ipynb
   The result will save in data_dir
