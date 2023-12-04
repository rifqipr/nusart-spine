from pydantic import BaseModel

class Art(BaseModel):
    id          : int
    image       : str
    title       : str
    artist      : str
    genre       : str
    era         : str
    description : str
    class Config:
        schema_extra = {
            "art demo" :{
                "id" : 1,
                "image_url" : "example_url",
                "title" : "demo",
                "artist" : "Pradipta",
                "genre" : "Post-Romantic",
                "era" : "Classical (1667)",
                "description" : "Lorem ipsum dolor sit amet"
            }
        }