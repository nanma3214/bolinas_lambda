# Guide to Maintain (the Nontechnical Part of) AWS S3

## Overview
**AWS S3** &rightarrow; Cloud storage for
* Bolinas traffic simulation data
* Bolinas Resilience - Wildfire Evacuation Simulation in-game survey data
  
The data is stored in AWS S3 bucket (containers for data) named **bolinas**. The file structure is as follows:
```
bolinas(bucket name)
└─── player_nodes (folder for Bolinas traffic simulation data)
│   └─── <simulation data stored by user ID>
│   │   ...
└─── survey_answer (folder for Bolinas Resilience in-game survey data)
│   │   answers.csv
```
&nbsp;

## Download the in-game survey data
1. Log in to [AWS console](https://aws.amazon.com/console/).
2. Click on the **services** tab at the top left corner, and choose **S3** under the **Storage** catagory to get into AWS S3 site.
3. Click the S3 bucket named **bolinas**, and then click on the folder **surveu_answer/**. There should be a file named `answers.csv`. 
4. Click on the file `answers.csv` to get to the file info page. On the top right corner of the page, click **Download** or **Open** to download the file to local computer.
5. Open the csv file with Excel or other software. The first two colomns are the **timestamp** of the survey in UTC, and the **user ID** internally generated for each player. Other columns are orders in pairs of 
   * **nodes**: the number label for the road intersection in Bolinas map, 
  
        and
   * **comments**: player input of either stay on the same course, or the reason to choose a different path.

&nbsp;

## Clean the Bolinas traffic simulation data regularly
Currently the Bolinas traffic simulation running at the backend of the simulation game stores the intermediate data at S3 under `bolinas/player_nodes/`. Manually logging into S3 to clean those data could be a solution to avoid large bills if the data reaches 50 TB level.

_A [Lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html) is setup for the **bolinas** bucket to automatically remove simulation data in 13 days. The effect is currently under study._

&nbsp;

## For technical details...
Refer to [this repository](https://github.com/nanma3214/bolinas_lambda).