# [A Survey of Outlier Detection Methods in Network Anomaly Identification](https://www.researchgate.net/publication/220459044_A_Survey_of_Outlier_Detection_Methods_in_Network_Anomaly_Identification)

## Quotes

`For example, an anomalous traffic pattern in a computer network could mean that a hacked computer is sending out sensitive data to an unauthorized destination.`

`Moreover, in many cases, it is not a priori known what objects are outliers.`
```
In order to apply outlier detection to anomaly based network intrusion detection, it is assumed [10] that -

1.  The majority of the network connections are
    normal traffic. Only a small amount of traffic is
    malicious.
2.  Attack traffic is statistically different from normal
    traffic.
```


# [Outlier Detection: Methods, Models, and Classification](https://dl.acm.org/doi/abs/10.1145/3381028?casa_token=J86tGfDzJwEAAAAA%3A44shV8Pmni8uTfxcY2cqxlVHSX8es8_DkZE7ToNsq6mqYI9FDDeATizr3jzUUfkGKEG-lGrrqdHe)

## Quotes
Challenges:  
`Thus outlier detection faces new challenges: identifying outliers in data with extremely high dimensionality, in unbounded large volumes of data streams, and in distributed data of  large scales, and so on.`

Starter Quote:  
`The first definition of the outlier is likely attributable to Grubbs in 1969 [19], “an outlier is one that appears to deviate markedly from other members of the sample in which it occurs.”`

Basically the same block quote as in the first paper:  
`Outliers are defined typically based on the following assumptions [21]: (1)  Outliers are different from the norm with respect to their features; (2) outliers are rare in a dataset compared to normal instances.`

There a three kinds of outlier detection:  
`Based on the availability of the input data’s labels, outlier detection methods can be categorized into three types: (1) supervised outlier detection, (2) semi-supervised outlier detection, and (3) unsupervised outlier detection.`

What happens if the data set becomes to big:  
`Put in another way, using small samples reduces the masking effect where outlier instances forming clusters are mistakenly regarded as normal instances [16, 28].`

## Methods of outlier detection
### Proximity Based Approaches
Outlier are located in sparse data area.
The nearest data points are very far away.
It can be detiermined by using nearest neighbors and clustering algorithms.   
Nearest neighborhood can be defined using k nearest neigbors or a radious centered by a data point. 
-> Normal data forms a populated area while outliers are far from their neighbors.

LOF: `the LOF score of p is the average ratio of p’s neighbors’ density to p’s density.`  
COF: Chaning distance (`which can be viewed as the shortest path connecting the k neighbors and the data instance.`) normalized by the average of the chaining distance of its k-NN.  
Local Correlation Integral (LOCI): Calculate point based distance density (MDEF) and the standard deviation.. If MDEF > 3 * lambda MDEF then outlier... O(n^3) no parameter for k in k-NN  
Influenced Outlierness (INFLO): The k-RNN is `the set of other instances whose k-nearest neighborhood includes p.` LOF fails to appropriately score the instances on the borders of clusters with significantly different densities. Therfore the k-RNN inclusion   
LocalOutlier Probability (LoOP): It is assumed that a data point p is at the center of its neighborhood, and the distances to its k-NN follow a half-Gaussian distribution

# [Outlier Detection Using Replicator Neural Networks](https://link.springer.com/chapter/10.1007/3-540-46145-0_17)
Paper that uses AE or in their terms RNN Replicatior Neural Networks to calculate a outlier score based on the mean square error.   
Shown with 2 data sets 1999 KDD Cup network and Wisconsin Breast Cancer Dataset.  
They had do split the log data into respective categories and combine some fields.   
Their network is relativly small compared to modern aproaches..


# [LogMine: Fast Pattern Recognition for Log Analytics](https://dl.acm.org/doi/abs/10.1145/2983323.2983358?casa_token=TUDwpnFeE4kAAAAA%3AtguThY1z7Q1x94ryHZ0p4p0KN03XGetfulfaxbONmr9gBaAK9kPxEz0n3o2bfDikaxJSHTfBJmpx)

A log analyzer must have a `recognize` and a `match` component for patterns to identify events and anomalies.
Desirable properties: No supervision (Work from scratch), Heterogeneity (Different sources must work), Efficiency, Scalability.
Prev approach: regex is doof.

Tokenization -> White Space separation and replacing common patterns like ip, date, number .. with tokens as to not create unnecessary patterns
Define distance on Sentences simple token match distance

More for finding clusters in heterogenous locations with quite simple methods.  

# [Advances and Challenges in Log Analysis](https://dl.acm.org/doi/10.1145/2076450.2076466)

Logs contain a wealth of information to help manage systems.

## Zitate

*Introduction*  
`Log analysis is a rich field of research;`

`As Brian Kernighan wrote in Unix for Beginners in 1979, “The most effective debugging tool is still careful thought, coupled with judiciously placed print statements.”`  
  
`The static interleaving scenario is more challenging because different modules may be written by different developers.`  
Static interleaving scenarios, as in a data graveyards, are more challenging.
As one place receiving messages from multiple data source have different interpretations and level of severity.
For example a connection lost message from a system networking library has a different implication compared to such a message coming from an application layer.

`Some users need aggregated or statistical information and not individual messages.`  
(PCA / SVM analysis in distributed systems where acquiring log data is expensive)

*Prediction*  
`Machine-learning techniques, especially anomaly detection, are commonly used to discover interesting log messages.`  
For such means the logs need to be fed in the form of feature vectors.  
`Extracting feature vectors from events logs is a nontrivial, yet  critical, step that affects the effectiveness of a predictive model.`

*Reporting and Profiling*  
`Another use for log analysis is to profile resource utilization, workload, or user behavior.`  
`Clustering algorithms such as k-means and hierarchical clustering group similar events.`  
`Markov chains have been used for pattern mining where temporal ordering is essential.`  

*Conclusion*  
`For example, statistical techniques could reveal an anomaly in the workload or that the system’s CPU utilization is high but not explain what to do about it.`  


# [Towards structured log analysis](https://ieeexplore.ieee.org/abstract/document/6261962)

Shows different requirements a logging analyser requires  
Goes over a few commercial and shows their core usage
Highlights the importance of structured (XML JSON or loosely) log data

Talks about a method of finding less frequent log patterns using PCA

## Quotes

`Furthermore, system breaches can be more easily identified by using security warning logs.`
`One popular use for application log analysis is anomaly detection.`  


# [Combining K-Means and XGBoost Models for Anomaly Detection Using Log Datasets](https://www.mdpi.com/2079-9292/9/7/1164)

## Quotes

`By definition, an anomaly is an outlying observation that appears to deviate markedly from other members`

# [Online System Problem Detection by Mining Patterns of Console Logs](https://ieeexplore.ieee.org/abstract/document/5360285?casa_token=9RSaCnMCKasAAAAA:nSTgb22paHWNcd7m7aR2uBiBHsNuzqDK0zK9zrX5QgNYrUJ7PKCqxDhrGJXM1cyWt3FYQqEV)




