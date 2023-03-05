# Class Diagram
A Class Diagram represents the classes, objects, and their relationships in a system. It provides a blueprint of the classes and their attributes, operations, and relationships with other classes.

A class diagram consists of several elements, including:

- Classes: Represent the objects and entities in a system, and are represented as rectangles.
- Attributes: Represent the data or properties of a class, and are represented as a list of variables within the class rectangle.
- Operations: Represent the behavior or actions of a class, and are represented as a list of methods within the class rectangle.
- Relationships: Represent the relationships between classes, such as inheritance, aggregation, composition, and association. They are represented as arrows connecting classes.

Class diagrams are useful for understanding the structure of a system and for illustrating the relationships between classes.

Refer to [PlantUML Documentation](https://plantuml.com/class-diagram)

``` plantuml
@startuml
class Todo {
  -id: int
  -title: string
  -description: string
  -due_date: date
  -status: string
  +get_id(): int
  +set_id(id: int): void
  +get_title(): string
  +set_title(title: string): void
  +get_description(): string
  +set_description(description: string): void
  +get_due_date(): date
  +set_due_date(due_date: date): void
  +get_status(): string
  +set_status(status: string): void
}

class TodoList {
  -todos: List<Todo>
  +add(todo: Todo): void
  +remove(todo: Todo): void
  +get_all(): List<Todo>
  +get_by_status(status: string): List<Todo>
  +get_by_due_date(date: date): List<Todo>
}

class User {
  -id: int
  -username: string
  -password: string
  -email: string
  +get_id(): int
  +set_id(id: int): void
  +get_username(): string
  +set_username(username: string): void
  +get_password(): string
  +set_password(password: string): void
  +get_email(): string
  +set_email(email: string): void
}

class UserManager {
  -users: List<User>
  +add(user: User): void
  +remove(user: User): void
  +get_all(): List<User>
  +get_by_username(username: string): User
}

TodoList --> Todo
UserManager --> User
@enduml
```
