# References

Here i list the references used with links and a short summary  

## [LogMine: Fast Pattern Recognition for Log Analytics](https://dl.acm.org/doi/abs/10.1145/2983323.2983358?casa_token=TUDwpnFeE4kAAAAA%3AtguThY1z7Q1x94ryHZ0p4p0KN03XGetfulfaxbONmr9gBaAK9kPxEz0n3o2bfDikaxJSHTfBJmpx)

## [Advances and Challenges in Log Analysis](https://dl.acm.org/doi/10.1145/2076450.2076466)

Logs contain a wealth of information to help manage systems.

### Zitate

*Introduction*  
`Log analysis is a rich field of research;`

`As Brian Kernighan wrote in Unix for Beginners in 1979, “The most effective debugging tool is still careful thought, coupled with judiciously placed print statements.”`  
  
`The static interleaving scenario is more challenging because different modules may be written by different developers.`  
Static interleaving scenarios, as in a data graveyards, are more challinging.
As one place receiving messages from multiple data source have different interpretions and level of serverty.
For example a connection lost message from a system networking libary has a different implication compared to such a message coming from an application layer.

`Some users need aggregated or statistical information and not individual messages.`  
(PCA / SVM analysis in distrebuted systems where aquiring log data is expensive)

*Prediction*  
`Machine-learning techniques, especially anomaly detection, are commonly used to discover interesting log messages.`  
For such means the logs need to be fed in the form of feature vectors.  
`Extracting feature vectors from events logs is a nontrivial, yet  ritical, step that affects the effectiveness of a predictive model.`

*Reporting and Profiling*  
`Another use for log analysis is to profile resource utilization, workload, or user behavior.`  
`Clustering algorithms such as k-means and hierarchical clustering group similar events.`  
`Markov chains have been used for pattern mining where temporal ordering is essential.`  

*Conclusion*  
`For example, statistical techniques could reveal an anomaly in the workload or that the system’s CPU utilization is high but not explain what to do about it.`  
