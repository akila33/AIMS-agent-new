from transformers import pipeline

def function(label_txt):
    output_text=''
    
    if len(data)>0:
        generator =  pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
        prompt = label_txt
        res = generator(prompt, max_length=100, do_sample=True, Temperature=0.9)
        output_text=res[0]['generated_text']
    return output_text