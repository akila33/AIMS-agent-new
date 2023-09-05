from rdflib import Graph, Literal, RDF, URIRef
# rdflib knows about quite a few popular namespaces, like W3C ontologies, schema.org etc.
from rdflib.namespace import FOAF , XSD
from rdflib.namespace import NamespaceManager
from rdflib import BNode
import pandas as pd
import numpy as np
import gzip
import pickle
import joblib
from joblib import dump,load
from uuid import uuid4

def outputlearning(datasetout,task_id,outputv,ns):
    namespace = ns
    select_pipem=outputv
    select_pipem.fit(datasetout.drop(datasetout.columns[-1], axis=1),datasetout[datasetout.columns[-1]].astype(int))
    k=select_pipem.named_steps['rfe'].support_,select_pipem.named_steps['rfe'].ranking_
    listn=''
    i=0
    flag=0
    clm=datasetout.columns[:-1]
    for ik in k[1]:
        #print(i,ik, k[1])
        if ik == 1:
            if flag ==0:
                listn=clm[i]
                flag = 1
            else:
                listn=listn+'.'+clm[i]
        i=i+1
    kg = Graph()
    kg.parse("KGLayer/commonkg.n3")
    #subject
    task = URIRef(namespace+'/'+task_id)
    #verb
    has_select_f = URIRef(namespace+'/selectedfeatures')
    kg.add((task, has_select_f, Literal(listn,lang="en")))
    #print(kg)
    kg.serialize(destination='KGLayer/commonkg'+".n3")
    kg.close()

def outputlearning_normal(task_id,output,namespace):
    kg = Graph()
    kg.parse("KGLayer/commonkg.n3")
    #subject
    task = URIRef(namespace+'/'+task_id)
    #verb
    has_output = URIRef(namespace+'/outcomes')
    kg.add((task, has_output, Literal(output,lang="en")))
    #print(kg)
    kg.serialize(destination='KGLayer/commonkg'+".n3")
    kg.close()
    
def task_output_workflowKG (listOfms,task_id,ns):
    namespace=ns
    if len(listOfms)>0:
        kg = Graph()
        kg.parse("KGLayer/workflows.n3")
        
        if len(task_id):
            #subject
            task = URIRef(namespace+'/'+task_id)
            #verb
            has_workflow = URIRef(namespace+'/workflow')
            has_ms_id = URIRef(namespace+'/wf_id')
            has_ims = URIRef(namespace+'/wf_ims')
            has_ms_iloc = URIRef(namespace+'/wf_iloc')
            _ms = BNode()
            kg.add((task, has_workflow, _ms))
            i=0
            #object
            for ms in listOfms:
                _ims = BNode()
                kg.add((_ms, has_ims, _ims))
                kg.add((_ims, has_ms_id, Literal(str(i),lang="en")))
                kg.add((_ims, has_ms_iloc, Literal(ms,lang="en")))
                i=i+1
        kg.serialize(destination='KGLayer/workflows'+".n3")
        kg.close()
        
#pv is the if the purpose is validated from the solution model       
def savemodel(task_id,model,ns,context,listOfms,pv):
    #print(context)
    namespace=ns
    policy_id = str(uuid4())
    policy = URIRef(namespace+'/'+policy_id)
    #save generated solution
    filename = 'KGLayer/models/'+task_id
    with gzip.GzipFile(filename + '.gz', 'wb', compresslevel=3) as fo:  
        joblib.dump(model, fo)
    #solution id
    s_id = str(uuid4())
    s = URIRef(namespace+'/'+s_id)
    kg = Graph()
    kg.parse("KGLayer/policy.n3")
    #add a policy
    has_ctx = URIRef(namespace+'/context')
    kg.add((policy, has_ctx, context))
    #subject
    task = URIRef(namespace+'/'+task_id)
    #verb
    has_model = URIRef(namespace+'/solution')
    has_state = URIRef(namespace+'/policy_state')
    has_workflow = URIRef(namespace+'/workflow')
    has_ms_id = URIRef(namespace+'/wf_id')
    has_ims = URIRef(namespace+'/wf_ims')
    has_ms_iloc = URIRef(namespace+'/wf_iloc')
    has_s_iloc = URIRef(namespace+'/s_iloc')
    has_reward = URIRef(namespace+'/reward')
    _ms = BNode()
    kg.add((context, has_model, s))
    kg.add((s, has_s_iloc, Literal(filename+'.gz',lang="en")))
    if pv == 0:
        kg.add((s, has_reward, Literal('0.5',lang="en")))
        kg.add((context, has_state, Literal('0.5',lang="en")))
    else:
        kg.add((s, has_reward, Literal('1',lang="en")))
        kg.add((context, has_state, Literal('1',lang="en")))
    kg.add((context, has_workflow, _ms))
    i=0
    #object
    lenlist = len(listOfms)
    msrward = 0
    if pv == 0:
        msrward = 0.5/lenlist
    else:
        msrward = 1/lenlist
    for ms in listOfms:
        f_sr = msrward*((lenlist-i)/lenlist)
        _ims = BNode()
        kg.add((_ms, has_ims, _ims))
        kg.add((_ims, has_ms_id, Literal(str(i),lang="en")))
        kg.add((_ims, has_ms_iloc, Literal(ms,lang="en")))
        kg.add((_ims, has_reward, Literal(str(f_sr),lang="en")))
        i=i+1
    #kg.add((task, has_model, Literal(filename+'.gz',lang="en")))
    #print(kg)
    kg.serialize(destination='KGLayer/policy'+".n3")
    kg.close()
    
def saveoutput(task_id,service,ns,context,listOfms,pv):
    namespace=ns
    policy_id = str(uuid4())
    policy = URIRef(namespace+'/'+policy_id)
    #save generated solution
    filename = 'KGLayer/models/'+task_id
    #solution id
    s_id = str(uuid4())
    s = URIRef(namespace+'/'+s_id)
    kg = Graph()
    kg.parse("KGLayer/policy.n3")
    #add a policy
    has_ctx = URIRef(namespace+'/context')
    kg.add((policy, has_ctx, context))
    #subject
    task = URIRef(namespace+'/'+task_id)
    #verb
    has_model = URIRef(namespace+'/solution')
    has_state = URIRef(namespace+'/policy_state')
    has_workflow = URIRef(namespace+'/workflow')
    has_ms_id = URIRef(namespace+'/wf_id')
    has_ims = URIRef(namespace+'/wf_ims')
    has_ms_iloc = URIRef(namespace+'/wf_iloc')
    has_s_iloc = URIRef(namespace+'/s_iloc')
    has_reward = URIRef(namespace+'/reward')
    _ms = BNode()
    kg.add((context, has_model, s))
    kg.add((s, has_s_iloc, Literal(service+'.py',lang="en")))
    if pv == '':
        kg.add((s, has_reward, Literal('0.5',lang="en")))
        kg.add((context, has_state, Literal('0.5',lang="en")))
    else:
        kg.add((s, has_reward, Literal(pv,lang="en")))
        kg.add((context, has_state, Literal(pv,lang="en")))
    kg.add((context, has_workflow, _ms))
    i=0
    #object
    lenlist = len(listOfms)
    msrward = 0.0
    if pv == '':
        msrward = 0.5/lenlist
    else:
        msrward = float(pv)/lenlist
    for ms in listOfms:
        f_sr = msrward*((lenlist-i)/lenlist)
        _ims = BNode()
        kg.add((_ms, has_ims, _ims))
        kg.add((_ims, has_ms_id, Literal(str(i),lang="en")))
        kg.add((_ims, has_ms_iloc, Literal(ms,lang="en")))
        kg.add((_ims, has_reward, Literal(str(f_sr),lang="en")))
        i=i+1
    #kg.add((task, has_model, Literal(filename+'.gz',lang="en")))
    #print(kg)
    kg.serialize(destination='KGLayer/policy'+".n3")
    kg.close()