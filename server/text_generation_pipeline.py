from transformers import pipeline

def function(input_text_file):
    output_text=''
    if len(input_text_file.split('.'))> 1:
        #open text file in read mode
        text_file = open(input_text_file, "r")
 
        #read whole file to a string
        data = text_file.read()
 
        #close file
        text_file.close()
    
    else:
        data = input_text_file
    if len(data)>0:
        generator =  pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
        prompt = data
        res = generator(prompt, max_length=100, do_sample=True, Temperature=0.9)
        output_text=res[0]['generated_text']
    return output_text
