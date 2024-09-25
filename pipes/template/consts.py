import pathlib

TEMPLATE_DIR = pathlib.Path(__file__).parent / "default"

TEMPLATE_FILES = {
    "project-creation": TEMPLATE_DIR / "project-creation.toml",
    "team-creation": TEMPLATE_DIR / "team-creation.toml",

    "model": TEMPLATE_DIR / "model.toml",
    "dataset": TEMPLATE_DIR / "dataset.toml",
    "task_planning": {
        "QAQC": TEMPLATE_DIR / "task_planning_qaqc.toml",
        "Transformation": TEMPLATE_DIR / "task_planning_transformation.toml",
        "Visualization": TEMPLATE_DIR / "task_planning_visualization.toml"
    },
    "task_creation": {
        "QAQC": TEMPLATE_DIR / "task_creation_qaqc.toml",
        "Transformation": TEMPLATE_DIR / "task_creation_transformation.toml",
        "Visualization": TEMPLATE_DIR / "task_creation_visualization.toml"
    }
}
