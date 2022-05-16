import csv
import gzip
import json
import os
from collections import defaultdict
from urllib.parse import urlparse
from urllib.request import urlopen, Request


tdir = "datasets"
URL = "https://data.gov.cz/soubor/distribuce.csv"

if __name__ == "__main__":
    os.makedirs(tdir, exist_ok=True)
    datasets = defaultdict(list)
    seen = set()

    req = Request(URL, headers={"Accept-Encoding": "gzip"})
    with urlopen(req) as r:
        assert r.headers["Content-Encoding"] == "gzip"
        body = gzip.open(r, "rt", encoding="utf-8")
        cr = csv.DictReader(body)
        for j, line in enumerate(cr):
            name = line["název"]
            url = line["přístupovéUrl"]
            if not name or not url:
                continue

            if (name, url) in seen:
                continue

            seen.add((name, url))

            netloc = urlparse(url).netloc
            datasets[netloc].append({"name": name, "url": url})

    for k, v in datasets.items():
        with open(os.path.join(tdir, k + ".json"), "wt", encoding="utf-8") as fw:
            json.dump(v, fw, ensure_ascii=False, indent=2)

    print("Updated")
