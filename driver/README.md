### Add lines(add a new mode for current cpu) ###
**WORKDIR: /home/user/work/awfy/driver**
* insert mode data into mysql.
```mysql
use dvander;
insert into awfy_mode value (32, 11, "headless-patch", "headless-compressed-pointer", "#FFFF00", 1);
insert into awfy_mode value (34, 1, "v8-turbofan-x64-patched", "v8-turbofan-x64-compressed-pointer", "#ABCDEF", 1);
```
* create config file.
```shell
cp client/machine_config/electro-x64.config client/machine_config/electro-x64-patch.config
```
edit config file 'client/machine_config/electro-x64-patch.config':
1) line 8(replace): 
```text
modes = headless-patch
```
2) line 24(replace): 
```text
modes = headless-patch
```
3) line 28(replace): 
```text
[headless-patch]
```

* edit schedule-run-chrome.sh
1) line 124(replace): 
```text
python dostuff-chrome.py  --config=client/machine_config/electro-x64.config --config2=client/machine_config/electro-x64-patch.config
```

* edit dostuff-chrome.py
1) line 65-66(insert):     
```text
if utils.config.has_section('headless-patch'):
     Engine = builders.Headless_patch()
```
                             
* edit build_server_chrome.py
1) line 41-42(insert):
```text
     if utils.config.has_section('headless-patch'):
          KnownEngines.append(builders.Headless_patch())
```     

* edit builders.py
1) line 378-480(copy): copy line 378-480 to line 481
2) line 481(replace): 
```text
# add Headless_patch Engine
```
3) line 482(replace): 
```text
class Headless_patch(Engine):
```
3) line 486(replace): 
```text
        self.source = utils.config.get('headless-patch', 'source')
```
3) line 516(replace):
```text
           out_argns = os.path.join(utils.RepoPath, self.source, 'out', self.cpu + '-patch', 'args.gn')
``` 
3) line 523(insert):
```text
                    # add patch to v8.
                    """
                    COMMAND:
                    patch -p 1 -i /repos/enable-compressed-pointer.patch
                    clean COMMAND:
                    patch -R -p 1 -i /repos/enable-compressed-pointer.patch
                    or 
                    git checkout .
                    """
                    with utils.FolderChanger(os.path.join(utils.RepoPath, self.source, 'v8')):
                        Run(['patch', '-p', '1', '-i', '/repos/enable-compressed-pointer.patch'], env)
``` 
3) line 540(replace):
```text
                    Run(['gn', 'gen', os.path.join(sourcePath, 'out', self.cpu + '-patch')], env)
``` 

3) line 516(replace):
3) line 516(replace):
3) line 516(replace):
3) line 516(replace):



3)
4)
