# Entity Relationship Diagram
An Entity Relationship Diagram (ERD) is a graphical representation of entities and their relationships to each other, used in database design. It provides a high-level view of the structure of a database, including entities and the relationships between them.

An ERD consists of three main components:

- Entities: Represent objects or concepts in the real world, such as customers, orders, or products.

- Attributes: Represent characteristics or properties of an entity, such as name, address, or date of birth.

- Relationships: Represent the relationships between entities, such as a customer placing an order or a product being part of an order. Relationships can be one-to-one, one-to-many, or many-to-many.

ERDs are used to define the structure of a database and to communicate the relationships between entities to stakeholders. They are an important tool in database design, helping to ensure that the database is properly structured to support the needs of the system. ERDs can also be used to identify potential data redundancies, improve data integrity, and simplify database maintenance.

Refer to [PlantUML Documentation](https://plantuml.com/ie-diagram)

``` plantuml
@startuml
entity Task {
  +id : int
  description : string
  due_date : date
  is_completed : bool
}

entity Category {
  +id : int
  name : string
}

entity User {
  +id : int
  username : string
  password : string
}

Task ||--|| Category
Task }o--|| User
@enduml
```