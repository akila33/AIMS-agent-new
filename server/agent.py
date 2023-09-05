import sys  
import os
sys.path.insert(0, '')
import outputkggeneration as okgg
import searchandinvoke as sandi
import inputkggeneration as ikgg
#persistant the best_model in the disc but described as triple knowledge 
from rdflib import Graph, Literal, RDF, URIRef
# rdflib knows about quite a few popular namespaces, like W3C ontologies, schema.org etc.
from rdflib.namespace import FOAF , XSD
from rdflib.namespace import NamespaceManager
from rdflib import BNode
from uuid import uuid4
#from inspect import getmembers, isfunction
#print(getmembers(sandi, isfunction))
import pickle
import joblib
from joblib import dump,load
import pandas as pd
import numpy as np
import gzip

output_memery={}
servicelist=[]

def reset_temp_memery():
    output_memery={}
    servicelist=[]

def OperatingTask (task_name,input_file_path,desir_output_type,task_domain,namespace,purpose):
    print(servicelist)
    g = Graph()
    g.parse("KGLayer/contextkg.n3")
    openflag = 0
    purpose_flag = 1
    if len(task_name) > 0 and len(desir_output_type)> 0:
        if (namespace==''):
            namespace='http://aimicroservice.derby.ac.uk'
        st, ctx = knowledge_reasoning (input_file_path,desir_output_type,task_domain,namespace,purpose)
        if st == 1:
            return st, ctx
        if st == 2:
            tserlist = []
            w=getWorkflow_context(ctx.split('/')[-1],namespace)
            for i in range(len(w)):
                tserlist.append(w.get(i))
            print('doing transfer learning in context of ', tserlist)
            output = workflow_transfor(tserlist,input_file_path,servicelist,output_memery)
            return st, output
        task_id = str(uuid4())
        task= URIRef(namespace+'/'+task_id)
        
        #verb:
        _type = URIRef(namespace+'/task')
        has_input = URIRef(namespace+'/input')
        has_output = URIRef(namespace+'/desire_output')
        has_ioct = URIRef(namespace+'/iocategory')
        has_iodt = URIRef(namespace+'/iodatatype')
        has_ioshape = URIRef(namespace+'/ioshape')
        has_domain = URIRef(namespace+'/domain')
        #object:
        g.add((task, RDF.type, _type))
        if (len(task_domain)>0): 
            g.add((task, has_domain, Literal(task_domain,lang="en")))     
        if len(input_file_path) > 0: 
            _input = BNode()
            input_type = input_file_path.split('.')[1]
            g.add((task, has_input, _input))
            g.add((_input, has_iodt, URIRef(namespace+'/'+input_type)))        
            _output = BNode()
            if input_type == 'csv':
                openflag=1
        g.add((task, has_output, _output))
        for x in desir_output_type: 
            #print(len(x.split('.')))
            if len(x.split('.'))==1:
                #print(x)
                g.add((_output, has_iodt, URIRef(namespace+'/'+x)))
            if len(x.split('.'))>1:
                g.add((_output, has_ioct, URIRef(namespace+'/'+x.split('.')[0])))
                g.add((_output, has_iodt, URIRef(namespace+'/'+x.split('.')[1])))
            if len(x.split('.'))>2:
                g.add((_output, has_ioshape, Literal(x.split('.')[2],lang="en")))
        #print(task_id+' task_input KG is generated')
        g.serialize(destination='KGLayer/contextkg'+".n3")
        g.close()
        ctx=''
        if openflag ==1:
            df = pd.read_csv(input_file_path)
            ctx = ikgg.task_panda_inputKG(namespace, task_id, task_domain, purpose, df, input_file_path, desir_output_type)
        else:
            ctx = ikgg.task_normal_inputKG (namespace, task_id, task_domain, purpose, input_file_path, desir_output_type)
        output_value=composition_flow(input_file_path,desir_output_type,input_file_path, task_id)
        if output_value[1] not in servicelist:
            servicelist.append(output_value[1])
        if type(output_value[0]) is int:
            print ('no solution find')
        else:
            if purpose !='':
                purpose_flag = check_purpose(servicelist, purpose, namespace)
            if purpose_flag == 0:
                print('A solution is created but purpose is not meet, see knowledge files for more detail.')
            else:
                print('A solution is created to fully serves the task and match the purpose, see knowledge files for more detail.')
            okgg.task_output_workflowKG (servicelist,task_id,namespace)
            #print(output_value[0])
            if openflag == 1:
                okgg.savemodel(task_id,output_value[0],namespace,ctx,servicelist,purpose_flag)
                #print(output_value[2]['datafile.pandas'])
                okgg.outputlearning(output_value[2]['datafile.pandas'],task_id,output_value[0], namespace) 
            else:
                print('here is the output:', output_value[0])
                rw = input("Enter your reward: (0 - 1, e.g. 0.2, 0.3 or 0.9)")
                okgg.saveoutput(task_id,output_value[1],namespace,ctx,servicelist,rw)
                okgg.outputlearning_normal(task_id,output_value[0],namespace)
        
        return output_value
    else:
        return 'erro: nothing is generated'

def workflow_transfor(workflow,inputpath,servicelist,output_memery):
    k=sandi.transforming_mutation(workflow[0],[inputpath],servicelist,output_memery)
    for si in workflow[1:]:
        print('servicename:', si)
        k=sandi.transforming_mutation(si,[k[0]],servicelist,k[2])
        servicelist.append(k[1])
    return k
    
def composition_flow(input_path,desir_output,input_data, task_id):
    #servicelist = []
    output_value = sandi.searchandinvoke ('',[input_path.split('.')[1]], desir_output, [input_path], task_id, servicelist, output_memery)
    #print('out while step: ',output_value[0])
    if type(output_value[0]) is int:
        print('############No single microservice is available, Composition start##############')
        if output_value[0]==505:
            servicelist.append(output_value[1])    
        input_type_test = [input_path.split('.')[1]]
        input_value = [input_path]
        #type(i) is int
        controlgate=0
        while(type(output_value[0]) is int):
            print('------------In while-----------')
            output_value = sandi.searchandinvoke ('',input_type_test, '', input_value, task_id, servicelist,output_memery)
            #print('0:', output_value[0], '1:', output_value[1])
            if type(output_value[0]) is int:
                if (output_value[0]==505 and controlgate<5):
                    servicelist.append(output_value[1])
                    controlgate=controlgate+1
                else:
                    print('---end while and composition fails----')
                    break
            else:
                if output_value[1] not in servicelist:
                    servicelist.append(output_value[1])
                    flag = output_match_nextms(output_value[1])
                    if flag!=0:
                        input_type_test = []
                        input_value = [output_value[0]]
                        #print(input_value)
                        for xf in flag:
                            #print('I know here is a problem')
                            input_type_test.append(xf[1]) 
                            #print('check input_value: ',len(input_value[0]))
                        output_value = sandi.searchandinvoke ('',input_type_test, desir_output, input_value, task_id, servicelist, output_memery)
                        if (len(output_value)<3):
                            print('...')
                        else:
                            output_memery.update(output_value[2])
                else:
                    print('--------')
                
        print('-------end while-------')
    else:
        servicelist.append(output_value[1])
        output_memery.update(output_value[2])
        print('******** A single service find to complete the task')
    if type(output_value[0]) is int:
        print('############Composition end unsucessfully##############')
    else:
        #output_memery.update(output_value)
        print('############Composition sucessfully complete##############')
    return output_value

def output_match_nextms(ms_name):
    g = Graph()
    g.parse("registry.n3")
    namespace='http://aimicroservice.derby.ac.uk'
    MService = URIRef(namespace+'/'+ms_name)
    flag=[]
    q = """
        PREFIX ns1: <http://aimicroservice.derby.ac.uk/>
        
        SELECT *
        WHERE {""" 
    if len(ms_name)>0:
        q=q+'ns1:'+ms_name+""" ns1:output ?out . ?out ns1:paramter ?up . {?up ns1:pid ?uid . ?up ns1:iocategory ?c . ?up ns1:iodatatype ?d .} UNION {?up ns1:pid ?uid . ?up ns1:iodatatype ?d}}""" 
        #print (q)
        qr = g.query(q)
        flag_memery=[]
        if len(qr)==0:
            print('No output find haha')
        else:
            for r in qr:
                if r["c"] is None:
                    if r["d"] is None:
                        print ('no output find')
                    else:
                        #print(r["d"].split('/')[-1])
                        if r["d"].split('/')[-1] not in flag_memery:
                            flag.append([r["uid"],r["d"].split('/')[-1]])
                            flag_memery.append(r["d"].split('/')[-1])
                else:
                    #print(r["c"].split('/')[-1])
                    cate=r["c"].split('/')[-1]
                    if r["d"] is None:
                        #print ('no specific output')
                        if cate not in flag_memery:
                            flag.append([r["uid"],cate])
                            flag_memery.append(cate)
                    else:
                        #print(r["d"].split('/')[-1])
                        if r["d"].split('/')[-1] not in flag_memery:
                            flag.append([r["uid"],cate+'.'+r["d"].split('/')[-1]])
                            flag_memery.append(r["d"].split('/')[-1])
        #print(flag)
        return flag
    else:
        return 0
    
def check_purpose(service_list, purpose, namespace):
    g = Graph()
    g.parse("registry.n3")
    q = """
        PREFIX ns1: <"""+namespace+"""/>
        SELECT ?s
        WHERE {?s a ns1:"""+purpose+""" .}"""
    #print(q)
    qr = g.query(q)
    g.close()
    services = []
    if len(qr)==0:
        return 0
    else:
        for r in qr:
            services.append(r["s"].split('/')[-1])
    for si in services:
        if si in service_list:
            #print(si, services)
            return 1
    
def knowledge_reasoning (input_file_path,desir_output_type,task_domain,namespace,purpose):
    #Matching all paratmeters from context KG return 0 or 100
    #if not 100, Matching input [0, 50], Matching ouput [0, 20], matching task_domain [0,10], matching purpose [0,10],
    #matching input file type [0,10]
        #if >80: provide the exist solution
        #if >60 and output not match: provide the workflow as solution without last service
        #if >40 to select first service in the workflow to start re-configuration
    #else: provide the exist solution
    print('Searching for solution ...')
    scores = 0
    c1 = context_inputsemantic_match(input_file_path,namespace)
    c2 = context_outputemantic_match(desir_output_type,namespace)
    c3 = context_domain_match(task_domain,namespace)
    c4 = context_purpose_match(purpose,namespace)
    mscore = {}
    if len(c1)> 0:
        for c1x in c1:
            scores = c1x[1]
            ctx = c1x[0]
            for c2x in c2:
                if c2x[0] == ctx:
                    scores = scores + c2x[1]
            for c3x in c3:
                if c3x[0] == ctx:
                    scores = scores + c3x[1]
            for c4x in c4:
                if c4x[0] == ctx:
                    scores = scores + c4x[1]
            mscore[ctx] = scores
    else:
        if len(c2)> 0 :
            for c2x in c2:
                scores = c2x[1]
                ctx = c2x[0]
                for c3x in c3:
                    if c3x[0] == ctx:
                        scores = scores + c3x[1]
                for c4x in c4:
                    if c4x[0] == ctx:
                        scores = scores + c4x[1]
                mscore[ctx] = scores
        else:
            if len (c3)>0:
                for c3x in c3:
                    scores = c3x[1]
                    ctx = c3x[0]
                    for c4x in c4:
                        if c4x[0] == ctx:
                            scores = scores + c4x[1]
                    mscore[ctx] = scores
            else:
                for c4x in c4:
                    scores = c4x[1]
                    ctx = c4x[0]
                    mscore[ctx] = scores
    if bool(mscore) == False:
        print('No kwnoeldge at all, start to learn knowledge and expore the solution')
        return 0, ''
    else:
        mscore = dict(sorted(mscore.items(), key=lambda item: item[1]))
        #print (mscore)
        _key = list(mscore)[-1]
        kscores = mscore[_key]
        if kscores >=90:
            print('from the policy knowledge, a solution context found', _key)
            return 1, _key
        if kscores >=60:
            print('Policy knowledge is found to apply transfor learning with the new data', _key)
            return 2, _key
        if kscores >= 35:
            print('Policy knowledge suggests a good microservice to start with')
            return 3, _key
        if kscores < 35:
            print('Little knoweldge, start to learn knowledge to expore the solution')
            return 4, _key
    
def context_inputsemantic_match(input_file_path,namespace):
    funflag=0
    if len(input_file_path.split(','))>1:
        funflag=1
    ft = input_file_path.split('.')[-1]
    fn = input_file_path.split('.')[0]
    ctxl = []
    scorex = []
    lags = 0 
    if ft == 'csv' and funflag == 0:
        inputdf = pd.read_csv(input_file_path)
        g = Graph()
        g.parse("KGLayer/contextkg.n3")
        q = """
            PREFIX ns1: <"""+namespace+"""/>
            SELECT ?ctx ?fx
            WHERE {?t ns1:context ?ctx . ?ctx ns1:input_data ?in . ?in ns1:data_type ns1:"""+ft+""" . ?in ns1:feature_type ?fx.}"""
        qr = g.query(q)
        g.close()
        if len(qr)==0:
            print('No input context has been find')
        else:
            countm = 0
            for r in qr:
                inpx = r["ctx"]
                #print(inpx)
                if len(ctxl)> 0:
                    if inpx != ctxl[-1]:
                        countm = 0
                        scorex.append([ctxl[-1],(lags/len(inputdf.columns))*30+10 ])
                        lags = 0
                        ctxl.append(inpx)
                else:
                    ctxl.append(inpx)    
                inp = r["fx"].split('/')[-1]
                for col in inputdf.columns:
                    if col == inp:
                        countm=countm+1
                if countm == len(inputdf.columns):
                    scorex.append([inpx,30+10])
                else:
                    lags = countm
        
        return scorex
    return scorex

def context_outputemantic_match(output,namespace):
    #ctxl=[]
    scorex = []
    g = Graph()
    g.parse("KGLayer/contextkg.n3")
    q = """
        PREFIX ns1: <"""+namespace+"""/>
        SELECT DISTINCT ?ctx
        WHERE {?t ns1:context ?ctx . ?ctx ns1:desire_output ?up . """
    for xc in output:
        outdata = xc.split('.')
        if len(outdata)>1:
            q=q+"""?up ns1:iocategory ns1:"""+outdata[0]+""" . """ 
            q=q+"""?up ns1:iodatatype ns1:"""+outdata[1]+""" . """
        else:
            q=q+"""{?up ns1:iocategory ns1:"""+xc+""" .} UNION {?up ns1:iodatatype ns1:"""+xc+""" .}"""
            
        q=q+"""}"""
        
    #print(q)
    qr = g.query(q)
    g.close()
    if len(qr)==0:
        print('No output context has been find')
    else:
        #countm = 0
        for r in qr:
            outpx = r["ctx"]
            #if len(ctxl)> 0:
                #if outpx != ctxl[-1]:
                    #ctxl.append(outpx)
            #else:
                #ctxl.append(outpx)
            scorex.append([outpx,30])
    return scorex

def context_domain_match(task_domain,namespace):
    scorex=[]
    g = Graph()
    g.parse("KGLayer/contextkg.n3")
    q = """
        PREFIX ns1: <"""+namespace+"""/>
        SELECT DISTINCT ?ctx
        WHERE {?t ns1:context ?ctx . ?ctx ns1:domain ns1:"""+task_domain+""" .}"""
    qr = g.query(q)
    g.close()
    if len(qr)==0:
        print('domain is not matched')
    else:
        for r in qr:
            dmx = r["ctx"]
            scorex.append([dmx,15])
    return scorex

def context_purpose_match(purpose,namespace):
    scorex=[]
    g = Graph()
    g.parse("KGLayer/contextkg.n3")
    q = """
        PREFIX ns1: <"""+namespace+"""/>
        SELECT DISTINCT ?ctx
        WHERE {?t ns1:context ?ctx . ?ctx ns1:purpose ns1:"""+purpose+""" .}"""
    qr = g.query(q)
    g.close()
    if len(qr)==0:
        print('purpose is not matched')
    else:
        for r in qr:
            dmx = r["ctx"]
            scorex.append([dmx,15])
    return scorex

def reset_knowledge():
    open('KGLayer/contextkg.n3', 'w').close()
    open('KGLayer/policy.n3', 'w').close()
    open('KGLayer/commonkg.n3', 'w').close()
    open('KGLayer/workflows.n3', 'w').close()
    mydir = 'KGLayer/models/'
    filelist = [ f for f in os.listdir(mydir) if f.endswith(".gz") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))

def commonKGlearning(datasetout,task_id,outputv,ns):
    namespace = ns
    select_pipem=outputv
    select_pipem.fit(datasetout.drop(datasetout.columns[-1], axis=1),datasetout[datasetout.columns[-1]].astype(int))
    k=select_pipem.named_steps['rfe'].support_,select_pipem.named_steps['rfe'].ranking_
    listn=''
    i=0
    flag=0
    for ik in k[1]:
        if ik == 1:
            if flag ==0:
                listn=str(i)
                flag = 1
            else:
                listn=listn+'.'+str(i)
        i=i+1
    kg = Graph()
    kg.parse("KGLayer/taskinput.n3")
    #subject
    task = URIRef(namespace+'/'+task_id)
    #verb
    has_select_f = URIRef(namespace+'/selectedfeatures')
    kg.add((task, has_select_f, Literal(listn,lang="en")))
    #print(kg)
    kg.serialize(destination='KGLayer/taskinput'+".n3")
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
            
def savemodel(task_id,model,ns):
    namespace=ns
    filename = 'KGLayer/models/'+task_id
    with gzip.GzipFile(filename + '.gz', 'wb', compresslevel=3) as fo:  
        joblib.dump(model, fo)
    kg = Graph()
    kg.parse("KGLayer/solution.n3")
    #subject
    task = URIRef(namespace+'/'+task_id)
    #verb
    has_model = URIRef(namespace+'/solution')
    kg.add((task, has_model, Literal(filename+'.gz',lang="en")))
    #print(kg)
    kg.serialize(destination='KGLayer/solution'+".n3")
    kg.close()
    #with gzip.GzipFile(filename + '.gz', 'rb') as fo:  
        #return joblib.load(fo)
def getWorkflow_context(context,namespace):
    wfd = {}
    g = Graph()
    g.parse("KGLayer/policy.n3")
    q = """
        PREFIX ns1: <"""+namespace+"""/>
        SELECT DISTINCT ?id ?e
        WHERE {ns1:"""+context+""" ns1:workflow ?w . ?w ns1:wf_ims ?ms . ?ms ns1:wf_id ?id . ?ms ns1:wf_iloc ?e}"""
    qr = g.query(q)
    g.close()
    if len(qr)==0:
        print('Something wrong, context is not in the knowledge space!')
    else:
        for r in qr:
            idx = str(r.asdict()['id'].toPython())
            exe = str(r.asdict()['e'].toPython())
            wfd[int(idx)] = exe
    return wfd