# Package Diagram
A package diagram is a UML diagram that shows the structure of a software system by grouping related elements into packages. A package is a container that can hold other packages, classes, interfaces, and other types of elements. Package diagrams are useful for organizing and managing large systems by breaking them down into smaller, more manageable components.

In a package diagram, packages are represented by rectangles with a folded corner, and the name of the package is written inside the rectangle. Packages can be connected by dependency, association, generalization, or other types of relationships to show how they relate to each other.

Packages can also contain other packages, which can be represented by nested rectangles inside the main package. The contents of a package can be shown using the package contents notation, which lists the elements inside the package using a tree-like structure.

Package diagrams are useful for visualizing the high-level structure of a software system, and for organizing the system into modular components that can be developed and tested separately. They can also help to identify dependencies between packages, and to ensure that each package has a clear and well-defined responsibility within the system.

There are two sub-types involved in dependency. They are <<import>> & <<access>>. Though there are two stereotypes users can use their own stereotype to represent the type of dependency between two packages.

`<<import>>` - one package imports the functionality of other package
`<<access>>` - one package requires help from functions of other package.

Refer to [PlantUML Documentation](https://plantuml.com/component-diagram)

![Sample Package Diagram](https://cdn-images.visual-paradigm.com/guide/uml/what-is-package-diagram/11-use-of-import.png)
