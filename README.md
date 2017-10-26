# EPIC to REDCap Normalization
This is a program used to take data we pulled from EPIC using an automated data pull, and normalizing the data so that
it can be uploaded into REDCap. During this process we generate 3 files.
-   Coordinator File
    - This file informs the research coordinator what data was found using the automated data pull. This is necessary
    because some data pull automatically still requires further interpretation by the coordinator. This file allows the
    coordinator to easily det
-   REDCap Label File
    - This file contains the normalized data in it's Labeled (human readable) form. This is primarily for the
     data manager who will be responsible for uploading this data into REDCap. If there are ever any issues with
     uploading the raw file, the data manger can use this file to see where the issues may be coming from.
-   REDCap Raw File
    - This file contains the normalized data in it's Raw (machine readable) form. This is the file that will be uploaded
    into REDCap
