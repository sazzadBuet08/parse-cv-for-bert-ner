import json
import numpy as np
import sys
import spacy
nlp = spacy.load('en_core_web_sm')

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

def init_mat(cv_data, key_to_idx):
    content = cv_data['content']
    content_len = len(content)
    n_tag_array = np.empty(content_len)
    n_tag_array.fill(0)
    annotations = cv_data["annotation"]
    for annotation in annotations:
        if "label" in annotation.keys():
            labels = annotation["label"]
            if len(labels) == 0:
                continue
            elif len(labels) > 1:
                raise Exception("More than one label found.")
            label = labels[0]
            label_idx = key_to_idx[label]
            for point in annotation["points"]:
                start = point["start"]
                end = point["end"]
                for idx in range(start, end+1):
                    n_tag_array[idx] = label_idx

    return n_tag_array


def parse_ner_tokens(cv_data, idx_to_key, np_tag_array):

    tokens = list()
    content = cv_data["content"]
    content_len = len(content)
    i = 0
    while i<content_len:
        if content[i] == '\n':
            while i<content_len and content[i]=='\n':
                i += 1
            if i<content_len:
                tokens.append("")

        else:
            cur_line = ""
            line_start_idx = i
            while i < content_len and content[i] != '\n':
                cur_line += content[i]
                i += 1


            doc = nlp(cur_line)

            for token in doc:
                cur_token = token.text
                cur_token = cur_token.encode("ascii", "ignore")
                cur_token = str(cur_token, 'ascii')
                if len(cur_token)==0:
                    continue
                token_idx = token.idx+line_start_idx

                tag_idx = np_tag_array[token_idx]
                tag = ""
                if tag_idx == 0:
                    tag = "O"
                else:
                    name = idx_to_key[tag_idx]
                    tag = name.replace(" ", "_")

                #print(cur_token, tag, token.idx, token_idx, cur_token)
                tokens.append(cur_token + " " + tag)

    return tokens



key_to_idx, idx_to_key = create_label_map(json_data)
print(key_to_idx)
print(idx_to_key)

np_cv_map = init_mat(json_data[0], key_to_idx)
print(np_cv_map[60:70])

tokens = parse_ner_tokens(json_data[0], idx_to_key, np_cv_map)
print(tokens)


all_tokens = list()
cv_cnt = 0

for cv_data in json_data:
    np_cv_map = init_mat(cv_data, key_to_idx)
    tokens = parse_ner_tokens(cv_data, idx_to_key, np_cv_map)
    all_tokens.append(tokens)
    cv_cnt += 1
    sys.stdout.write("\r%d%% completed" % cv_cnt)
    sys.stdout.flush()

with open("../output/train.txt", "w") as wf:
    for i in range(0, 200):
        if i>0:
            wf.write("\n")
        for token in all_tokens[i]:
            wf.write(token+'\n')

with open("../output/dev.txt", "w") as wf:
    for i in range(200, 210):
        if i>0:
            wf.write("\n")
        for token in all_tokens[i]:
            wf.write(token+'\n')

with open("../output/test.txt", "w") as wf:
    for i in range(210, 220):
        if i>0:
            wf.write("\n")
        for token in all_tokens[i]:
            wf.write(token+'\n')

print(all_tokens[0])