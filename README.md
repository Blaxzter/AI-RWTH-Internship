# AI-RWTH-Internship

Repository for my internship at the RWTH as an elective internship from the university in Maastricht.


## Abstract

Universities and organisations in education have increasingly become the target of cyberattacks due to their large attack vector. 
File servers that form the backbone of the different working processes are the primary target of these attacks. 
In the face of these dangers, data protection in the form of consecutive incremental backups is required. 
This internship’s primary goal was to develop a machine learning tool capable of finding malicious activities that occurred on a secured file server by classifying the backups metadata into the respective normal mode and or being an outlier.

To archive this goal, different unsupervised outlier detection methods were researched, combined with the selection of two suitable techniques matching the requirements. 
The first approach uses state of the art outlier detection ensemble method SUOD on extracted and vectorised backup metadata, with the second approach addressing how path data of the individual files are parsed into multisets and used in One-Class Support Vector Machines. 
This internship further addressed a design concept for deploying the components of the ml-tool, including a web interface for visualising and interacting, a backend API and a database for persistent storing and continuously training the models on new data.

The evaluation of is these approaches on commit data of a large git project parsed into backup formats showed how the two methods classified the backups by their respective features and isolated different characteristics as outliers. 
The models further provide an outlier probability coupled with the model’s certainty for the prediction.
