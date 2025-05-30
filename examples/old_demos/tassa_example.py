import uuid

from tassa import Tassa
from tassa.events import Set, Update
from tassa.schemas import Page, Header1, Paragraph, ImageCls, Text, InputBox, Slider, ImageUpload, Button, \
    Scene, Pcd, Ply, Glb, PointCloud, div

doc = Tassa("ws://localhost:8012")


# this is blocking because it autostarts.
@doc.bind(start=True)
def show_heatmap():
    from PIL import Image
    # image = Image.open("test.jpg")

    page = Page(
        Header1("Alan's Example"),
        Button(value="Hello!", style='''{"width":"100%", "height":"100px"}'''),
        InputBox(value="Hello World!"),
        Text("hello Jansen?", key="ge_demo"),
        Header1("Alan's Example"),
        Slider(min=20, max=50, step=2, value=40),
        div(Paragraph("Timur is sitting on the right"),
            style='{"border":"1px solid black", "width":"100px", "height":"100px"}'),
        ImageUpload(label="Upload an image: "),
        # ImageCls(data=image, key="alan_img"),
        # PointCloud(urls=["https://escher.ge.ngrok.io/files/william/nerfstudio/correspondences/2023-01-20_23-08-27/orange/mask_in.ply", "https://escher.ge.ngrok.io/files/william/nerfstudio/correspondences/2023-01-20_23-08-27/fork/mask_in.ply"]),
        # PointCloud(path="https://escher.ge.ngrok.io/files/will_scene.pcd")
        Scene(
            # Pcd(src="https://escher.ge.ngrok.io/files/will_scene.pcd", translation=[0, 0, 0], rotation=[0, 0, 0]),
            Ply(src="https://escher.ge.ngrok.io/files/william/nerfstudio/correspondences/2023-01-20_23-08-27/orange/mask_in.ply",
                position=[0.2, 0, 0], rotation=[0, 0, 0]),
            Ply(src="https://escher.ge.ngrok.io/files/william/nerfstudio/correspondences/2023-01-20_23-08-27/fork/mask_in.ply",
                position=[0, .2, 0], rotation=[0, 0, 0]),
            Ply(src="https://escher.ge.ngrok.io/files/william/nerfstudio/correspondences/2023-01-20_23-08-27/pink/mask_in_features_pca.ply",
                position=[0, 0, .2], rotation=[0, 0, 0]),
            Ply(src="https://escher.ge.ngrok.io/files/william/nerfstudio/correspondences/2023-01-20_23-08-27/spoon/mask_in.ply",
                position=[0, 0, 0], rotation=[0, 0, 0]),
        )
    )
    event = yield Set(page)
    while not event == "TERMINAL":
        if event == "UPLOAD":
            event = yield Update(ImageCls(data=event.value, key="alan_img"))
        else:
            # if event == "INPUT":
            #     event = yield Update(Text("hello there~~", key="ge_demo"))
            # elif event == "CLICK":
            print(vars(event))
            # event = yield Update(Text("hello there~~"))
            res = Paragraph(str(vars(event)), key=str(uuid.uuid4())[-10:])
            print(res.serialize())
            event = yield Update(res)
