import copy
import json
import logging
from xml.etree import ElementTree as ET
from typing import List, Literal


logger = logging.getLogger(__name__)

xml_template = """
<annotation>
    <folder></folder>
    <filename></filename>
    <size>
        <width></width>
        <height></height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
</annotation>
"""
doc = ET.fromstring(xml_template)


class Converter:
    def convert(self, input_data: List[dict], export_type: Literal["xml", "json"] = "xml") -> list:
        # if export_type == "xml":
        return self.convert_to_xml(input_data=input_data)
        # else:
        #     return self.convert_to_json(input_data=input_data)

    @staticmethod
    def convert_to_json(
        input_data: List[dict],
    ) -> str:
        # every file result
        results = []
        for sample in input_data:
            data = sample.get("data")
            if not data:
                continue
            # change skipped result is invalid
            annotated_result = data.get("result")
            if annotated_result and sample.get("state") == "SKIPPED":
                annotated_result["valid"] = False

            # change result struct
            if annotated_result:
                annotations = []
                for tool in annotated_result.copy().keys():
                    if tool.endswith("Tool"):
                        tool_results = annotated_result.pop(tool)
                        for tool_result in tool_results.get("result", []):
                            # 视频文件的标注结果已经保存了 label 键的值，不需要再做转换
                            if "label" not in tool_result:
                                tool_result["label"] = tool_result.pop("attribute", "")
                            tool_result["attribute"] = tool_result.pop("textAttribute", "")
                            tool_result.pop("sourceID", None)

                            if tool == "tagTool" or tool == "textTool":
                                tool_result.pop("label")

                            tool_result.pop("attribute")

                        annotations.append(tool_results)

                annotated_result["annotations"] = annotations
            else:
                continue
            annotated_result_str = json.dumps(annotated_result, ensure_ascii=False)
            results.append(
                {
                    "id": sample.get("id"),
                    "result": annotated_result_str,
                    "urls": data.get("urls"),
                    "fileNames": next(
                        (url.split("/")[-1] if url.split("/") else "" for url in data.get("urls", {}).values()),
                        "",
                    ),
                }
            )

        # Serializing json
        json_object = json.dumps(results, default=str, ensure_ascii=False)
        return json_object

    @staticmethod
    def convert_to_xml(
        input_data: List[dict],
    ) -> list:
        global xml_template
        xml_template = copy.deepcopy(xml_template)
        doc = ET.fromstring(xml_template)
        xml_parts = []
        for sample in input_data:
            data = sample.get("data")
            if not data:
                continue
            # change skipped result is invalid
            annotated_result = data.get("result")
            if annotated_result and sample.get("state") == "DONE":
                width = annotated_result["width"]
                height = annotated_result["height"]
                file_name = list(data["fileNames"].values())[0]
                folder = ""
                if "/" in file_name:
                    dir_name, file_name = file_name.split("/")
                if label := doc.find(".//size/width"):
                    label.text = str(width)
                if label := doc.find(".//size/height"):
                    label.text = str(height)
                if label := doc.find(".//folder"):
                    label.text = folder
                if label := doc.find(".//filename"):
                    label.text = file_name
                for tool in annotated_result.copy().keys():
                    if tool.endswith("Tool"):
                        tool_results = annotated_result.pop(tool)
                        for tool_result in tool_results.get("result", []):
                            object_element = ET.SubElement(doc, "object")
                            if "label" not in tool_result:
                                tool_result["label"] = tool_result.get("attribute", "")
                            ET.SubElement(object_element, "name").text = tool_result["label"]
                            ET.SubElement(object_element, "pose").text = "Unspecified"
                            ET.SubElement(object_element, "truncated").text = "0"
                            ET.SubElement(object_element, "occluded").text = "0"
                            ET.SubElement(object_element, "difficult").text = "0"

                            bndbox_element = ET.SubElement(object_element, "bndbox")
                            ET.SubElement(bndbox_element, "xmin").text = str(tool_result["x"])
                            ET.SubElement(bndbox_element, "ymin").text = str(tool_result["y"])
                            ET.SubElement(bndbox_element, "xmax").text = str(tool_result["x"] + tool_result["width"])
                            ET.SubElement(bndbox_element, "ymax").text = str(tool_result["y"] + tool_result["height"])
                xml_string = ET.tostring(doc, encoding="unicode")
                xml_parts.append(xml_string.strip())
        return xml_parts


converter = Converter()
