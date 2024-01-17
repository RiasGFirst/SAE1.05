<p align="center">
  <img src="https://i.ibb.co/whbpBVn/mitm.png" width="100" />
</p>
<p align="center">
    <h1 align="center">SAE1.05</h1>
</p>
<p align="center">
    <em>SAE 1.05 Traiter des données, séparé en 2 fichiers, un script de découvert des IP dans un réseau et un MITM. Codé en Python avec l'aide de la librairie Scapy. Équipe TRAG Marcelin et NECHAEV Vladimir</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/RiasGFirst/SAE1.05?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/languages/top/RiasGFirst/SAE1.05?style=flat&color=0080ff" alt="repo-top-language">
<p>
<hr>

---

## 📂 Repository Structure

```sh
└── SAE1.05/
    ├── discover.py
    └── mitm.py
```
---

## 🚀 Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `Python Version 3.x.x`

---

### ⚙️ Installation

1. Clone the SAE1.05 repository:

```sh
git clone https://github.com/RiasGFirst/SAE1.05
```

2. Install the dependence 

```sh
sudo apt install python3-scapy
```

3. Go to the directory

```sh
cd SAE1.05/
```

---

### 🤖 Running the discover.py

Pour le discover.py :

L'option -a déclenche la découverte active avec l'adresse IP d'un hôte qui sera donnée en argument, comme le montre l'exemple ci-dessous.

```sh
sudo python3 discover.py -a 192.168.1.2
```

L'option -p permet de déclencher une découverte passive, avec comme argument l'adresse IP de l'hôte cible.

```sh
sudo python3 discover.py -p 192.168.1.2
```

L'option -t permet de tester la présence de l'ensemble des hôtes d'un réseau avec ICMP et dont l'adresse réseau est donnée en argument, comme le montre l'exemple ci-dessous.

```sh
sudo python3 discover.py -t 192.168.1.0/24
```

Lorsqu'une écoute est déclenchée, le programme affiche le résultat de la découverte en indiquant si un hôte est présent ou non. Ce même résultat pourra être exporté dans un fichier avec l'option -x, dont le nom est donné en argument.

```sh
sudo python3 discover.py -a 192.168.1.2 -x /tmp/resultat.txt
```

---

### 🤖 Running the mitm.py

Pour le mitm.py il faut faire la commande 

```sh
sudo python3 mitm.py -n IPNETWORK/24
```

---

## 📄 License

This project is protected under the MIT Licence

