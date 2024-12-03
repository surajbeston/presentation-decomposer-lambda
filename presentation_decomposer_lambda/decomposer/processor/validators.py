from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union

class ValueUnit(BaseModel):
    value: float
    unit: str

class Color(BaseModel):
    red: int
    green: int
    blue: int
    alpha: int

class BulletInfo(BaseModel):
    visible: bool
    type: int
    char: Optional[str]
    image_url: Optional[str]
    bullet_size_percent: Optional[float]
    bullet_color: Optional[Color]
    color: Optional[Color]
    font_name: Optional[str]
    font_size: Optional[ValueUnit]
    bold: bool
    italic: bool
    underline: bool
    orientation: int
    kerning: bool
    distance: ValueUnit
    start_value: int
    current_value: int
    indent: ValueUnit
    prefix: str
    suffix: str
    level: Optional[int]
    style: str
    type_description: str

    @validator('font_size', 'distance', 'indent', pre=True)
    def convert_to_value_unit(cls, v):
        if isinstance(v, dict) and 'value' in v and 'unit' in v:
            return ValueUnit(**v)
        elif isinstance(v, (int, float)):
            return ValueUnit(value=v, unit="px")
        return v

class Run(BaseModel):
    text: str
    font_name: str
    font_size: float
    bold: bool
    italic: bool
    underline: bool
    color: Color
    highlight_color: Optional[Color]
    position_x: ValueUnit
    position_y: ValueUnit
    width: ValueUnit
    height: ValueUnit

class Padding(BaseModel):
    left: ValueUnit
    right: ValueUnit
    top: ValueUnit
    bottom: ValueUnit

class Margin(BaseModel):
    left: ValueUnit
    right: ValueUnit
    top: ValueUnit
    bottom: ValueUnit

class Paragraph(BaseModel):
    text: str
    alignment: str
    level: Optional[int]
    bullet_info: BulletInfo
    runs: List[Run]
    position_x: ValueUnit
    position_y: ValueUnit
    width: ValueUnit
    height: ValueUnit
    line_height: ValueUnit
    margin: Margin
    padding: Padding
    autofit: str
    background_color: Optional[Color]

class TextFrame(BaseModel):
    paragraphs: List[Paragraph]
    vertical_alignment: str

class Fill(BaseModel):
    type: Optional[str]
    color: Optional[Color]
    transparency: ValueUnit

class Line(BaseModel):
    color: Optional[Color]
    width: ValueUnit
    style: Optional[str]
    transparency: ValueUnit

class Shape(BaseModel):
    name: str
    type: str
    width: ValueUnit
    height: ValueUnit
    position_x: ValueUnit
    position_y: ValueUnit
    rotation: ValueUnit
    z_order: Optional[int]
    has_text: bool
    vertical_alignment: str
    text_auto_grow_height: Optional[bool] = None
    text_auto_grow_width: Optional[bool] = None
    text_word_wrap: Optional[bool] = None
    text_fit_to_size: Optional[bool] = None
    text_frame: Optional[TextFrame] = None
    fill: Fill
    line: Line
    padding: Padding

class SlideStructure(BaseModel):
    index: int
    shapes: Dict[str, str]
    structure: List[Shape]
    thumbnail: Optional[str]
    background: Optional[str]
    frame_size: Dict[str, int]

class ProcessingResult(BaseModel):
    status: str
    progress: Optional[float] = None
    total_slides: int
    processed_slides: Optional[int] = None
    current_slide: Optional[SlideStructure] = None
    slides: List[SlideStructure]
    time_elapsed: Optional[float] = None
    time_to_first_slide: Optional[float] = None
    total_processing_time: Optional[float] = None

class SlideData(BaseModel):
    result: ProcessingResult
