# Film Production Scheduler

This is a Final Year Project submitted as course requirements for IEDA 4920 at HKUST, co-developed by Tsz Hei Louey, Hin Yeung AU, and Hang Kin Nicholas YUEN, under the supervision of Mr. Eugene CHAN from EuCan Productions and Professor Xuan QIU.

## Authors

- [Tsz Hei (Newton) LOUEY](https://www.github.com/codingnewton)
- [Hin Yeung AU](https://www.github.com/hyauaj)
- [Hang Kin Nicholas YUEN](https://www.github.com/nicholashkyuen)

## Acknowledgements

 - [Professor Xuan QIU](https://seng.hkust.edu.hk/about/people/faculty/xuan-qiu)
 - [EuCan Productions](https://www.eucanproductions.com/)

## Installation

The application can be downloaded through the [release v1.0](https://github.com/codingnewton/FilmProductionScheduler/releases/tag/v1.0). The executable is only intended for Window users. For MacOS or Linux, please refer to the guidelines in Deployment for creating an app. 

After unzipping the file, FilmScheduler.exe can be found within the folder FilmScheduler. Please retain the file structure of all the folders.
If you wish open the app through another directory, please create a shortcut from your intended directory to the FilmScheduler.exe file.

Individuals may also use the solution directly through our source code by the following two methods.

**`main.py`** initiates a basic UI. It is same as the release

**`schedule_optimizer.py`** contains the raw code without the UI. Users have to specify the variables `excel_file` and `output_location` before running


## Deployment

Users are required to intialized their input via an Excel File. An example excel file `Member&Task_Info.xlsx` was included in the folder. There is no restriction to the naming of the excel file. However, the sheets names and initialization format has to be retained for the solution to work properly. 

Users may also create their own application by running the file `build_app.py`. Depending on the environment where you create the app, the app will become native to the environment. I.e., Window environment will create only a Window executable. 
After running `build_app.py`, two new folders will be created, namely `build` and `dist`. Please find the package `FilmScheduler` within the `dist` folder. 
