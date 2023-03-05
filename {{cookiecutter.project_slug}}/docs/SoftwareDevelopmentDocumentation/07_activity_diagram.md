# Activity Diagram

An Activity Diagram represents the flow of activities in a system. It provides a visual representation of the steps involved in a process or activity, and the flow of control between these steps.

An activity diagram consists of several elements, including:

- Activities: Represent the steps or tasks involved in a process or activity. They are represented as rounded rectangles.
- Transitions: Represent the flow of control between activities. They are represented as arrows connecting activities.
- Decision nodes: Represent decisions or branches in the flow of control. They are represented as diamonds.
- Initial and final nodes: Represent the starting and ending points of a process or activity. The initial node is represented as a filled circle, and the final node is represented as a bull's eye.
- Swimming lanes: Represent the partitioning of activities into pools, which represent different participants or roles in the process or activity.

Activity diagrams are useful for modeling the flow of control in a system and for understanding the relationships between activities.

Refer to [PlantUML Documentation](https://plantuml.com/activity-diagram-beta)

``` plantuml
@startuml
|Swimlane 1|
start
if (Task assigned?) then (yes)
  |Swimlane 3| 
  :Do the task;
  |Swimlane 2| 
  :Task Completed;
else (no)
  |Swimlane 2| 
  :Task Not Assigned;
endif
stop
@enduml
```
