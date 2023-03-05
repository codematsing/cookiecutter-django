# Deployment Diagram

A Deployment Diagram represent the physical deployment of software components and hardware components in a system. It provides a visual representation of the mapping of software components to hardware components, such as servers, databases, and clients.

A deployment diagram consists of several elements, including:

- Nodes: Represent the hardware components in a system, such as servers, clients, or databases. 
- Components: Represent the software components in a system, such as modules, libraries, or executables. 
- Communication Paths: Represent the communication between nodes, such as network connections or communication protocols. 
- Artifacts: Represent the physical files that are generated or deployed as part of the system, such as executables or configuration files.

Deployment diagrams are useful for understanding the physical deployment of software components and hardware components in a system. They can be used in a variety of domains, including software development, system design, and architecture.

``` plantuml
@startuml

node "Web Server" {
    component "Todo App Web" as todo_web
}

node "Application Server" {
    component "Todo App API" as todo_api
}

node "Database Server" {
    database "Todo App Database" as todo_db
}

todo_web -> todo_api : HTTP Request
todo_api -> todo_db : Database Query

@enduml
```

## Tech Stack
A tech stack is the combination of technologies a company uses to build and run an application or project. Sometimes called a “solutions stack,” a tech stack typically consists of programming languages, frameworks, a database, front-end tools, back-end tools, and applications connected via APIs.