import os
from model_annotator import LipidNameAnnotator
import pandas as pd
from cobra.io import read_sbml_model, write_sbml_model
from _utils import transform_boimmg_id_in_annotation_id


def get_info(path):
    """Function that gets all statisticall information from LipidNameAnnotator class relative to lipids class caugth and number of lipids annotated.
    This data is stored in a spreadsheet specific for each model analised.

    :param path: Path to the model to be analised
    :type path: _type_
    """
    model = read_sbml_model(path)
    annotator = LipidNameAnnotator()
    info = annotator.find_model_lipids(model)
    model_id = model.id
    if model_id == "":
        model_id = "iBD1106"
    lipids_class = pd.Series(info[0])
    lipids_class = pd.DataFrame(lipids_class)
    original_annotations = pd.Series(info[1])
    original_annotations = pd.DataFrame(original_annotations)
    class_annotated = pd.Series(info[2])
    class_annotated = pd.DataFrame(class_annotated)
    sugested_annotations = info[3]

    ########## Set annotations #############
    path = f"Annotation/models/models_annotated/{model_id}.xml"
    model_final = info[4]
    # Write the SBML model to the XML file
    write_sbml_model(model_final, path)

    ######### Set statistical information ##########
    path = f"Annotation/models/results/{model_id}.xlsx"

    with pd.ExcelWriter(path) as writer:
        lipids_class.to_excel(
            writer, sheet_name=str(model_id), index=True, startrow=0, startcol=0
        )

        class_annotated.to_excel(
            writer, sheet_name=str(model_id), index=True, startrow=0, startcol=4
        )

    ######## Annotations to be curated ########
    sugested_annotations = transform_boimmg_id_in_annotation_id(sugested_annotations)
    path_txt = f"Annotation/models/results/{model_id}.txt"
    output = open(path_txt, "w")
    for k, v in sugested_annotations.items():
        output.writelines(f"{k} {v}\n")


if __name__ == "__main__":
    folder_path = r"Annotation/models/models_case_study"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            get_info(file_path)
