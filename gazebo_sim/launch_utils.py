from pathlib import Path
from ament_index_python.packages import PackageNotFoundError, get_package_share_directory

PACKAGE_NAME = 'gazebo_sim'
try:
    PACKAGE_PATH = get_package_share_directory(PACKAGE_NAME)
except PackageNotFoundError:
    raise RuntimeError(f"Package '{PACKAGE_NAME}' not found. Ensure it is built and sourced correctly.")

DEFAULT_URDF_MODEL = 'base_model.urdf'
DEFAULT_MODEL_PATH = str(Path(PACKAGE_PATH) / 'models' / DEFAULT_URDF_MODEL)

DEFAULT_SDF_WORLD = 'base_world.sdf'
DEFAULT_WORLD_PATH = str(Path(PACKAGE_PATH) / 'worlds' / DEFAULT_SDF_WORLD)
