import elasticsearch
import logging
#delete requires to install delete_by_query


class DatabaseElasticSearch():

    def __init__(self, host="127.0.0.1", port=9200, timeout=50):
        # self.es = elasticsearch.Elasticsearch()
        self.es = elasticsearch.Elasticsearch([{'host': host, 'port': port}])


    def save(self, json_data, index, doc_type, doc_id):
        """ creates the index"""
        try:  
            print "saving the data in ", json_data, doc_type, self.es
            index  = index+"_"+doc_type
            # if self.es.indices.exists(index) == False:
            #     print "creating index...",mapping
            #     self.es.indices.create(index)
            #     self.es.indices.put_mapping(index=index, doc_type=doc_type, body=mapping)
            res = self.es.index(index=index, doc_type=doc_type, id=doc_id, body=json_data)
            return {"status":"success","result":res}
            # print status
        except Exception as e:
            print e.message,e
            logging.debug("error while saving data on es "+ str(e))
            return {"status": "error", "message":e.message+str(e)}
        

    def fetch(self, index, doc_type, dsl_query, offset, limit, aggs=None, fields = []):
        print "es _fetch.."
        body = {
                "_source":fields,
                "from" : offset, "size" : limit,
                 "query" : dsl_query,

                }
        # print aggs
        if aggs:
          body = {
                  "_source":fields,
                  "from" : offset, "size" : limit,
                   "query" : dsl_query,
                   "aggs":aggs
                  }


        index  = index+"_"+doc_type
        try: 
            print "Query to ES",body, index,doc_type
            es_result = self.es.search(index=index, doc_type=doc_type, body=body,explain=True)
            # print es_result,"********"
            return es_result
        except Exception as e:
            print e.message,e,"EEXX"
            return {"status": "error", "message":"Exception: "+str(e)}

    def delete_gh(self, index, doc_type, org_id, gethealthID):
      """deletes the record from index
      params:index, doc_type, org_id, gethealthID
      return: response status
      """
      index  = index+"_"+doc_type
      body = {
                "query": {
              "bool": {
            "must": [{"term": {"org_id": org_id}}, 
            {"term": {"gethealthID": gethealthID

              }}]}

              }
             }
      logging.debug(index+" : "+str(body))

      res = "" 
      try:
        if self.es.indices.exists(index) == True:
          res = self.es.delete_by_query(index,doc_type,body=body)
          return res
      except Exception as e:
        print e,"EX"
        return {"status":"error","message":str(e)}

        

if __name__ == '__main__':
    es = DatabaseElasticSearch()
    json_data = {
                "utc_offset": "",
               "e_id": "6_14_6_497385276",
               "last_updated": "",
               "weight": 79.874,
               "timestamp": "2016-02-26T16:41:57",
               "bmi": "",
               "height": "",
               "free_mass": "",
               "source_name": "",
               "validated": "",
               "mass_weight": "",
               "user_id": "14_6",
               "fat_percent": "",
               "org_id": 6,
               "source": "withings",
               "source_id": 497385276

    }
    sleep = {
              "utc_offset": "+0530",
              "last_updated": "",
              "timestamp": "2016-06-06T05:25:00",
              "e_id": "3_6e48e84b_e89b_401e_9f83_7fab6a676e12_113233598693",
              "fetched_time": "2016-05-02 05:24:54.864986",
              "deep": 407,
              "awake": 97,
              "gethealthID": "6e48e84b_e89b_401e_9f83_7fab6a676e12",
              "source_name": "",
              "validated": "",
              "times_woken": 42,
              "total_sleep": 576460000,
              "user_id": "56813ab6_bdb1_4653_b5f2_f7fbe4172f59",
              "light": 7,
              "org_id": 3,
              "source": "fitbit",
              "rem": 457,
              "source_id": "1132335986933"
            }
    weight = {
            "utc_offset": "",
            "bmi": "",
            "last_updated": "",
            "weight": 8.932,
            "timestamp": "2016-02-23T21:39:06",
            "e_id": "6e48e84b_e89b_401e_9f83_7fab6a676e12",
            "fetched_time": "2016-05-01 18:13:53.064154",
            "height": "",
            "gethealthID": "6e48e84b_e89b_401e_9f83_7fab6a676e15",
            "source_name": "",
            "validated": "",
            "mass_weight": "",
            "user_id": "",
            "org_id": 1,
            "fat_percent": "",
            "free_mass": "",
            "source": "withings",
            "source_id": "49552271833"
            }
    fitness = {
              "utc_offset": "",
              "last_updated": "",
              "source_uid": "",
              "timestamp": "",
              "start_time": "2016-07-18T13:42:25+05:30",
              "e_id": "99_8055b774_0dd0_4e6e_b2d9_4d75a8642403_e798769b-a620-456a-b085-6d44ebf045e17",
              "fetched_time": "2016-07-26 07:24:39.381975",
              "intensity": "",
              "gethealthID": "8055b774_0dd0_4e6e_b2d9_4d75a8642403",
              "duration": 1,
              "source_name": "",
              "validated": "",
              "distance": 1,
              "user_id": "",
              "org_id": 7,
              "calories": 10,
              "source": "fitbit",
              "steps": 12,
              "end_time": "2016-07-18T13:43:49+05:30",
              "source_id": "e798769b-a620-456a-b085-6d44ebf045e177",
              "activity_category": "",
              }

    mapping  = {
                  "properties": {
                    "timestamp": {
                      "type": "date"
                    }
                  }
                }
    dm = {'utc_offset': None,  'calories': 0, 'timestamp': '2016-04-05T05:42:01', 'start_time': '2016-04-05T05:42:01', 'e_id': '2_1_2_35211205', 'fetched_time': '2016-04-25 18:02:36.311921', 'intensity': '', 'duration': 2057, 'source_name': '', 'validated': '', 'distance': 7, 'user_id': u'1_2', 'org_id': 2L, 'source': u'dailymile', 'steps': '', 'end_time': '2016-04-05T06:16:18', 'source_id': 35211205, 'activity_category': '', 'type': u'Running'}
    # es.save(dm, "deviceapi", "fitness", 4)
    mf = {'utc_offset': '', 'last_updated': '', 'timestamp': '2016-03-30T21:59:05+05:30', 'e_id': '2_1_2_570b69d19230ddddd67ec5e2', 'fetched_time': '2016-04-25 18:22:56.050601', 'deep': 25560, 'awake': 1380, 'source_name': '', 'validated': True, 'times_woken': 3, 'total_sleep': 37440, 'user_id': u'1_2', 'light': 11520, 'org_id': 2L, 'source': u'misfit', 'rem': '', 'source_id': u'570b69d19230ddddd67ec5e2'}
    print es.save(fitness, "deviceapi", "fitness", "1234")
    # assert
    # print es.fetch("deviceapi",   "fitness", 'org_id:"app1"')
    # print es.delete_gh("deviceapi", "weight",1,"6e48e84b_e89b_401e_9f83_7fab6a676e15")