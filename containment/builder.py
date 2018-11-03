# -*- coding: utf-8 -*-
import json
import os
import pathlib
import subprocess
import sys

import docker

from .config import config


class Context:
    def __init__(self):
        # CONFIGURATION STRINGS
        self.project_adapter = rf"""RUN     useradd -G docker --uid {config.uid} --home /home/{config.user} {config.user}
        RUN     echo {config.user} ALL=(ALL) NOPASSWD: ALL >> /etc/sudoers
        COPY    ./entrypoint.sh entrypoint.sh
        RUN     chmod +x entrypoint.sh"""
        self.entrypoint_text = f"""#!{config.shell}
        cd {config.project_config.directory}
        sudo sed -ie 's/docker:x:[0-9]*:{config.user}/docker:x:{config.docker_gid}:{config.user}/g' /etc/group
        sudo usermod -s {config.shell} {config.user}
        exec {config.shell}"""
        try:
            ssh_auth_sock = os.environ["SSH_AUTH_SOCK"]
        except KeyError:
            ssh_auth_sock = ""
        if ssh_auth_sock:
            ssh_auth_sock_parent = pathlib.Path(
                ssh_auth_sock
            ).parent.as_posix()
            self.run_text = f"""docker run -it \
                           -v /var/run/docker.sock:/var/run/docker.sock \
                           -v {config.home}:{config.home} \
                           -v {config.project_config.directory}:{config.project_config.directory} \
                           -v {ssh_auth_sock_parent} \
                           -e SSH_AUTH_SOCK={ssh_auth_sock} \
                           --entrypoint=/entrypoint.sh -u {config.user}:{config.docker_gid} {config.tag}:latest"""
        else:
            self.run_text = f"""docker run -it \
                           -v /var/run/docker.sock:/var/run/docker.sock \
                           -v {config.home}:{config.home} \
                           -v {config.project_config.directory}:{config.project_config.directory} \
                           --entrypoint=/entrypoint.sh -u {config.user}:{config.docker_gid} {config.tag}:latest"""

        self.externalbasis = "ubuntu"
        self.base_text = f"""FROM    {self.externalbasis}
        RUN     apt update && apt install -y sudo docker.io"""

context = Context()

class CommandLineInterface:
    """Why did I put his in this module?  Why not cli.py?"""
    def __init__(self):
        self.pkg_install_cmds = {
            "debian": "apt install -y",
            "ubuntu": "apt install -y",
            "python3": "`which pip3` install",
            "python": "`which pip` install",
        }

    def _os_install(self, package_file):
        """
        take in a dict return a string of docker build RUN directives
        one RUN per package type
        one package type per JSON key
        """
        packages = " ".join(json.load(package_file.open()))
        if packages:
            for packager in self.pkg_install_cmds:
                if packager in context.externalbasis:
                    installer = self.pkg_install_cmds[packager]
            return f"RUN    {installer} {packages}"
        else:
            return ""

    def _lang_install(self, package_file):
        """
        """
        packages_dict = json.load(package_file.open())
        install_command = ""
        if packages_dict:
            for lang in packages_dict:
                if lang in self.pkg_install_cmds:
                    packages = " ".join(packages_dict[lang])
                    installer = self.pkg_install_cmds[lang]
                    install_command = (
                        install_command + f"RUN    {installer} {packages}\n"
                    )
            return install_command
        else:
            return ""

    def pave_profile(self):
        """
        Usage:
          containment pave_profile
        """
        config.personal_config.directory.mkdir()
        json.dump(
            config.personal_config.package_list,
            config.personal_config.os_packages.open(mode="w"),
        )
        json.dump({}, config.personal_config.lang_packages.open(mode="w"))
        config.personal_config.projects.mkdir()

    def pave_project(self):
        """
        Usage:
          containment pave_project
        """
        config.project_customization.directory.mkdir()
        config.project_customization.entrypoint.write_text(
            context.entrypoint_text
        )
        config.project_customization.runfile.write_text(
            context.run_text
        )
        config.project_customization.os_packages.write_text("[]")
        config.project_customization.lang_packages.write_text("{}")
        self.write_dockerfile()

    def pave_project(self):
        """
        Usage:
          containment pave_project
        """
        print("*******************")
        print("inside pave_project")
        config.project_config.directory.mkdir()
        print(config.project_config.directory.absolute())
        
        config.project_config.dockerfile.write_text(context.base_text)
        config.project_config.os_packages.write_text("[]")
        config.project_config.lang_packages.write_text("{}")
        config.project_config.dockerfile.write_text(context.base_text)
        config.project_config.dockerfile.write_text(context.entrypoint_text)
        config.project_config.dockerfile.write_text(context.run_text)

    def ensure_config(self):
        if not config.project_config.directory.is_dir():
            print("config.project_config.directory.absolute(): ",
                  config.project_config.directory.absolute())
            self.pave_project()
        if not config.personal_config.directory.is_dir():
            self.pave_profile()
        if not config.project_customization.directory.is_dir():
            self.pave_project()

    def write_dockerfile(self):
        """
        Usage:
          containment write_dockerfile
        """
        config.project_customization.dockerfile.write_text(
            self._assemble_dockerfile()
        )

    def _assemble_dockerfile(self):
        return "\n".join(
            [
                config.project_config.base.read_text(),
                self._os_install(config.project_config.os_packages),
                self._os_install(config.personal_config.os_packages),
                self._os_install(config.project_customization.os_packages),
                self._lang_install(config.project_config.lang_packages),
                self._lang_install(config.personal_config.lang_packages),
                self._lang_install(
                    config.project_customization.lang_packages
                ),
                context.project_adapter,
            ]
        )

    def build(self):
        """
        Usage:
          containment build
        """
        print("We have entered the build method!")
        docker_build = docker.from_env().api.build
        build_actions = []
        for a in docker_build(
            str(config.project_customization.directory), tag=config.tag
        ):
            build_actions.append(a)

    def run(self):
        """
        Usage:
          containment run
        """
        run_command = (
            config.project_customization.runfile.read_text().split()
        )
        chmod_string = (
            "chmod +x "
            + config.project_customization.runfile.absolute().as_posix()
        )
        subprocess.run(chmod_string.split())
        subprocess.run(
            run_command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
        )
