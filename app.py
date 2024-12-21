from configs import pan_collection, ipo_pan_collection
from flask import Flask, jsonify, request, render_template
from pymongo.errors import PyMongoError
import requests as r
from json import loads
import xmltodict as xtd

app = Flask(__name__)


class CompanyInfo:
    def __init__(self, company_id, company_name):
        self.company_id = company_id
        self.company_name = company_name

    def create_select_tags(self):
        return f"<option value={self.company_id}>{self.company_name}</option>"


@app.route("/", methods=["GET"])
def get_home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def get_ipo_company_list():
    url = "https://linkintime.co.in/Initial_Offer/IPO.aspx/GetDetails"
    payload = {}
    headers = {"content-type": "application/json; charset:utf-8"}
    response = r.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        return {"err_msg": "Failed to fetch ipo details"}, response.status_code
    try:
        company_list = xtd.parse(loads(response.text)["d"])[
            "NewDataSet"]["Table"]
        company_list = [CompanyInfo(
            company["company_id"], company["companyname"]).create_select_tags() for company in company_list]
        company_select_body = "\r\n".join(
            [company for company in company_list])
        return company_select_body, 200
    except KeyError as e:
        return {"err_msg": f"Missing key: {str(e)}"}, 500
    except Exception as e:
        return {"err_msg": f"An unexpected error occurred: {str(e)}"}, 500


@app.route("/ipo/query", methods=["POST"])
def query_ipo():
    body = request.get_json()

    if "pan" not in body:
        err = jsonify({"error_msg": "PAN is missing from the request"})
        return err, 400

    if "ipo_id" not in body:
        err = jsonify({"error_msg": "IPO Id is missing from the request"})
        return err, 400

    client_id = body["ipo_id"]
    pan = body["pan"]

    ipo_pan_resp = ipo_pan_collection.find_one({"PAN": pan, "id": client_id})
    if ipo_pan_resp and ipo_pan_resp.get("status", None) is None:
        inserted_id = str(ipo_pan_resp["_id"])
        ipo_pan_resp["_id"] = inserted_id
        return ipo_pan_resp, 200

    url = "https://linkintime.co.in/Initial_Offer/IPO.aspx/SearchOnPan"
    payload = {"clientid": client_id, "PAN": pan,
               "IFSC": "", "CHKVAL": "1", "token": ""}
    headers = {"content-type": "application/json; charset:utf-8"}
    response = r.request("POST", url, headers=headers, json=payload)

    if response.status_code != 200:
        return {"err_msg": "Failed to fetch ipo details for the given pan"},
        response.status_code
    try:
        ipo_resp = xtd.parse(loads(response.text)["d"])["NewDataSet"]["Table"]
        ipo_resp["PAN"] = pan
        ipo_pan_collection.find_one_and_delete(
            {"PAN": pan, "id": client_id, "status": "Invalid"})
        insert_result = ipo_pan_collection.insert_one(ipo_resp)
        inserted_id = str(insert_result.inserted_id)
        ipo_resp["_id"] = inserted_id

        return ipo_resp, 200

    except KeyError as e:
        default_resp = {"PAN": pan, "id": client_id, "status": "Invalid"}
        result = ipo_pan_collection.insert_one(default_resp)
        default_resp["_id"] = str(default_resp["_id"])
        return default_resp, 200

    except PyMongoError as e:
        print(f"Database error occurred: {e}")
        return {"err_msg": "Database operation failed"}, 500

    except Exception as e:
        default_resp = {"PAN": pan, "id": client_id, "status": "Invalid"}
        result = ipo_pan_collection.insert_one(default_resp)
        default_resp["_id"] = str(default_resp["_id"])
        return default_resp, 200


@app.route("/user", methods=["POST"])
def create_user():
    body = request.get_json()

    if "name" not in body:
        err = jsonify({"error_msg": "name missing from the request"})
        return err, 400

    if "pan" not in body:
        err = jsonify({"error_msg": "pan missing from the request"})
        return err, 400

    user_with_pan = list(pan_collection.find({"pan": body["pan"]}))

    if len(user_with_pan) != 0:
        err = jsonify(
            {"error_msg": "user with the given pan is already present"})
        return err, 400

    user_pan = pan_collection.insert_one({"name": body["name"],
                                          "pan": body["pan"]})
    return {"msg": "User Created", "id": str(user_pan.inserted_id)}, 200


@app.route("/pan/list", methods=["GET"])
def get_pan_list():
    pan_list = list(pan_collection.find())
    return jsonify(pan_list)
