from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

db = client.bizDB
businesses = db.biz

pipeline = [
    { "$match" : { "town" : "Banbridge "} },
    { "$project" : {"town" : 1, "profit" : 1, "num_employees" : 1, "_id" : 0} },
    { "$unwind" : "$profit"},
    { "$match" : {
        "num_employees" : { $gte : 50 },
        "profit.gross" : { $gte : 0 }}},
    { $group : {
        _id : null,
        count : { $sum : 1 },
        total : { $sum : "$profit.gross"}
        average : { $avg : "$profit.gross"}
        max : { $max : "$profit.gross"}
        min : { $min : "$profit.gross"}
    }}    
].pretty()

pipelinemovieexample = [
    { $group : {
        _id : "$movie"
        count : { $sum : 1}
    }}
]

for business in businesses.aggregate(pipeline):
    print( business["town"], str(business["profit"][2]["gross"]) )