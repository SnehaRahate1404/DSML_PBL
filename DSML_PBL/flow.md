flowchart TD
    A["Start"] --> B{"Practice?"}
    B -- Yes --> C["Choose Character to Chat"]
    B -- No --> A
    C --> D{"Chat Session"}
    D --> E{"Initial Proficiency and Session Duration"}
    E --> F{"Prediction of Machine Learning Model"}
    F --> G["End"]