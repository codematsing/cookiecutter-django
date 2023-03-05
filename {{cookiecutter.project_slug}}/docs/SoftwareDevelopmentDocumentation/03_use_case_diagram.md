# Use Case Diagram
A Use Case Diagram is a graphical representation of the interactions between a system and its users, known as actors. It is used to capture the functional requirements of a system and to model the user's interactions with that system.

A use case diagram consists of three main elements:

- Actors: Represent the users of the system, including external entities such as people, organizations, or other systems.

- Use Cases: Represent the functions or services provided by the system to its actors. Each use case is a sequence of actions that the system performs to achieve a specific goal for the actor.

- Relationships: Show the relationships between actors and use cases, including generalization (an actor can perform multiple use cases), include (one use case includes the functionality of another), and extend (a use case extends the functionality of another).

There are three main relationships in a use case diagram:

- Generalization: This relationship indicates that one actor can perform multiple use cases.
- Include: This relationship indicates that one use case includes the functionality of another use case.
- Extend: This relationship indicates that a use case extends the functionality of another use case.

These relationships help to organize and simplify the use cases by showing how they are related and dependent on each other. Understanding these relationships is important for identifying potential problems and for making design decisions.

Use case diagrams are useful for defining the scope of a system, understanding the requirements of the users, and for communication between stakeholders. They provide a high-level view of the system and are useful for identifying potential problems early in the development process.

Refer to [PlantUML Documentation](https://plantuml.com/use-case-diagram)

``` plantuml
@startuml
' Define the actors
left to right direction
actor User

' Define the use cases
Rectangle "Todo App" as app {
    usecase "Add Task" as create
    usecase "View Tasks" as read
    usecase "Edit Task" as update
    usecase "Delete Task" as delete
}

' Connect the actors to the use cases
User -r-> create
User -r-> read
User -r-> update
User --> delete

@enduml
```
