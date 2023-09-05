# rdflib knows about quite a few popular namespaces, like W3C ontologies, schema.org etc.
# learning knowledge libs
# import libraries
from pandas_profiling import ProfileReport
from rdflib import Graph, URIRef

outputmemery={}

def searchandinvoke(ms_type,ms_input_category, ms_output_category, input_source, task_id, memery, output_memery):
    g = Graph()
    g.parse("registry.n3")
    invoke=''
    q = """
        PREFIX ns1: <http://aimicroservice.derby.ac.uk/>
        
        SELECT *
        WHERE {""" 
    if len(ms_type)>0:
        q=q+"""?ms rdf:type ns1:"""+ms_type+""" .
    """
    #print('ms input: ',ms_input_category)
    if len(ms_input_category)>0:
        q=q+""" ?ms ns1:input ?in . ?in ns1:paramter ?ip .""" 
        for xc in ms_input_category:
            print(xc)
            if len(xc.split(','))>1:
                inputdata = xc.split(',')[-1].split('.')
            else:
                inputdata = xc.split('.')
            if len(inputdata)>1:
                q=q+"""?ip ns1:iocategory ns1:"""+inputdata[0]+""" . """ 
                q=q+"""?ip ns1:iodatatype ns1:"""+inputdata[1]+""" ."""
            else:
                if len(xc.split(','))>1:
                    q=q+"""{?ip ns1:iocategory ns1:"""+'two_'+xc.split(',')[0]+""" .} UNION {?ip ns1:iodatatype ns1:"""+'two_'+xc.split(',')[0]+""" .} """
                else:
                    q=q+"""{?ip ns1:iocategory ns1:"""+xc+""" .} UNION {?ip ns1:iodatatype ns1:"""+xc+""" .} """
            #q=q+"""?in ns1:iocategory ns1:"""+xc+""" .""" 
        #for xd in ms_input_datatype:    
            #q=q+"""?in ns1:iodatatype ns1:"""+xd+""" .    
    if len(ms_output_category)>0:
        q=q+""" ?ms ns1:output ?out . ?out ns1:paramter ?up .""" 
        for xc in ms_output_category:
            outdata = xc.split('.')
            if len(outdata)>1:
                q=q+"""?up ns1:iocategory ns1:"""+outdata[0]+""" . """ 
                q=q+"""?up ns1:iodatatype ns1:"""+outdata[1]+""" ."""
            else:
                q=q+"""{?up ns1:iocategory ns1:"""+xc+""" .} UNION {?up ns1:iodatatype ns1:"""+xc+""" .}"""
        #for xc in ms_output_category:
            #q=q+"""?out ns1:iocategory ns1:"""+xc+""" .""" 
        #for xd in ms_output_datatype:    
            #q=q+"""?out ns1:iodatatype ns1:"""+xd+""" .
    q=q+"}"
    #print (q)
    qr = g.query(q)
    match=[]
    outputsmanticmemery=[]
    modules = {}
    if len(qr)==0:
        print('No microservice has been find')
        return 404,'No microservice has been find'
    else:
        for r in qr:
            #print('this is service found', r["ms"].split('/')[-1], 'and previous output_memery:', output_memery)
            if r["ms"].split('/')[-1] not in memery:
                required_input_num = input_number_count(r["ms"].split('/')[-1])
                if isinstance(input_source[0], list):
                    #print('has_input_number: ', len(input_source[0]),'invoke_required_input_number',required_input_num)
                    if len(input_source[0])>=required_input_num:
                        #print('Check semantic matching on inputs')
                        #input_semantic_matching
                        input_semantic=input_semantic_matching(r["ms"].split('/')[-1])
                        #print('last service name and input',memery[-1], input_semantic)
                        output_semantic=output_semantic_matching(memery[-1])
                        match = find_match_parameter(input_semantic,output_semantic)
                        #print('important!', len(match),len(output_semantic))
                        if(len(match)==required_input_num):
                            invoke = r["ms"].split('/')[-1]
                            outputsmanticmemery.append(output_semantic)
                    else:
                        #print('tune input learning algorithm')
                        #print('-step 1: checking any combinations of all possible input from different service')
                        #print(type(input_source[0]))
                        input_semantic=input_semantic_matching(r["ms"].split('/')[-1])
                        output_semantic=output_semantic_matching(memery[-1])
                        match = find_match_parameter(input_semantic,output_semantic)
                        #print('else_inputsemantics:!!!', input_semantic)
                        if(len(match)==len(output_semantic)):
                            invoke = r["ms"].split('/')[-1]
                            outputsmanticmemery.append(output_semantic)
                        else:
                            print('There is no matched the service can take the last output as input')
                            print('Agent is working on combinations of all previous outputs to search a possible solution')
                            match_2 =[] 
                            #print('2nd else_inputsemantics:!!!', input_semantic, 'match_2', match_2, 'output_memery', output_memery)
                            for i_output_m in output_memery:
                                #print('in for:', i_output_m)
                                for ist in input_semantic:
                                    #print('ist',ist,input_semantic[ist])
                                    i=0
                                    for io in input_semantic[ist]: 
                                        if i == 0:
                                            key=io
                                            i=i+1
                                        else:
                                            key=key+'.'+io
                                    #print(i_output_m, key)
                                    if i_output_m == key:
                                        match_2.append([i_output_m,0,int(ist)])
                                        #print('-step 2: if it can match, connect output together:',output_memery[i_output_m],len(match)+len(match_2),len(output_semantic))
                                    else:
                                        #datafile.split.#X_train, X_test, y_train, y_test#
                                        if len(i_output_m.split('#'))>1:
                                            v=i_output_m.split('#')[-2]
                                            i=0
                                            for specific in v.split(','):
                                                i_output_m_s = i_output_m.split('#')[0]+'#'+specific.strip()+'#'
                                                #print('-step 2.1:', i_output_m_s, key)
                                                if i_output_m_s == key:
                                                    match_2.append([i_output_m, i, int(ist)])
                                                    #print('-step 2.2: we find one', len(match_2)+len(match), required_input_num, match, match_2)
                                                i=i+1
                                if (len(match_2)+len(match)) == required_input_num:
                                    print('wow! find combination output -> input')
                                    invoke = r["ms"].split('/')[-1]
                                    modules[invoke] = __import__(invoke)
                                    combined_input_value={}
                                    for im in match:
                                        combined_input_value[im[1]]= input_source[0][im[0]]
                                    for idx in match_2:
                                        combined_input_value[idx[2]]= output_memery[idx[0]][idx[1]]
                                    lenc = len(combined_input_value)    
                                    #od = collections.OrderedDict(sorted(combined_input_value.items()))
                                    #print('combined value and invoke:------------------',combined_input_value)
                                    if lenc == 1:
                                        output=modules[invoke].function(combined_input_value[0])
                                    if lenc == 2:
                                        output=modules[invoke].function(combined_input_value[0],combined_input_value[1])
                                    if lenc == 3:
                                         #print ("start imported", invoke, 'microservice.', combined_input_value[0],combined_input_value[1],combined_input_value[2])
                                                   output=modules[invoke].function(combined_input_value[0],combined_input_value[1],combined_input_value[2])
                                    #print('end combination and invoke:--------------')
                                    #outputmemeryupdate(outputsmanticmemery[-1],output)
                                    print ("Successfully imported", invoke, 'microservice.')
                                    return output,invoke,outputmemery    
                                else:
                                    print('...continue searching solution...')
                else:
                    #print('has_input_number: ', len(input_source),'invoke_required_input_number',required_input_num)
                    if len(input_source)==required_input_num:
                        output_semantic = output_semantic_matching(r["ms"].split('/')[-1])
                        outputsmanticmemery.append(output_semantic)
                        invoke = r["ms"].split('/')[-1]
        try:
            if invoke!='':
                modules[invoke] = __import__(invoke)
                print ("Successfully imported", invoke, 'microservice.')
                
                if len(input_source)>0:
                    if len(input_source)==1:
                        #print(input_source[0])
                        if(len(match)>0):
                            #print ("assign matched output parameter: ", match[0][1]," -->input")
                            p_index=match[0][1]
                            output=modules[invoke].function(input_source[0][p_index])
                        else:
                            p_index=0
                            output=modules[invoke].function(input_source[0])
                            outputmemeryupdate(outputsmanticmemery[-1],output)
                        for xc in ms_output_category:
                            outdata = xc.split('.')
                            if len(outdata)>1:
                                if (outdata[1]=='pandas'):
                                    print ('input: ', input_source[0], '->knowledge: ', output.columns.values.tolist())
                                #knowledgelink = generating_profileReport(output, task_id)
                                #print ('Details data knolwedge has been saved in ProfileReport')
                            else:
                                if (xc == 'pandas'):
                                    print ('input: ', input_source[0], '->knowledge: ', output.columns.values.tolist())
                                #knowledgelink = generating_profileReport(output, task_id)
                        #print ('Details data knolwedge has been saved in ProfileReport')
                        outputmemeryupdate(outputsmanticmemery[-1],output)    
                        return output,invoke,outputmemery
                    if len(input_source)==2:
                        if(len(match)==2):
                            output=modules[invoke].function(input_source[0][match[0][1]],input_source[0][match[1][1]])
                            outputmemeryupdate(outputsmanticmemery[-1],output)
                        return output,invoke,outputmemery
                    if len(input_source)==3:
                        if(len(match)==2):
                            #print(match[0][1],match[1][1],match[2][1])
                            output=modules[invoke].function(input_source[0][match[0][1]],input_source[0][match[1][1]],input_source[0][match[2][1]])
                            outputmemeryupdate(outputsmanticmemery[-1],output)
                        return output,invoke,outputmemery
                    #if len(input_source)==4:
                        #output = modules[invoke].function(input_source[0],input_source[1],input_source[2],input_source[3])
                        #outputmemeryupdate(outputsmanticmemery[-1],output)
                        #return output,invoke
                    #if len(input_source)==5:
                        #output = modules[invoke].function(input_source[0],input_source[1],input_source[2],input_source[3],input_source[4])
                        #outputmemeryupdate(outputsmanticmemery[-1],output)
                        #return output,invoke
                else:
                    output= modules[invoke].function()
                    outputmemeryupdate(outputsmanticmemery[-1],output)
                    return output,invoke,outputmemery
            else:
                return 404,'No microservice has been find',outputmemery
        except ImportError:
            print ("Error importing ", invoke, '.')
            return 505,invoke,outputmemery
        
def transforming_mutation(servicename,input_source,memery,output_memery):
    match=[]
    outputsmanticmemery=[]
    modules = {}
    if servicename=='':
        return 404,'empty input'
    else:
        required_input_num = input_number_count(servicename)
        if isinstance(input_source[0], list):
            if len(input_source[0])>=required_input_num:
                input_semantic=input_semantic_matching(servicename)
                output_semantic=output_semantic_matching(memery[-1])
                match = find_match_parameter(input_semantic,output_semantic)
                if(len(match)==required_input_num):
                    invoke = servicename
                    outputsmanticmemery.append(output_semantic)
            else:
                input_semantic=input_semantic_matching(servicename)
                output_semantic=output_semantic_matching(memery[-1])
                match = find_match_parameter(input_semantic,output_semantic)
                if(len(match)==len(output_semantic)):
                    invoke = servicename
                    outputsmanticmemery.append(output_semantic)
                else:
                    match_2 =[] 
                    for i_output_m in output_memery:
                        for ist in input_semantic:
                            i=0
                            for io in input_semantic[ist]: 
                                if i == 0:
                                    key=io
                                    i=i+1
                                else:
                                    key=key+'.'+io
                            if i_output_m == key:
                                match_2.append([i_output_m,0,int(ist)])
                            else:
                                if len(i_output_m.split('#'))>1:
                                    v=i_output_m.split('#')[-2]
                                    i=0
                                    for specific in v.split(','):
                                        i_output_m_s = i_output_m.split('#')[0]+'#'+specific.strip()+'#'            
                                        if i_output_m_s == key:
                                            match_2.append([i_output_m, i, int(ist)])                
                                        i=i+1
                        if (len(match_2)+len(match)) == required_input_num:
                            #print('wow! find combination output -> input','service name is: '+servicename)
                            invoke = servicename
                            modules[invoke] = __import__(invoke)
                            combined_input_value={}
                            for im in match:
                                combined_input_value[im[1]]= input_source[0][im[0]]
                            for idx in match_2:
                                combined_input_value[idx[2]]= output_memery[idx[0]][idx[1]]
                            lenc = len(combined_input_value)    
                                   
                            if lenc == 1:
                                output=modules[invoke].function(combined_input_value[0])
                            if lenc == 2:
                                output=modules[invoke].function(combined_input_value[0],combined_input_value[1])
                            if lenc == 3:
                                output=modules[invoke].function(combined_input_value[0],combined_input_value[1],combined_input_value[2])
                                    
                            print ("Successfully imported", invoke, 'microservice.')
                            return output,invoke,outputmemery    
                        else:
                            print('...continue searching solution...')
        else:
            if len(input_source)==required_input_num:
                print (len(input_source), required_input_num)
                output_semantic = output_semantic_matching(servicename)
                outputsmanticmemery.append(output_semantic)
                invoke = servicename
        try:
            if invoke!='':
                modules[invoke] = __import__(invoke)
                print ("Successfully imported", invoke, 'microservice.')
                if len(input_source)>0:
                    if len(input_source)==1:
                        if(len(match)>0):
                            p_index=match[0][1]
                            output=modules[invoke].function(input_source[0][p_index])
                        else:
                            p_index=0
                            output=modules[invoke].function(input_source[0])
                            outputmemeryupdate(outputsmanticmemery[-1],output)
                        return output,invoke,outputmemery
                    if len(input_source)==2:
                        if(len(match)==2):
                            output=modules[invoke].function(input_source[0][match[0][1]],input_source[0][match[1][1]])
                            outputmemeryupdate(outputsmanticmemery[-1],output)
                        return output,invoke,outputmemery
                    if len(input_source)==3:
                        if(len(match)==2):
                            output=modules[invoke].function(input_source[0][match[0][1]],input_source[0][match[1][1]],input_source[0][match[2][1]])
                            outputmemeryupdate(outputsmanticmemery[-1],output)
                        return output,invoke,outputmemery
                else:
                    output= modules[invoke].function()
                    outputmemeryupdate(outputsmanticmemery[-1],output)
                    return output,invoke,outputmemery
            else:
                return 404,'No microservice has been find',outputmemery
        except ImportError:
            print ("Error importing ", invoke, '.')
            return 505,invoke,outputmemery
        
def generating_profileReport(df_source, task_id):
    profile = ProfileReport(df_source, title=task_id+' data profilling')
    #profile.to_file("pandas.html")
    return profile

def input_number_count(ms_name):
    g = Graph()
    g.parse("registry.n3")
    namespace='http://aimicroservice.derby.ac.uk'
    MService = URIRef(namespace+'/'+ms_name)
    q = """
        PREFIX ns1: <http://aimicroservice.derby.ac.uk/>
        
        SELECT ?ip
        WHERE {""" 
    if len(ms_name)>0:
        q=q+'ns1:'+ms_name+""" ns1:input ?in . ?in ns1:paramter ?ip . ?ip ns1:pid ?uid . ?ip ns1:iocategory ?c .}""" 
        qr = g.query(q)
        counter=0
        if len(qr)==0:
            #print('No input find')
            counter=0
        else:
            counter = len(qr)
        #print('!!!!!-',counter)
        return counter
    else:
        return 0
def input_semantic_matching(ms_name):
    g = Graph()
    g.parse("registry.n3")
    namespace='http://aimicroservice.derby.ac.uk'
    MService = URIRef(namespace+'/'+ms_name)
    
    q = """
        PREFIX ns1: <http://aimicroservice.derby.ac.uk/>
        
        SELECT ?uid ?c ?d ?isp
        WHERE {""" 
    if len(ms_name)>0:
        q=q+'ns1:'+ms_name+""" ns1:input ?in . ?in ns1:paramter ?ip . ?ip ns1:pid ?uid . {?ip ns1:iocategory ?c . ?ip ns1:iodatatype ?d . ?ip ns1:ioshape ?isp} UNION {?ip ns1:iocategory ?c . ?ip ns1:iodatatype ?d .} UNION {?ip ns1:iocategory ?c .}}"""
        #{?ip ns1:iocategory ?c . ?ip ns1:iodatatype ?d . ?ip ns1:ioshape ?isp} UNION {?ip ns1:iocategory ?c . ?ip ns1:iodatatype ?d .} UNION {?ip ns1:iocategory ?c .}
        #print(q)
        qr = g.query(q)
        flagdict={}
        uid_memery=[]
        if len(qr)==0:
            return flag
        else:
            for r in qr:
                flag=[]
                if r["uid"] is not None:
                    flag_memery=[]
                    
                    if r["c"] is not None:
                        if r["c"].split('/')[-1] in flag_memery:
                            pass
                        else:
                            #print(r["c"].split('/')[-1],flag_memery)
                            flag_memery.append(r["c"].split('/')[-1])
                            flag.append(r["c"].split('/')[-1])
                    if r["d"] is not None:
                        if r["d"].split('/')[-1] in flag_memery:
                            pass
                        else:
                            #print(r["d"].split('/')[-1],flag_memery)
                            flag_memery.append(r["d"].split('/')[-1])
                            flag.append(r["d"].split('/')[-1])
                    if r["isp"] is not None:
                        if str(r.asdict()['isp'].toPython()) in flag_memery:
                            pass
                        else:
                            #print(str(r.asdict()['isp'].toPython()),flag_memery)
                            flag_memery.append(str(r.asdict()['isp'].toPython()))
                            flag.append(str(r.asdict()['isp'].toPython()))
                            #print('this is the value in flag:', flag,len(flag))
                    if str(r.asdict()['uid'].toPython()) in uid_memery:
                        pass
                    else:
                        flagdict[str(r.asdict()['uid'].toPython())]= flag
                        uid_memery.append(str(r.asdict()['uid'].toPython()))
                        #print('this is the value in flag_dict:', flagdict[str(r.asdict()['uid'].toPython())])
            return flagdict
    else:
        return flagdict
def output_semantic_matching(ms_name):
    g = Graph()
    g.parse("registry.n3")
    namespace='http://aimicroservice.derby.ac.uk'
    MService = URIRef(namespace+'/'+ms_name)
    flag=[]
    q = """
        PREFIX ns1: <http://aimicroservice.derby.ac.uk/>
        
        SELECT ?c ?d ?isp
        WHERE {""" 
    if len(ms_name)>0:
        q=q+'ns1:'+ms_name+""" ns1:output ?out . ?out ns1:paramter ?op . ?op ns1:pid ?uid . {?op ns1:iocategory ?c . ?op ns1:iodatatype ?d . ?op ns1:ioshape ?isp} UNION {?op ns1:iocategory ?c . ?op ns1:iodatatype ?d .} UNION {?op ns1:iocategory ?c .}}"""
        #print(q)
        qr = g.query(q)
        flag_memery=[]
        if len(qr)==0:
            return flag
        else:
            for r in qr:
                if r["c"] is not None:
                    if r["c"].split('/')[-1] in flag_memery:
                        pass
                    else:
                        #print(r["c"].split('/')[-1],flag_memery)
                        flag_memery.append(r["c"].split('/')[-1])
                        flag.append(r["c"].split('/')[-1])
                if r["d"] is not None:
                    if r["d"].split('/')[-1] in flag_memery:
                        pass
                    else:
                        #print(r["d"].split('/')[-1],flag_memery)
                        flag_memery.append(r["d"].split('/')[-1])
                        flag.append(r["d"].split('/')[-1])
                if r["isp"] is not None:
                    if str(r.asdict()['isp'].toPython()) in flag_memery:
                        pass
                    else:
                        #print(str(r.asdict()['isp'].toPython()),flag_memery)
                        flag_memery.append(str(r.asdict()['isp'].toPython()))
                        flag.append(str(r.asdict()['isp'].toPython()))
        #print('output::::', flag)
        return flag
    else:
        #print('output::::', flag)
        return flag
    
def find_match_parameter(input_flag,output_flag):
    #pair=[[0, 0]]
    pair=[]
    print('find_match_paramenter---')
    #print(input_flag)
    for f in input_flag:
        #print(input_flag[f])
        if len(input_flag[f])>0 and len(output_flag)>0:
            if len(input_flag[f]) == 1:
                #print(input_flag[f][0],output_flag[0])
                if input_flag[f][0] == output_flag[0]:
                    pair.append([0,0])
                    return pair
                if len(output_flag[f])>1:
                    if input_flag[f][0] == output_flag[1]:
                        pair.append([0,0])
                        return pair
            if len(input_flag[f]) == 2:
                #print(input_flag[f][1],output_flag[0])
                if len(output_flag)==1:
                    if input_flag[f][1] == output_flag[0] or input_flag[f][1] == output_flag[1]:
                        pair.append([0,0])
                        return pair
                if len(output_flag)>1:
                    if input_flag[f][0] == output_flag[0] and input_flag[f][1] == output_flag[1]:
                        pair.append([0,0])
                        return pair
            if len(input_flag[f]) == 3 and len(output_flag)==3:
                #i_sem = input_flag[f][2].split('#')[-2].split(',')
                o_sem = output_flag[2].split('#')[-2].split(',')
                index_j=0
                for ox in o_sem:
                    #print('output=3:',ox,'input=1:',f, '=', input_flag[f][2].split('#')[-2])
                    if ox.strip() == input_flag[f][2].split('#')[-2].strip():
                        #print('pair created')
                        pair.append([f,index_j])
                        index_j=index_j+1
                    #index_i = index_i + 1
    
    return pair

def outputmemeryupdate(ms_output_semantic,ms_output):
    #print('this is semantic!!!!', ms_output_semantic)
    i=0
    for io in ms_output_semantic:
        if i ==0:
            key=io
        else:
            key=key+'.'+io
        i=i+1
    outputmemery[key]=ms_output
    #key=''
    #i=0
    
    #joblib.dump(outputmemery, 'outputmemery.joblib')
    
    #for x in outputmemery:
        #print('this is the key!!!!', x)
    #try:
        #geeky_file = open('output_memery.txt', 'wt', encoding="utf-8")
        #key=''
        #geeky_file.write(outputmemery, encoding="utf-8")
        #geeky_file.close()
    #except:
        #print("Unable to write to file")
    #outputmemery = json.load(open("output_memery.txt"))
    #print(ms_output_semantic,ms_output)
    #key=''
    #for io in ms_output_semantic:
        #key=key+'.'+io
    #outputmemery[key]=ms_output
    #json.dump(outputmemery, open("output_memery.txt",'w'))
    