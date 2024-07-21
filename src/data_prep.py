import sys
import re
import json
import argparse
from pathlib import Path

def extract_n_samples(headings, articles, n):
    out_list = []
    for idx, d in enumerate(zip(headings, articles), 1):
        if idx == n+1:
            break
        out_list.append([d[0], d[1]])
    return out_list

def convert_data_to_json(n_samples: list, out_file):
    list_4_json = [] # a list of dictionaries of the form text:string
    for s in n_samples:
        list_4_json.append({"text":s[0] + " " + s[1]})
    with open(Path('/opt',out_file+'.json'), 'w', encoding='utf-8') as f:
        json.dump(list_4_json, f)
    print(f"{out_file} has been saved successfully")

def read_data(data_path, split):
    
    data_file = Path(data_path, split+'.txt')
    assert data_file.exists(), f"{data_file} not found"
    heading_pattern = '( \n \n = [^=]*[^=] = \n \n )'
    with open(data_file, 'r') as tr_f:
        lines = tr_f.read()
    head_art_split = re.split(heading_pattern, lines)
    headings = [x[7:-7] for x in head_art_split[1::2]]
    articles = [x for x in head_art_split[2::2]]
    return headings, articles



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract the abridged version of wikitext103 dataset")
    parser.add_argument("--data-path", type=str, required=True, help="Path to the WikiText103 dataset")
    parser.add_argument("--split", type=str, required=True, help="train/val split specifier")
    parser.add_argument("--num-samples", type=int, required=True, help="Number of samples to be extracted")
    parser.add_argument("--out-file", type=str, required=True, help="Output (.json) file")
    args = parser.parse_args()
    if Path(args.data_path).exists():
        print(f"{args.data_path} exists")
    else:
        print(f"{args.data_path} not found, exiting !!!")
        sys.exit(0)
    print(f"Reading {args.split} data .......")
    headings, articles = read_data(args.data_path, split=args.split)
    print("Extracting samples......")
    data_list = extract_n_samples(headings=headings, articles=articles, n=args.num_samples)
    print("Saving the abridged dataset")
    convert_data_to_json(n_samples=data_list, out_file=args.out_file+f"_{args.num_samples}.json")
