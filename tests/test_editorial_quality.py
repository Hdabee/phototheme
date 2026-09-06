from PIL import Image
from app.editor.photo_state import PhotoEditState
from app.editor.project_story import ProjectStoryState
from app.renderer.collage_renderer import render_collage

def test_editorial_timeline_renders_four_photos(tmp_path):
    states=[]
    for index,color in enumerate(["red","green","blue","yellow"]):
        source=tmp_path/f"photo_{index}.png"
        Image.new("RGB",(360,480),color).save(source)
        states.append(PhotoEditState(photo_id=f"photo_{index}",source_path=str(source),caption=f"Etape {index+1}"))
    output=tmp_path/"editorial.png"
    theme={"id":"portrait-timeline-editorial","background":"#F2EFE8","premium":False}
    layout={"id":"editorial-timeline-four","photo_count":4}
    story=ProjectStoryState(hero_photo_id="photo_3")
    render_collage(states,layout,theme,output,size=1080,story=story)
    assert output.exists()
    assert Image.open(output).size==(1080,1080)
