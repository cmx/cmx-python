from time import sleep

import numpy as np
from tqdm import tqdm

from tassa import Tassa
from tassa.events import Set, Update, Frame
from tassa.schemas import (
    Scene,
    Frustum,
    group,
    # Instances,
)


def colmap_to_three(m):
    """Converts a 3x4 colmap camera matrix to a 4x4 three.js camera matrix."""
    matrix = np.array(m).reshape(4, 4)
    return matrix.T.flatten().tolist()


doc = Tassa(
    ws="ws://localhost:8013",
    # uri="http://localhost:8000/demos/vqn-dash/three",
    uri="http://dash.ml/demos/vqn-dash/three",
    reconnect=True,
    debug=True,
)

dataset = f"/instant-feature/datasets/rooms_dpvo/davis_lab_v1"
from ml_logger import logger

transforms = logger.load_json(dataset + "/transforms.json")
poses = sorted(transforms["frames"], key=lambda x: x["file_path"])


@doc.bind(start=True)
def show_heatmap():
    scene = Scene(
        group(key="cameras"),
    )

    event = yield Set(scene)
    assert event == "INIT"

    sleep(2.0)

    cameras = []
    for i, pose in enumerate(tqdm(poses)):
        matrix = colmap_to_three(pose["transform_matrix"])
        camera = Frustum(
            matrix=matrix,
            showUp=i % 5 == 0,
            showFrustum=False,
            showFocalPlane=False,
            showImagePlane=True,
            scale=10,
            near=0.08,
            far=0.2,
            fov=75,
            key=f"camera_{i}",
        )
        cameras.append(camera)

    event = yield Frame(
        Update(
            # Text(f"hahahha   {i}", key="debug-prompt"),
            group(*list(cameras)[::1], key="cameras"),
        )
    )

    sleep(1000)
