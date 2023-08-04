from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"Message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """returns all picture"""
    if data:
        return data, 200

    return {"Message": "Internal server error"}, 500


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """get a picture"""
    if data:
        for item in data:
            if item["id"] == id:
                return item
                return data, 200

    return {"Message": "Picture Not Found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if data:
        # Get the JSON data sent in the POST request
        picture_data = request.json
        print(picture_data)
        uniqueData = True

        for item in data:
            if item["id"] == picture_data["id"]:
                return {"Message": f"picture with id {picture_data['id']} already present"}, 302
                
        if(uniqueData):
            # Create New JSON data from the POST
            new_picture = {
                "id": picture_data["id"],
                "pic_url": picture_data["pic_url"],
                "event_country": picture_data["event_country"],
                "event_state": picture_data["event_state"],
                "event_city": picture_data["event_city"],
                "event_date": picture_data["event_date"],
            }
            data.append(new_picture)
            print(new_picture)
            return new_picture, 201
            #return data, 200 
    else:
        return {"Message": "Internal server error"}, 500

    return {"Message": "Internal server error"}, 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    if data:
        update_data = request.json
        # Find the user with the matching ID
        for item in data:
            if item["id"] == id:
                # Update the user properties with the new data
                item["event_country"] = update_data["event_country"]
                item["event_state"] = update_data["event_state"]
                item["event_city"] = update_data["event_city"]
                item["event_date"] = update_data["event_date"]

                return {"Message": "Update Successfull"}, 201
    else:
        return {"Message": "Internal server error"}, 500


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """delete a picture"""
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return {"Message": "Picture Deleted"}, 204

    return {"Message": "Picture Not Found"}, 404
