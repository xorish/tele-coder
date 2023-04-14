def add_group(self):
    group_name = self.group_name.text()
    import sys
    import os
    import json
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file = open(f"{path}/group_data.json", "r")
    data = json.load(file)
    file.close()
    if group_name:
        flag = 0
        for i in data.copy().keys():
            if i == group_name:
                flag = 1
                self.status.setText("Group name already exist, try something else!")
        if flag == 0:
            data[group_name] = self.group_text.toPlainText()
            file = open(f"{path}/group_data.json", "w")
            json.dump(data, file, indent=6)
            file.close()
            self.status.setText("Group added.")
            group_add(self)
    else:
        data[self.group_combo.currentText()] = self.group_text.toPlainText()
        file = open(f"{path}/group_data.json", "w")
        json.dump(data, file, indent=6)
        file.close()
        self.status.setText("Group updated.")


def group_combo_clear(self):
    self.group_combo.clear()


def codebook_combo_clear(self):
    self.codebook_combo.clear()


def codebook_path_combo_clear(self):
    self.codebook_dir_combo.clear()


def group_add(self):
    import sys
    import os
    import json
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file = open(f"{path}/group_data.json", "r")
    data = json.load(file)
    file.close()
    group_combo_clear(self)
    for i in data.keys():
        self.group_combo.addItem(i)


def group_show(self):
    import sys
    import os
    import json
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file = open(f"{path}/group_data.json", "r")
    data = json.load(file)
    file.close()
    try:
        current = self.group_combo.currentText()
        group_info = data[current]
        self.group_text.setText(group_info)
    except:
        pass


def group_search(self):
    search = self.search_group.text()
    if search:
        import sys
        import os
        import json
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/group_data.json", "r")
        data = json.load(file)
        file.close()
        group_combo_clear(self)
        for i in data.keys():
            if search in i:
                self.group_combo.addItem(i)
    else:
        group_add(self)


def codedir_combo_add(self):
    import sys
    import os
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file = open(f"{path}/code_book_paths", "r")
    data = eval(file.read())
    file.close()
    codebook_path_combo_clear(self)
    for i in data:
        self.codebook_dir_combo.addItem(i)


def code_path_add(self):
    import sys
    import os
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    pathx = self.code_book_path.text()
    file = open(f"{path}/code_book_paths", "r")
    data = eval(file.read())
    file.close()
    try:
        flag = 0
        for i in data:
            if pathx == i:
                self.status.setText("Codebook dir already exists!")
                flag = 1
        if flag == 0:
            data.append(pathx)
            self.status.setText("Codebook dir added!")
            file = open(f"{path}/code_book_paths", "w")
            file.write(str(data))
            file.close()
            codedir_combo_add(self)
    except:
        pass


def codebooks_add(self):
    import os
    pathx = self.codebook_dir_combo.currentText()
    if pathx != "Select Codebook Directory":
        cmd = f"ls {pathx}"
        try:
            res = os.popen(cmd).readlines()
            codebook_combo_clear(self)
            if len(res) > 0:
                for i in res:
                    if ".py" or ".sh" in i:
                        self.codebook_combo.addItem(i.replace("\n", ""))
            else:
                self.status.setText("No codebooks found in the current directory!")
        except:
            self.status.setText("Error in loading codebooks.")


def edit_code(self):
    from subprocess import Popen, PIPE
    pathx = self.codebook_dir_combo.currentText()
    filex = self.codebook_combo.currentText()
    cmd = f"code {pathx}/{filex}"
    pro = Popen("exec " + cmd, stdout=PIPE, stderr=PIPE, shell=True)
    err_message = pro.stderr.read().decode()
    self.status.setText(err_message)


def delete_group(self):
    import sys
    import os

    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    group_name = self.group_combo.currentText()
    if group_name!="Select Group":
        file = open(f"{path}/temp_buff", "w")
        file.write(group_name)
        file.close()

        self.process_group_delete.start('python3', ['-u', f'{path}/delete_group_consent.py'])
    else:
        self.status.setText("Invalid group!")

def delete_code_dir(self):
    import sys
    import os

    path = os.path.dirname(os.path.abspath(sys.argv[0]))

    dir_name = self.codebook_dir_combo.currentText()
    if dir_name!="Select Codebook Directory":
        file = open(f"{path}/temp_buff_dir", "w")
        file.write(dir_name)
        file.close()
        self.process_dir_delete.start('python3', ['-u', f'{path}/delete_dir_consent.py'])
    else:
        self.status.setText("Invalid directory!")

def execute(self):
    self.status.setText("Running codebook...")
    import sys
    import os
    import json

    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file = open(f"{path}/group_data.json", "r")
    data = json.load(file)
    file.close()
    group = self.group_combo.currentText()
    file_name = self.codebook_combo.currentText()


    cursor = self.disp.textCursor()
    cursor.movePosition(cursor.End)
    filepath = self.codebook_dir_combo.currentText() + "/" + self.codebook_combo.currentText()
    server_info_map = {}
    connection_flag=1
    try:
        file_extention = file_name.split(".")[1]
        group_info = data[group].split("\n")
        for i in group_info:
            if i:
                server_info = i.split(" ")
                server_info_map[server_info[0]] = [server_info[1], server_info[2]]
                self.disp.clear()
        for i in server_info_map:
            disp_color_change(self, "rgb(42, 177, 23)")
            cursor.insertText(f"\nChecking connection status with server {i}...")
            ssh_check=f"sshpass -p {server_info_map[i][1]} ssh -o StrictHostKeyChecking=no {server_info_map[i][0]}@{i} 'echo ola'"
            status=os.popen(ssh_check).read()
            if status=="ola\n":
                cursor.insertText(f"\nConnection established with the server {i}...\n")
            else:
                disp_color_change(self,"rgb(192, 57, 43)")
                cursor.insertText(f"\nConnection failed with the server {i}..\n")
                connection_flag=0
                break

        if connection_flag==1:
            cursor.insertText("\n\nConnection established to all servers.\n\n")
            if self.non_root.isChecked():
                ssh_cmd_list = []
                for i in server_info_map.keys():
                    scp_cmd = f"sshpass -p {server_info_map[i][1]} scp -o StrictHostKeyChecking=no {filepath} {server_info_map[i][0]}@{i}:~/"

                    os.system(scp_cmd)
                    if file_extention == "py":
                        cmdx = f"python3 ~/{file_name}"
                        ssh_cmd = f"sshpass -p {server_info_map[i][1]} ssh -o StrictHostKeyChecking=no {server_info_map[i][0]}@{i} '{cmdx}'"
                        ssh_cmd_list.append(ssh_cmd)

                    if file_extention == "sh":
                        cmdx = f"/bin/bash  {file_name}"
                        ssh_cmd = f"sshpass -p {server_info_map[i][1]} ssh -o StrictHostKeyChecking=no {server_info_map[i][0]}@{i} '{cmdx}'"
                        ssh_cmd_list.append(ssh_cmd)

                from multiprocessing import Pool

                cursor.insertText(f"\nExecution of '{file_name}' has started as NON-ROOT.\n\n")
                with Pool(len(ssh_cmd_list)) as p:

                    cursor.insertText('\n\n'.join(p.map(ssh_cmd_executor, ssh_cmd_list)))


            if self.root.isChecked():
                ssh_cmd_list=[]
                for i in server_info_map.keys():
                    scp_cmd = f"sshpass -p {server_info_map[i][1]} scp -o StrictHostKeyChecking=no {filepath} {server_info_map[i][0]}@{i}:~/"
                    os.system(scp_cmd)
                    if file_extention == "py":
                        cmdx = f"echo {server_info_map[i][1]} | sudo -S python3 ~/{file_name}"
                        ssh_cmd = f"sshpass -p {server_info_map[i][1]} ssh -o StrictHostKeyChecking=no {server_info_map[i][0]}@{i} '{cmdx}'"
                        ssh_cmd_list.append(ssh_cmd)
                    if file_extention == "sh":
                        cmdx = f"echo {server_info_map[i][1]} | sudo -S /bin/bash  {file_name}"
                        ssh_cmd = f"sshpass -p {server_info_map[i][1]} ssh -o StrictHostKeyChecking=no {server_info_map[i][0]}@{i} '{cmdx}'"
                        ssh_cmd_list.append(ssh_cmd)

                from multiprocessing import Pool
                cursor.insertText(f"\nExecution of '{file_name}' has started as ROOT.\n\n")
                with Pool(len(ssh_cmd_list)) as p:

                    cursor.insertText('\n\n'.join(p.map(ssh_cmd_executor, ssh_cmd_list)))

        else:
            cursor.insertText("\n\n Execution Failed!\n\n")

    except Exception as e:
        disp_color_change(self, "rgb(192, 57, 43)")
        self.disp.setText(str(e))
        cursor.insertText("\nSelect a valid file \n")
        cursor.insertText("\n\n Execution Failed!\n\n")

def ssh_cmd_executor(ssh_cmd):
    import os
    out=os.popen(ssh_cmd).read()
    return out
def disp_color_change(self,color):
    self.disp.setStyleSheet("font: 16pt \"Courier New\";\n"
                            f"color: {color};\n"
                            "background-color: rgb(14, 14, 2);\n"
                            "selection-background-color: rgb(206, 92, 0);\n"
                            "selection-color: rgb(0, 0, 0);\n"
                            "")

def add_hoc_command_runner(self):
    self.status.setText("Running command...")
    import sys
    import os
    import json

    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file = open(f"{path}/group_data.json", "r")
    data = json.load(file)
    file.close()
    command=self.command.text()
    group = self.group_combo.currentText()
    cursor = self.disp.textCursor()
    cursor.movePosition(cursor.End)
    server_info_map = {}
    connection_flag=1
    try:

        group_info = data[group].split("\n")
        for i in group_info:
            if i:
                server_info = i.split(" ")
                server_info_map[server_info[0]] = [server_info[1], server_info[2]]
                self.disp.clear()
        for i in server_info_map:
            disp_color_change(self, "rgb(42, 177, 23)")
            cursor.insertText(f"\nChecking connection status with server {i}...")
            ssh_check=f"sshpass -p {server_info_map[i][1]} ssh -o StrictHostKeyChecking=no {server_info_map[i][0]}@{i} 'echo ola'"
            status=os.popen(ssh_check).read()
            if status=="ola\n":
                cursor.insertText(f"\nConnection established with the server {i}...\n")
            else:
                disp_color_change(self,"rgb(192, 57, 43)")
                cursor.insertText(f"\nConnection failed with the server {i}..\n")
                connection_flag=0
                break

        if connection_flag==1:
            cursor.insertText("\n\nConnection established to all servers.\n\n")
            if self.non_root.isChecked():
                ssh_cmd_list = []
                for i in server_info_map.keys():
                        ssh_cmd = f"sshpass -p {server_info_map[i][1]} ssh -o StrictHostKeyChecking=no {server_info_map[i][0]}@{i} '{command}'"
                        ssh_cmd_list.append(ssh_cmd)


                from multiprocessing import Pool

                cursor.insertText(f"\nExecution of '{command}' has started as NON-ROOT.\n\n")
                with Pool(len(ssh_cmd_list)) as p:

                    cursor.insertText('\n\n'.join(p.map(ssh_cmd_executor, ssh_cmd_list)))


            if self.root.isChecked():
                ssh_cmd_list=[]
                for i in server_info_map.keys():
                    ssh_cmd = f"sshpass -p {server_info_map[i][1]} ssh -o StrictHostKeyChecking=no {server_info_map[i][0]}@{i} 'echo {server_info_map[i][1]} | sudo -S {command}'"
                    ssh_cmd_list.append(ssh_cmd)


                from multiprocessing import Pool
                cursor.insertText(f"\nExecution of '{command}' has started as ROOT.\n\n")
                with Pool(len(ssh_cmd_list)) as p:

                    cursor.insertText('\n\n'.join(p.map(ssh_cmd_executor, ssh_cmd_list)))
            command = self.command.text()
            file = open(f"{path}/command_history", "a")
            file.write(command+"\n")
            file.close()
        else:
            cursor.insertText("\n\n Execution Failed!\n\n")

    except Exception as e:
        disp_color_change(self, "rgb(192, 57, 43)")
        self.disp.setText(str(e))
        cursor.insertText("\nSelect a valid file \n")
        cursor.insertText("\n\n Execution Failed!\n\n")

def command_hist(self):
    import sys
    import os
    from PyQt5 import QtCore
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    self.process_history = QtCore.QProcess()
    self.process_history.start('python3', ['-u', f'{path}/history.py'])

def clear_command_hist(self):
    import sys
    import os
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    self.process_history_delete.start('python3', ['-u', f'{path}/delete_history_consent.py'])