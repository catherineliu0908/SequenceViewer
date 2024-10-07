from flask import Flask, request
import flask
from Bio import SeqIO
from Bio.SeqFeature import FeatureLocation, CompoundLocation
from io import StringIO

app = Flask(__name__)


def show(data):
    appear_type = set()
    response = {
        "cgview": {
            "version": "1.5.0",
            "sequence": {"length": 0},
            "features": [],
            "legend": {"items": []},
            "tracks": [
                {
                    "name": "Features",
                    "dataType": "feature",
                    "dataMethod": "source",
                    "dataKeys": "json-feature",
                }
            ],
        }
    }
    for gb_record in SeqIO.parse(StringIO(data), "genbank"):
        print("Name %s, %i features" % (gb_record.name, len(gb_record.features)))
        print(len(gb_record.seq))
        response["cgview"]["sequence"]["length"] = len(gb_record.seq)
        # print(gb_record)
        for gb_feature in gb_record.features:
            if gb_feature.type == "CDS":
                if type(gb_feature.location) == CompoundLocation:
                    for loc in gb_feature.location.parts:
                        response["cgview"]["features"].append(
                            {
                                "start": loc.start,
                                "stop": loc.end,
                                "name": gb_feature.qualifiers["locus_tag"][0]
                                + gb_feature.qualifiers["product"][0],
                                "source": "json-feature",
                                "legend": "CDS",
                                "strand": gb_feature.location.strand,
                            }
                        )
                else:
                    response["cgview"]["features"].append(
                        {
                            "start": gb_feature.location.start,
                            "stop": gb_feature.location.end,
                            "name": gb_feature.qualifiers["locus_tag"][0]
                            + gb_feature.qualifiers["product"][0],
                            "source": "json-feature",
                            "legend": "CDS",
                            "strand": gb_feature.location.strand,
                        }
                    )
                if "CDS" not in appear_type:
                    response["cgview"]["legend"]["items"].append(
                        {
                            "name": "CDS",
                            "swatchColor": "blue",
                            "decoration": "arrow",
                        }
                    )
                    appear_type.add("CDS")
            elif gb_feature.type == "promoter" or gb_feature.type == "regulatory":
                print(gb_feature)
                if type(gb_feature.location) == CompoundLocation:
                    for loc in gb_feature.location.parts:
                        response["cgview"]["features"].append(
                            {
                                "start": loc.start,
                                "stop": loc.end,
                                "name": gb_feature.qualifiers["note"][0],
                                "source": "json-feature",
                                "legend": "promoter",
                                "strand": gb_feature.location.strand,
                            }
                        )
                else:
                    response["cgview"]["features"].append(
                        {
                            "start": gb_feature.location.start,
                            "stop": gb_feature.location.end,
                            "name": gb_feature.qualifiers["note"][0],
                            "source": "json-feature",
                            "legend": "promoter",
                            "strand": gb_feature.location.strand,
                        }
                    )
                if "promoter" not in appear_type:
                    response["cgview"]["legend"]["items"].append(
                        {
                            "name": "promoter",
                            "swatchColor": "orange",
                            "decoration": "arrow",
                        }
                    )
                    appear_type.add("promoter")
            elif gb_feature.type == "tRNA":
                print(gb_feature)
                if type(gb_feature.location) == CompoundLocation:
                    for loc in gb_feature.location.parts:
                        response["cgview"]["features"].append(
                            {
                                "start": loc.start,
                                "stop": loc.end,
                                "name": gb_feature.qualifiers["locus_tag"][0]
                                + gb_feature.qualifiers["product"][0]
                                if "locus_tag" in gb_feature.qualifiers
                                else gb_feature.qualifiers["note"][0],
                                "source": "json-feature",
                                "legend": "tRNA",
                                "strand": gb_feature.location.strand,
                            }
                        )
                else:
                    response["cgview"]["features"].append(
                        {
                            "start": gb_feature.location.start,
                            "stop": gb_feature.location.end,
                            "name": gb_feature.qualifiers["locus_tag"][0]
                            + gb_feature.qualifiers["product"][0]
                            if "locus_tag" in gb_feature.qualifiers
                            else gb_feature.qualifiers["note"][0],
                            "source": "json-feature",
                            "legend": "tRNA",
                            "strand": gb_feature.location.strand,
                        }
                    )
                if "tRNA" not in appear_type:
                    response["cgview"]["legend"]["items"].append(
                        {
                            "name": "tRNA",
                            "swatchColor": "green",
                            "decoration": "arrow",
                        }
                    )
                    appear_type.add("tRNA")
    return response

# def search_data(data, name):
#     pass

@app.route("/show", methods=["POST"])
def show_data():
    if request.method == "POST":
        try:
            data = request.json["data"]  # Assuming JSON data is sent
        except Exception as e:
            print(e)
            return {"message": "fail"}
        response_data = show(data)
        response = flask.jsonify({"message": "Data received", "data": response_data})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        return {"message": "Only POST requests are allowed"}, 405


if __name__ == "__main__":
    app.run(debug=True)
