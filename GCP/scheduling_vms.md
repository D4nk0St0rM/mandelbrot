### How to schedule VM start n stop

##### Create the start function [One time only per project]

- Cloud Functions 
- Create Function.
  - startInstancePubSub.
- Memory allocated - LEAVE 
- Trigger: Cloud Pub/Sub.
- Topic, Create new topic....
  - Name: start-instance-event.
  - Create
- Runtime: Node.js 6.
  - index.js tab.
  - package.json tab.
- For Function to execute: startInstancePubSub.
- Create


##### Create the stop function [One time only per project]
- Create Function.
  - stopInstancePubSub.
- Leave Memory allocated
- Trigger
  - Cloud Pub/Sub.
- Topic - Create new topic....
  - Name: stop-instance-event.
  - Create
 - Runtime: Node.js 6.
    - index.js tab.
    - package.json tab.
- For Function to execute, stopInstancePubSub.
- Click Create.




#### Set up the Cloud Scheduler jobs to call Cloud Pub/Sub [Per VM you wish to shut down]

##### Create the start job

- Cloud Scheduler 
- Create Job.
- Name: startup-mmlinuxvm [based on your VM instance]
- For Frequency, enter 0 9 * * 1-5. [Linked to website to help determine range you wish to use)
- Target: Pub/Sub.
- Topic: start-instance-event.
- Payload, [based on your criteria for your VM]
  - {"zone":"europe-west2-c","instance":"mmlinuxvm"}
- Create.


##### Create the stop job

- Cloud Functions
- Create Job.
- Name: shutdown-mmlinuxvm [based on your VM]
- For Frequency, enter 0 9 * * 1-5. [Linked to website to help determine range you wish to use)
- Target: Pub/Sub.
- Topic: stop-instance-event.
- Payload, enter the following [based on your VM criteria]
  - {"zone":"europe-west2-c","instance":"linuxvm"}
- Create.
