# 10 Mental Comparison Default Scheduler vs Custom Scheduler vs Scheduler Extenders
This section is about **how to THINK**, not memorize YAML.
## Big-picture mental model
> Kubernetes has **one default scheduler**,  
> may run **additional schedulers**,  
> and can optionally **extend scheduling decisions externally**.

---
## Comparison Table (Very Important)

|Aspect|Default Scheduler|Custom Scheduler|Scheduler Extender|
|---|---|---|---|
|What it is|Built-in scheduler|Another scheduler instance|External HTTP service|
|Runs where|Control plane|Control plane (or pod)|Outside scheduler|
|Binary|kube-scheduler|kube-scheduler|Your own program|
|Scheduler name|default-scheduler|Any unique name|Uses default scheduler|
|Pod selects it|Implicit|`schedulerName`|No|
|Scheduling logic|Built-in filters & scoring|Modified / custom logic|Augments existing logic|
|Replaces default?|No|No|No|
|KCNA focus|High|Medium|Low|
|CKA focus|Medium|High|High|

---
## 1. Default Scheduler (Baseline)
### Mental model
> “The normal Kubernetes brain”

What it does:
- Watches for Pending pods
- Filters nodes (taints, resources, affinity)    
- Scores nodes (spread, binpacking, etc.)    
- Picks the best node    
Key points:
- Name: `default-scheduler`
- Used when pod **does not specify** a scheduler
- One default scheduler per cluster
KCNA takeaway:
- This is what most pods use
---
## 2. Custom Scheduler (Separate Brain)
### Mental model
> “A second brain that handles specific pods”

What it is:
- Another instance of `kube-scheduler`
- Has its **own name**
- Watches **only pods that ask for it**
Key ideas:
- Runs alongside default scheduler
- Uses same API server
- Pods choose it with:
    `schedulerName: my-scheduler`

Important behavior:
- Default scheduler ignores those pods
- Custom scheduler ignores others

Use cases:
- Special workloads
- Custom placement rules
- Research / optimization   

KCNA takeaway:
- Pod explicitly asks for the scheduler
---
## 3. Scheduler Extender (Advisor Model)
### Mental model
> “Default scheduler asks an external expert for advice”

What it is:
- External HTTP service
- Called by the default scheduler
- Helps filter or score nodes
Important:
- Does not schedule pods directly
- Cannot bind pods
- Works **with** default scheduler

When used:
- Very advanced requirements    
- External systems (GPUs, licenses, network)


CKA takeaway:
- Extenders are **advanced**
- Unlikely deep YAML in KCNA
---
## One-line Mental Summary
- Default Scheduler → “Automatic”
- Custom Scheduler → “Pod chooses scheduler”
- Scheduler Extender → “Scheduler asks for help”
---
