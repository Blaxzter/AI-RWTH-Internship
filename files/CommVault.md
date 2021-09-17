# Commvault

## Backup & Recovery
Data Protection, automated backup and recovery of different systems

## Disaster Recovery
Easy to use data recovery tool

## Commvault Command Center
Web UI to interact with all service provided by Commvault
YOu can start backupos, do file recovery, and so on..

### Commvault Cloud
Free cloud service that stores the last 7 Backups to a offsite location that can be restored.

### Storage
Disk, Cloud and Tape storage... 
Each type of storage can be connected to a media agent throuhg either network or direct attachment
 
#### NAS (Network Attached Storage)
IIs a storage that is attached through a network device
When using network attached storange with 
#### SAN (Storage Area Network)
Media Agents can use shared disk storage.. more scalable then DAS  
If a media Agent fails the data can be unaccassible till the media agent is back online
### DAS 
Simplist storage solution.. If media agent crashes the data is unaccassible


## Disaster Recovery
Consider Bandwidth when stuff is stored on offsite locations

## DeDublication
Layer that stores the same data only once 
Memory Buffer.. Dedublication Database  
Backups are shorter as only new and changed blocks are stored

Deduplication Signiture is used as a lookup 