# References

Here i list the references used with links and a short summary  

## [LogMine: Fast Pattern Recognition for Log Analytics](https://dl.acm.org/doi/abs/10.1145/2983323.2983358?casa_token=TUDwpnFeE4kAAAAA%3AtguThY1z7Q1x94ryHZ0p4p0KN03XGetfulfaxbONmr9gBaAK9kPxEz0n3o2bfDikaxJSHTfBJmpx)

A log analyzer must have a `recognize` and a `match` component for patterns to identify events and anomalies.
Desirable properties: No supervision (Work from scratch), Heterogeneity (Different sources must work), Efficiency, Scalability.
Prev approach: regex is doof.

Tokenization -> White Space separation and replacing common patterns like ip, date, number .. with tokens as to not create unnecessary patterns
Define distance on Sentences simple token match distance

More for finding clusters in heterogenous locations with quite simple methods.  

## [Advances and Challenges in Log Analysis](https://dl.acm.org/doi/10.1145/2076450.2076466)

Logs contain a wealth of information to help manage systems.

### Zitate

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


## [Towards structured log analysis](https://ieeexplore.ieee.org/abstract/document/6261962)

Shows different requirements a logging analyser requires  
Goes over a few commercial and shows their core usage
Highlights the importance of structured (XML JSON or loosely) log data

Talks about a method of finding less frequent log patterns using PCA

### Quotes

`Furthermore, system breaches can be more easily identified by using security warning logs.`
`One popular use for application log analysis is anomaly detection.`  


## [Combining K-Means and XGBoost Models for Anomaly Detection Using Log Datasets](https://www.mdpi.com/2079-9292/9/7/1164)

### Quotes

`By definition, an anomaly is an outlying observation that appears to deviate markedly from other members`

## [Online System Problem Detection by Mining Patterns of Console Logs](https://ieeexplore.ieee.org/abstract/document/5360285?casa_token=9RSaCnMCKasAAAAA:nSTgb22paHWNcd7m7aR2uBiBHsNuzqDK0zK9zrX5QgNYrUJ7PKCqxDhrGJXM1cyWt3FYQqEV)

















