import json
import bert_repo.tokenization as tokenization

import tensorflow as tf

json_data = None

with open('/Users/habibullaharaphat/PycharmProjects/keras_sample/data/ner_in_resume.json', 'r', encoding="utf-8") as f:
    text = ""
    cnt = 0
    for line in f:
        if cnt>0:
            text += ","
        text += ""+line
        cnt = cnt + 1

    text = "[" + text + "]"

    json_data = json.loads(text)

print(json_data[0].keys())

print(json_data[0]['annotation'])

annotations = json_data[0]['annotation']
text = json_data[0]['content']

# for i in range(1295, 1305):
#     print(text[i])
# for annotation in annotations:
#     print(annotation)

def create_label_map(json_cvs):
    key_to_idx = dict()
    idx_to_key = dict()
    cnt = 0
    for json_cv in json_cvs:
        annotations = json_cv["annotation"]
        for annotation in annotations:
            if "label" in annotation.keys():
                labels = annotation["label"]
                if len(labels)==0:
                    continue
                elif len(labels)>1:
                    raise Exception("More than one label found.")
                label = labels[0]
                if label not in key_to_idx:
                    cnt += 1
                    key_to_idx[label] = cnt
                    idx_to_key[cnt] = label

    return key_to_idx, idx_to_key

def init_mat(cv_data):
    content =
    content_len =

key_to_idx, idx_to_key = create_label_map(json_data)

print(key_to_idx)
print(idx_to_key)


