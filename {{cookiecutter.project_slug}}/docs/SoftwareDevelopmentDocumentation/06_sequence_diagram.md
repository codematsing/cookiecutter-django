# Sequence Diagram
A Sequence Diagram represents the interactions between objects or components in a system. It shows the sequences of messages exchanged between objects over time, and provides a visual representation of the interactions between objects and the order in which these interactions occur.

A sequence diagram consists of several elements, including:

- Objects or components: Represent the objects or components in the system, such as classes, functions, or modules.
- Messages: Represent the interactions between objects or components. Each message is represented by an arrow pointing from the sender object to the receiver object.

Sequence diagrams are useful for capturing the interactions between objects or components in a system, and for visualizing the flow of control in the system. They ensure that the interactions between objects or components are understood and properly designed.

Refer to [PlantUML Documentation](https://plantuml.com/sequence-diagram)

``` plantuml
@startuml
actor User
participant TodoApp
participant Database

User -> TodoApp: Opens Todo App
activate TodoApp

User -> TodoApp: Creates Task
TodoApp -> Database: Saves Task
activate Database
Database --> TodoApp: Returns Task ID
deactivate Database
TodoApp --> User: Shows Task Created

User -> TodoApp: Edits Task
TodoApp -> Database: Updates Task
activate Database
Database --> TodoApp: Returns success message
deactivate Database
TodoApp --> User: Shows Task Updated

User -> TodoApp: Deletes Task
TodoApp -> Database: Deletes Task
activate Database
Database --> TodoApp: Returns success message
deactivate Database
TodoApp --> User: Shows Task Deleted

User -> TodoApp: Logs out
deactivate TodoApp
@enduml
```
