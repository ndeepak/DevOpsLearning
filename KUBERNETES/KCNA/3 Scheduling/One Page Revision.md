# One Page Revision
# 3) One-Page Revision Notes Sheet (Final)
## Kubernetes Scheduling – Quick Revision

### Scheduler Basics
- Scheduler assigns pods to nodes    
- Default scheduler name: `default-scheduler`    
- Scheduler writes `nodeName`    

---
### Multiple Schedulers
- Multiple schedulers can run    
- Each scheduler has a unique name    
- Pod selects scheduler using `schedulerName`    
- If scheduler not running → pod Pending    

---
### Custom Scheduler
- Same kube-scheduler binary    
- Own config file    
- Own schedulerName    
- Runs alongside default scheduler    

---
### Leader Election
- Required for HA schedulers    
- Only leader schedules pods    
- Uses Lease objects    

---
### Scheduler Extender
- External HTTP service    
- Used by default scheduler    
- Filters or scores nodes    
- Does not schedule pods directly    

---
### Common Exam Traps
- Default scheduler is used unless overridden    
- Schedulers do not compete for pods    
- SchedulerName must match exactly    
- Pending pod often means scheduler issue    

---
### One-line Memory Rules
- Pod chooses scheduler, not the cluster    
- Default scheduler is fallback    
- Custom scheduler is opt-in    
- Extenders advise, schedulers decide    

---