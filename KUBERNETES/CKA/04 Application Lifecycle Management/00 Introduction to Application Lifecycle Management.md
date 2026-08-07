# Introduction to Application Lifecycle Management 
Application Lifecycle Management (ALM) in Kubernetes is about **managing an application after it has been deployed**.

Many beginners think Kubernetes' job ends after creating Pods. In reality, creating Pods is just the beginning.

Applications need to evolve continuously:
- New versions are released.
- Bugs need to be fixed.
- Security patches need to be applied.
- Traffic increases and decreases.
- Pods crash.
- Nodes fail.
- Configuration changes.
- Secrets rotate.

Kubernetes provides mechanisms to handle all of these automatically.

The major topics are:
```
Application Lifecycle Management

├── Rolling Updates
├── Rollbacks
├── Configuration Management
├── Scaling
└── Self Healing
```

