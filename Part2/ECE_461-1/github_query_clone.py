import git
import os
from os.path import exists
import shutil

def clone_repo():
    n = 0
    #readme_list = []
    with open(r"cloning_repos/git_urls.txt", "r") as url_file:
        urls = url_file.readlines()
    for url in urls:
        url = url.strip()
        n += 1
        new_dir_name = "cloning_repos/cloned_repo{}".format(n)
        if os.path.exists(new_dir_name):
            shutil.rmtree(new_dir_name, ignore_errors=False, onerror=None)
        os.mkdir(new_dir_name)
        repo = git.Repo.clone_from(url, new_dir_name)
        readme_exists = exists("{}/README.md".format(new_dir_name))
        if readme_exists:
            rampup_time = 1
        else:
            rampup_time = 0
        readme_list = url + " " + str(rampup_time) + "\n"
        
        with open("rampup_time.txt", "a") as rampup_file:
            rampup_file.write(readme_list)
            
clone_repo()