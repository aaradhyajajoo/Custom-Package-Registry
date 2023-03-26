#!/usr/bin/env tsc
import { readFileSync, appendFile } from 'fs';
const fetch = require('node-fetch');

async function change_to_git(url_path:string)
{
    const txt = readFileSync(url_path, 'utf-8');
    const regex =  txt.match(/(\/){1}([-.\w]+)+/ig);
    if(regex) 
    {
        for(let i = 0; i < regex.length; i = i + 3) 
        {
            if(regex[i] == '/github.com') 
            {
                const url = 'https:/' + regex[i] + regex[i + 1] + regex[i + 2] + '\n';
                appendFile('cloning_repos/git_urls.txt', url, function (err) {
                    if (err) throw err;
                });
            }
            else
            {
                const repo_name = regex[i+2].slice(1);
                const registry = 'https://registry.npmjs.org/' + repo_name + '';
                const res = await fetch(registry);
                const data = await res.json();
                const new_reg = data['bugs']['url'].match(/(\/){1}([-.\w]+)+/ig);
                const url = 'https:/' + new_reg[0] + new_reg[1] + new_reg[2] + '\n';
                appendFile('cloning_repos/git_urls.txt', url, function (err) {
                    if (err) throw err;
                });
            }
        }
    }
}

change_to_git(process.argv.slice(2)[0]);