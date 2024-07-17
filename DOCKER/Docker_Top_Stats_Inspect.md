### Docker Commands: `top`, `stats`, and `inspect`

#### 1. `docker top`
The `docker top` command displays the running processes of a container. This is useful for checking what processes are running inside the container at any given time.
##### Syntax:
`docker top <container_name_or_id>`
##### Example:
`docker top my_container`
##### Output:
This command will output a list of processes running inside `my_container` similar to the `ps` command in Linux.
```
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                1234                5678                0                   12:34               ?                   00:00:00            /bin/bash
root                5678                1234                0                   12:35               ?                   00:00:00            sleep 1000
```
#### 2. `docker stats`
The `docker stats` command provides real-time statistics for running containers, similar to the `top` command in Linux.
##### Syntax:
`docker stats [OPTIONS] [CONTAINER...]`
- Without specifying any container, it will show stats for all running containers.
- You can also specify one or more container names or IDs to get stats for specific containers.
##### Example:
`docker stats`
or for a specific container:
`docker stats my_container`
##### Output:
This command will output statistics such as CPU usage, memory usage, network I/O, and more for the specified containers.
```
CONTAINER ID   NAME           CPU %     MEM USAGE / LIMIT    MEM %     NET I/O         BLOCK I/O       PIDS
123abc456def   my_container   0.07%     15.13MiB / 1GiB      1.48%     1.23kB / 2.34kB 12.3MB / 4.5MB  5
```
#### 3. `docker inspect`
The `docker inspect` command returns detailed information about a Docker object, such as containers, images, volumes, or networks. The output is in JSON format and includes metadata about the specified object.
##### Syntax:
`docker inspect <container_name_or_id>`
or for other Docker objects like images:
`docker inspect <image_name_or_id>`
##### Example:
`docker inspect my_container`
##### Output:
The command outputs detailed JSON data including configuration, state, network settings, mounts, etc.

```
[
    {
        "Id": "123abc456def789ghij",
        "Created": "2023-07-10T10:15:30.456789123Z",
        "Path": "/bin/sh",
        "Args": [
            "-c",
            "while true; do echo hello world; sleep 1; done"
        ],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 1234,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2023-07-10T10:15:31.123456789Z",
            "FinishedAt": "0001-01-01T00:00:00Z"
        },
        ...
    }
]
```