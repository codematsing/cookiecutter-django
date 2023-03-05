# Mockups

## Sitemap

Sitemaps are important because they provide a visual representation of the structure and organization of a website or application. They help developers, designers, and stakeholders to understand the overall layout of the website or application, and how different pages or components are connected to each other. This understanding is essential for creating a clear and intuitive user experience, ensuring that users can easily navigate the website or application and find the information they need.

Refer to [PlantUML Documentation](https://plantuml.com/mindmap-diagram)

``` plantuml
@startuml

left to right direction

rectangle Home as h
rectangle Tasks as t
rectangle "Task Details" as td
rectangle "Add Task" as at

h --> t
t --> td
t --> at
h --> at

@enduml
```

## WireFrame

Tools:
* https://miro.com/ (Preferred)
* https://docs.google.com/presentation (Simplified)
* https://www.figma.com/ (Professional)

UI/UX Inspirations:
* (Simple) https://dribbble.com/shots/19298161-Simple-clean-CRUD-database-table
* (Ajax) https://dribbble.com/shots/3919705-BREAD-UI-Exploration-EDIT/attachments/10095822?mode=media
