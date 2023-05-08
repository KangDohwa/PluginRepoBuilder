from requests import get
import json
import os
import sys
import git
from datetime import datetime


def download(dl_link=None, file_name=None, ver=None, repo=None):
    file_name = file_name.replace("?", "")
    mdir = os.getcwd()+"\\Plugins\\"+file_name+"\\"+ver
    fdir = os.path.join(mdir, file_name+".zip")
    if os.path.isdir(mdir) == False or os.path.isfile(fdir) == False:
        os.makedirs(mdir)
        print("{} {} is on process.".format(file_name, ver))

        with open(fdir, "wb") as file:
            if dl_link != "None":
                response = get(dl_link)
                file.write(response.content)
                print("{} {} Successfully Downloaded.".format(file_name, ver))
    else:
        print("{} {} is already exist. Moving on next...".format(file_name, ver))

    gdir = mdir+"\\src"
    if not repo == None:
        if not os.path.isdir(gdir):
            try:
                if repo.strip()[-1] == "/" or repo.strip()[-1] == "\\":
                    os.makedirs(gdir)
                    git.Git(gdir).clone(repo[:-1]+".git")
                else:
                    os.makedirs(gdir)
                    git.Git(gdir).clone(repo+".git")
                print("{} {} Successfully Cloned.".format(file_name, ver))
            except:
                print("{} {} Repo Not Valid.".format(file_name, ver))
    else:
        print("{} {} no Repository.".format(file_name, ver))


now = datetime.now()

js = open("repo.json", "rt", encoding="UTF8")
jsw = open("list archive/list_{}.json".format(
    now.date()), "a", encoding="UTF8")
jsr = open("repo archive/repo_{}.json".format(
    now.date()), "a", encoding="UTF8")

jsRepo = json.load(js)
ar = []

for i in jsRepo:
    t = {}
    for j in i:
        if j == "Name" or j == "AssemblyVersion" or j == "RepoUrl" or j == "DownloadLinkInstall" or j == "LastUpdate":
            if j == "LastUpdate":
                t[j] = i.get(j)
                t["LastUpdateInString"] = datetime.fromtimestamp(
                    i.get(j)).strftime("%Y-%m-%d %H:%M")
            # t.append("{} : {}".format(j, i.get(j)))
            else:
                t[j] = i.get(j)
            # ("{} : {}".format(j, i.get(j)))
    ar.append(t)
    download(t["DownloadLinkInstall"], t["Name"],
             t["AssemblyVersion"], t["RepoUrl"])
    # jsw.write(json.dumps(t, indent = 2))
ar.sort(key=lambda x: (x["Name"]).upper())
# ar.sort(key=str.lower)
jsw.write(json.dumps(ar, indent=2))
jsr.write(json.dumps(jsRepo))
js.close()
jsw.close()
