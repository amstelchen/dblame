# dblame

TK frontend to systemd-analyze

#### Installation

Steps assume that `python` (>= 3.7) and `pip` are already installed.

Install dependencies (see sections below)

Then, run:

    $ pip install dblame

Install directly from ``github``:


    $ pip install git+https://github.com/amstelchen/dblame#egg=dblame

When completed, run it with:

    $ dblame

#### Dependencies

On Debian-based distributions (Mint, Ubuntu, MX, etc.), installation of the packages `tk` and `python3-tk` may be necessary.

    $ sudo apt install python3-tk tk

On Arch based distributions, only tk needs to be installed.

    $ sudo pacman -S tk

On Fedora Linux, installation of the packages `python3-tkinter` and `tk` is necessary instead.

    $ sudo dnf install python3-tkinter tk

openSUSE needs the package `python3-tk` (`python3[8|9|10|11]-tk`) installed.

    $ sudo zypper install python310-tk

Anyways, it often helps to keep your python installation updated:

    $ python -m pip install --upgrade pip wheel setuptools

#### System requirements

*dblame* <sup>(0.1.2)</sup> is tested to work on the following distributions:

- Debian 10 or newer (10.1, 11.3) 
- Ubuntu, Kubuntu, Xubuntu 20.04 or newer
- Pop!_OS 20.04 or newer
- Linux Mint 20 or newer
- Arch Linux
- Manjaro 20
- Garuda Linux
- ArcoLinux
- Zorin OS 16.1 or newer 
- EndeavourOS 
- Fedora 37 Workstation 
- openSUSE Tumbleweed and Leap 15.2 or newer 

No support:

- Zorin OS 15.3 (no support for Python 3.7)
- MX Linux (no systemd)
- Void Linux (no systemd)

Tests underway:

- none currently.

#### TODO

:pushpin: better regex matching when total time > 1min

```
Startup finished in 8.556s (kernel) + 55.596s (userspace) = 1min 4.152s 
graphical.target reached after 54.183s in userspace
```

#### Licences

*dblame* is licensed under the [GPLv2](LICENSE) license.

<a href="https://www.flaticon.com/free-icons/time" title="time icons">Time icons created by Freepik - Flaticon</a>
