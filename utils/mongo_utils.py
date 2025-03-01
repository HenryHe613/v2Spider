import pymongo

class mongo:
    def __init__(self):
        self.client = pymongo.MongoClient(
            host='127.0.0.1',
            port=27017,
            username='root',
            password='root'
        )
        self.db = self.client['v2ex']
        self.collection = self.db['posts']

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, data):
        return self.collection.find_one(data)

    def update(self, data):
        query = {"id": data["id"]}
        data.pop("id")
        data = {"$set": data}
        result = self.collection.update_one(query, data, upsert=True)
        # print(f"match {result.matched_count} document, update {result.modified_count} document")
        return result

    def delete(self, data):
        self.collection.delete_one(data)
        
        
if __name__ == '__main__':
    db = mongo()
    print(db.find({"name": "test"}))