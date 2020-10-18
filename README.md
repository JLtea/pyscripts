# scripts

## Collection of Python Scripts for JSON processing and validation

Run with:
`python3 preprocess.py example.json example.txt`



Running across multiple files:

`for f in *.json; do
  python3 preprocess.py "$f" "${f%.json}_T.txt"
done`

`for f in *.json; do`
`  python3 jsonToExcel.py "$f" "${f%.json}_T.xlsx"`
`done`

Running across all json in child directories:
for d in */ ; do
    for f in "$d"/*.json; do
    python3 preprocess.py "$f" "${f%.json}_T.txt"
    done
done

for d in */ ; do
    for f in "$d"/*.json; do
    python3 jsonToExcel.py "$f" "${f%.json}_T.xlsx"
    done
done
