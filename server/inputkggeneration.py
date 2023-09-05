from rdflib import Graph, Literal, RDF, URIRef
# rdflib knows about quite a few popular namespaces, like W3C ontologies, schema.org etc.
from rdflib.namespace import FOAF , XSD
from rdflib.namespace import NamespaceManager
from rdflib import BNode
import pandas as pd
import numpy as np
from uuid import uuid4

def task_panda_inputKG (namespace, task_id, task_domain, task_purpose, inputdf, inputdata_name,dot):
    #flag = check_existance()
    flag = 0
    if (flag==1):
        #link task id to the exist task id
        #linkToPolicyKG()
        print('link to policy, find same datainput')
        #linkToWorldKG()
        #changeState()
    else:
        kg = Graph()
        kg.parse("KGLayer/contextkg.n3")
        
        if len(task_id) > 0 and len(inputdf) > 0:
            #subject
            task = URIRef(namespace+'/'+task_id)
                       
            #verb
            has_ctx = URIRef(namespace+'/context')
            #context object
            ctx_id = str(uuid4())
            ctx= URIRef(namespace+'/'+ctx_id)
            
            _data = inputdata_name.split('.')
            data_name = URIRef(namespace+'/'+_data[0])
            data_type = URIRef(namespace+'/'+_data[-1])
            has_datatype = URIRef(namespace+'/data_type')
            has_input = URIRef(namespace+'/input_data')
            has_number_record = URIRef(namespace+'/record_nubmer')
            has_number_feature = URIRef(namespace+'/feature_number')
            has_feature_type = URIRef(namespace+'/feature_type')
            has_output = URIRef(namespace+'/desire_output')
            has_ioct = URIRef(namespace+'/iocategory')
            has_iodt = URIRef(namespace+'/iodatatype')
            has_ioshape = URIRef(namespace+'/ioshape')
            
            kg.add((task, has_ctx, ctx))
            #object
            if len(task_domain) > 0:
                domain = URIRef(namespace+'/'+task_domain)
                #verb
                has_domain = URIRef(namespace+'/domain')
                kg.add((ctx, has_domain, domain))
                       
            if len(task_domain) > 0:
                _purpose = URIRef(namespace+'/'+task_purpose)
                has_purpose = URIRef(namespace+'/purpose')
                kg.add((ctx, has_purpose, _purpose))
                
            if len(dot) > 0:
                _output = BNode()
                kg.add((ctx, has_output, _output))
                for x in dot: 
                    #print(len(x.split('.')))
                    if len(x.split('.'))==1:
                        #print(x)
                        kg.add((_output, has_iodt, URIRef(namespace+'/'+x)))
                    if len(x.split('.'))>1:
                        kg.add((_output, has_ioct, URIRef(namespace+'/'+x.split('.')[0])))
                        kg.add((_output, has_iodt, URIRef(namespace+'/'+x.split('.')[1])))
                    if len(x.split('.'))>2:
                        kg.add((_output, has_ioshape, Literal(x.split('.')[2],lang="en")))
                
            kg.add((ctx, has_input, data_name))
            kg.add((data_name, has_datatype, data_type))
            #parsing inputdata
            numberr = inputdf.shape[0]
            numberf = inputdf.shape[1]
            kg.add((data_name, has_number_record, Literal(str(numberr),lang="en")))
            kg.add((data_name, has_number_feature, Literal(str(numberf),lang="en")))
            for col in inputdf.columns:
                col = col.replace(" ", "_")
                kg.add((data_name, has_feature_type, URIRef(namespace+'/feature/'+col)))
        kg.serialize(destination='KGLayer/contextkg'+".n3")
        kg.close()
        return ctx
def task_normal_inputKG (namespace, task_id, task_domain, task_purpose, inputdata_name, dot):
    #flag = check_existance()
    flag = 0
    if (flag==1):
        #link task id to the exist task id
        #linkToPolicyKG()
        print('link to policy, find same datainput')
        #linkToWorldKG()
        #changeState()
    else:
        kg = Graph()
        kg.parse("KGLayer/contextkg.n3")
        
        if len(task_id) > 0:
            #subject
            task = URIRef(namespace+'/'+task_id)
                       
            #verb
            has_ctx = URIRef(namespace+'/context')
            #context object
            ctx_id = str(uuid4())
            ctx= URIRef(namespace+'/'+ctx_id)
            
            _data = inputdata_name.split('.')
            data_name = URIRef(namespace+'/'+_data[0])
            data_type = URIRef(namespace+'/'+_data[-1])
            has_datatype = URIRef(namespace+'/data_type')
            has_input = URIRef(namespace+'/input_data')
            has_output = URIRef(namespace+'/desire_output')
            has_ioct = URIRef(namespace+'/iocategory')
            has_iodt = URIRef(namespace+'/iodatatype')
            has_ioshape = URIRef(namespace+'/ioshape')
            
            kg.add((task, has_ctx, ctx))
            #object
            if len(task_domain) > 0:
                domain = URIRef(namespace+'/'+task_domain)
                #verb
                has_domain = URIRef(namespace+'/domain')
                kg.add((ctx, has_domain, domain))
                       
            if len(task_domain) > 0:
                _purpose = URIRef(namespace+'/'+task_purpose)
                has_purpose = URIRef(namespace+'/purpose')
                kg.add((ctx, has_purpose, _purpose))
                
            if len(dot) > 0:
                _output = BNode()
                kg.add((ctx, has_output, _output))
                for x in dot: 
                    #print(len(x.split('.')))
                    if len(x.split('.'))==1:
                        #print(x)
                        kg.add((_output, has_iodt, URIRef(namespace+'/'+x)))
                    if len(x.split('.'))>1:
                        kg.add((_output, has_ioct, URIRef(namespace+'/'+x.split('.')[0])))
                        kg.add((_output, has_iodt, URIRef(namespace+'/'+x.split('.')[1])))
                    if len(x.split('.'))>2:
                        kg.add((_output, has_ioshape, Literal(x.split('.')[2],lang="en")))
            #data_name = URIRef(namespace+'/'+dataname)  
            #data_type = URIRef(namespace+'/'+data_type) 
            kg.add((ctx, has_input, data_name))
            kg.add((data_name, has_datatype, data_type))
        kg.serialize(destination='KGLayer/contextkg'+".n3")
        kg.close()
        return ctx
            