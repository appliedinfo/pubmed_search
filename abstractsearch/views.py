from django.shortcuts import render
from forms import SearchForm
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import FormView, TemplateView,View
from django.http import HttpResponse
# import elasticsearch
from database import DatabaseElasticSearch
import simplejson as json
from havoc_search import search_keyword
# Create your views here.
import re


class SearchView(TemplateView):

    form = SearchForm
    template_name = "search.html"

    def get(self, request, form=None, *args, **kwargs):
        # if request.user.is_authenticated():
        #     return  HttpResponseRedirect('dashboard') #todo fix error here
        return render(request, self.template_name, {
                    'form': self.form() if form is None else form})

    def post(self, request, *args, **kwargs):
        """
        Authentication and Redirection
        """

        # from django.template import RequestContext
        data = request.POST.copy()
        form = self.form(data)
        context = {}
        # if form.is_valid():
        params = [q.strip() for q in data["query"].split(',') if q]
        es = DatabaseElasticSearch(host='45.79.223.102')
        # dsl_query = {
        # "match": {
        #     "abstract": "phosphate dehydrogenase"
        # }
        # }
                #find synonyms  
        key_variations = []
        for p  in params:
            key = search_keyword(p)
            key_variations.append(p)
            key_variations.extend(key["keyword_variation"])
        key_variations = list(set([k.lower() for k in key_variations]))
        queries = []

        for p in key_variations:
            queries.append({ "match": { "abstract": p }})



        query = {
        "dis_max": {
            "queries": queries,
            "tie_breaker": 0.3
        }
        }
        context = {}
        # results = es.fetch('pubmed','five_yr',dsl_query)
        results = es.fetch('pubmed', 'five_yr', query, 0, 50,fields=['pmid',"abstract"])
        # print results
        if results.get("status","success") == "success":
            hits = results['hits']['hits']
            total = results['hits']["total"]
            prv = None
            nxt = None


            summary = {
                # "status":200,
                # "message":"Ok",
                "results":total,
                # "start_date":start_date,
                # "end_date":end_date,
                # "offset":offset,
                # "limit":limit,
                # "previous":prv,
                # "next":nxt,
                # "params":params
            }
            # if aggs:
            #     return  { "meta": summary, self.type.lower():[x["_source"] for x in hits],
            #     "aggs":result.get("aggregations")}
            rr = []
            for x in hits:
                t = x["_source"]
                t["score"] = x["_score"]
                rr.append(t)
            fr = { "meta": summary, "results":rr}#[x["_source"] for x in hits]}
            # final_results = []
            # for rr in fr["results"]:
            #     # print 
            #     for key_var in key_variations:
            #         # print rr["abstract"]
            #         if key_var.lower() in rr["abstract"].lower():
            #             print "found"
            #             # rr["abstract"].lower().replace(key_var.lower(),)
            #             repl  = '<span style="background-color:yellow;">'+key_var+'</span>'
            #             abstract = re.sub(key_var.lower(), repl, rr["abstract"].lower())
            #             rr["abstract"] = abstract
            #         final_results.append(rr)   
            context = {
                        'form': self.form() if form is None else form,"results":fr["results"],
                        "words":' '.join(key_variations),"post":True,"keywords":','.join(key_variations)}
        # fr =  { "meta": {"message":"error",}, "results":[]}
        return self.render_to_response(context)
        # return HttpResponse(json.dumps(fr), content_type='application/json')





        return HttpResponse(context)