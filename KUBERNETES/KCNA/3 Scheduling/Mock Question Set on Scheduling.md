# 2Mock Question Set on Scheduling
We’ll do this in **three levels**:
- Basic (KCNA)
- Intermediate (Mixed)
- Exam traps    

---
## Section A: KCNA-Level Questions
### Q1
A pod does not specify `schedulerName`. Which scheduler will schedule it?
A. Custom scheduler  
B. First available scheduler  
C. default-scheduler  
D. All schedulers compete

Correct answer: **C**
Explanation: Default is always used unless overridden.

---

### Q2
What happens if a pod specifies a schedulerName that does not exist?
A. Scheduled by default scheduler  
B. Automatically changed  
C. Pod stays Pending  
D. Pod fails immediately

Correct answer: **C**

---
### Q3
Which field in the Pod spec selects a scheduler?
A. nodeName  
B. schedulingPolicy  
C. schedulerName  
D. priorityClassName

Correct answer: **C**

---
### Q4
Can multiple schedulers run in a single cluster?
A. No  
B. Only one at a time  
C. Yes  
D. Only in HA mode

Correct answer: **C**

---
## Section B: Intermediate Questions
### Q5
Two schedulers are running: default-scheduler and my-scheduler.  
A pod has this spec:
`spec:   schedulerName: my-scheduler`
Which scheduler will schedule the pod?
Correct answer: **my-scheduler**

---
### Q6
Why is leader election needed for schedulers?
Correct answer:
- To ensure **only one instance** of a scheduler actively schedules pods in HA setups
---
### Q7
Which Kubernetes component actually assigns `nodeName` to a pod?
A. kubelet  
B. scheduler  
C. controller-manager  
D. API server
Correct answer: **B**

---
## Section C: Exam Trap Questions
### Q8
Do multiple schedulers compete for the same pod?
Correct answer: **No**
Why:
- Scheduler only acts on pods with matching `schedulerName`

---
### Q9
Does a scheduler extender replace the scheduler?
Correct answer: **No**
Why:
- It only advises the default scheduler
---
### Q10
Can a DaemonSet use a custom scheduler?
Correct answer: **Yes**
Why:
- DaemonSet pods can include `schedulerName`