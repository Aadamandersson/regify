#!/usr/bin/env bash

ATOM_PKG="syntax_highlighting/language-regify"
VSCODE_PKG="syntax_highlighting/language-vscode"

ATOM_INSTALL_PATH="/.atom/packages"
VSCODE_INSTALL_PATH="/.vscode/packages"

function check_if_installed() {
    if [[ -z $(which $1) ]]; then {
        echo "[-]" $1 "is not installed!"
        exit
    }
    else
        echo "[+]" $1 "is installed"
    fi
}

function check_directory() {
    if [[ -d $1 ]]; then
        echo "[+] Directory $1 exists"
    else {
        echo "[-] Directory $1 does not exist!"
        exit
    }
    fi
}

if [[ -z $1 ]]; then
    echo "usage: " $0 "<atom|vscode|noeditor>"
    exit
fi

echo "~~~~~~~~~~~~~ Installation wizard for REgify ~~~~~~~~~~~~~"
echo "[+] Checking dependencies..."
check_if_installed pip3

PKG_PATH=""
EDITOR_PATH=""


if [[ $1 == "atom" ]]; then {
    check_if_installed atom
    PKG_PATH=$ATOM_PKG
    EDITOR_PATH=$ATOM_INSTALL_PATH

}
    #statements
elif [[ $1 == "vscode" ]]; then {
    check_if_installed code
    PKG_PATH=$VSCODE_PKG
    EDITOR_PATH=$VSCODE_INSTALL_PATH
}

elif [[ $1 == "noeditor" ]]; then {
    echo "[+] No syntax highlighter will be installed"
}
else {
    echo "[-] Unknown argument" $1
    exit
}
fi

PKG_PATH=$(pwd)"/"$INSTALL_PKG_PATH
EDITOR_PATH=$HOME$EDITOR_PATH

check_directory $PKG_PATH
check_directory $EDITOR_PATH



echo "[+] Copying" $PKG_PATH "into" $EDITOR_PATH
cp -rf $PKG_PATH $EDITOR_PATH

if [[ $? -eq 0 ]]; then {
    echo "[+] Copied files sucessfully"
}
else {
    echo "[-] Copy failed"
    exit
}
fi
